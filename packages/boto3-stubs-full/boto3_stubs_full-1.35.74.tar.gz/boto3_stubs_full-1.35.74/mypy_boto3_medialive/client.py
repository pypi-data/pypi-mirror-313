"""
Type annotations for medialive service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_medialive.client import MediaLiveClient

    session = Session()
    client: MediaLiveClient = session.client("medialive")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeSchedulePaginator,
    ListChannelPlacementGroupsPaginator,
    ListChannelsPaginator,
    ListCloudWatchAlarmTemplateGroupsPaginator,
    ListCloudWatchAlarmTemplatesPaginator,
    ListClustersPaginator,
    ListEventBridgeRuleTemplateGroupsPaginator,
    ListEventBridgeRuleTemplatesPaginator,
    ListInputDevicesPaginator,
    ListInputDeviceTransfersPaginator,
    ListInputSecurityGroupsPaginator,
    ListInputsPaginator,
    ListMultiplexesPaginator,
    ListMultiplexProgramsPaginator,
    ListNetworksPaginator,
    ListNodesPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
    ListSignalMapsPaginator,
)
from .type_defs import (
    AcceptInputDeviceTransferRequestRequestTypeDef,
    BatchDeleteRequestRequestTypeDef,
    BatchDeleteResponseTypeDef,
    BatchStartRequestRequestTypeDef,
    BatchStartResponseTypeDef,
    BatchStopRequestRequestTypeDef,
    BatchStopResponseTypeDef,
    BatchUpdateScheduleRequestRequestTypeDef,
    BatchUpdateScheduleResponseTypeDef,
    CancelInputDeviceTransferRequestRequestTypeDef,
    ClaimDeviceRequestRequestTypeDef,
    CreateChannelPlacementGroupRequestRequestTypeDef,
    CreateChannelPlacementGroupResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    CreateCloudWatchAlarmTemplateGroupResponseTypeDef,
    CreateCloudWatchAlarmTemplateRequestRequestTypeDef,
    CreateCloudWatchAlarmTemplateResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    CreateEventBridgeRuleTemplateGroupResponseTypeDef,
    CreateEventBridgeRuleTemplateRequestRequestTypeDef,
    CreateEventBridgeRuleTemplateResponseTypeDef,
    CreateInputRequestRequestTypeDef,
    CreateInputResponseTypeDef,
    CreateInputSecurityGroupRequestRequestTypeDef,
    CreateInputSecurityGroupResponseTypeDef,
    CreateMultiplexProgramRequestRequestTypeDef,
    CreateMultiplexProgramResponseTypeDef,
    CreateMultiplexRequestRequestTypeDef,
    CreateMultiplexResponseTypeDef,
    CreateNetworkRequestRequestTypeDef,
    CreateNetworkResponseTypeDef,
    CreateNodeRegistrationScriptRequestRequestTypeDef,
    CreateNodeRegistrationScriptResponseTypeDef,
    CreateNodeRequestRequestTypeDef,
    CreateNodeResponseTypeDef,
    CreatePartnerInputRequestRequestTypeDef,
    CreatePartnerInputResponseTypeDef,
    CreateSignalMapRequestRequestTypeDef,
    CreateSignalMapResponseTypeDef,
    CreateTagsRequestRequestTypeDef,
    DeleteChannelPlacementGroupRequestRequestTypeDef,
    DeleteChannelPlacementGroupResponseTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteChannelResponseTypeDef,
    DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    DeleteCloudWatchAlarmTemplateRequestRequestTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    DeleteEventBridgeRuleTemplateRequestRequestTypeDef,
    DeleteInputRequestRequestTypeDef,
    DeleteInputSecurityGroupRequestRequestTypeDef,
    DeleteMultiplexProgramRequestRequestTypeDef,
    DeleteMultiplexProgramResponseTypeDef,
    DeleteMultiplexRequestRequestTypeDef,
    DeleteMultiplexResponseTypeDef,
    DeleteNetworkRequestRequestTypeDef,
    DeleteNetworkResponseTypeDef,
    DeleteNodeRequestRequestTypeDef,
    DeleteNodeResponseTypeDef,
    DeleteReservationRequestRequestTypeDef,
    DeleteReservationResponseTypeDef,
    DeleteScheduleRequestRequestTypeDef,
    DeleteSignalMapRequestRequestTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DescribeAccountConfigurationResponseTypeDef,
    DescribeChannelPlacementGroupRequestRequestTypeDef,
    DescribeChannelPlacementGroupResponseTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeInputDeviceRequestRequestTypeDef,
    DescribeInputDeviceResponseTypeDef,
    DescribeInputDeviceThumbnailRequestRequestTypeDef,
    DescribeInputDeviceThumbnailResponseTypeDef,
    DescribeInputRequestRequestTypeDef,
    DescribeInputResponseTypeDef,
    DescribeInputSecurityGroupRequestRequestTypeDef,
    DescribeInputSecurityGroupResponseTypeDef,
    DescribeMultiplexProgramRequestRequestTypeDef,
    DescribeMultiplexProgramResponseTypeDef,
    DescribeMultiplexRequestRequestTypeDef,
    DescribeMultiplexResponseTypeDef,
    DescribeNetworkRequestRequestTypeDef,
    DescribeNetworkResponseTypeDef,
    DescribeNodeRequestRequestTypeDef,
    DescribeNodeResponseTypeDef,
    DescribeOfferingRequestRequestTypeDef,
    DescribeOfferingResponseTypeDef,
    DescribeReservationRequestRequestTypeDef,
    DescribeReservationResponseTypeDef,
    DescribeScheduleRequestRequestTypeDef,
    DescribeScheduleResponseTypeDef,
    DescribeThumbnailsRequestRequestTypeDef,
    DescribeThumbnailsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    GetCloudWatchAlarmTemplateGroupResponseTypeDef,
    GetCloudWatchAlarmTemplateRequestRequestTypeDef,
    GetCloudWatchAlarmTemplateResponseTypeDef,
    GetEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    GetEventBridgeRuleTemplateGroupResponseTypeDef,
    GetEventBridgeRuleTemplateRequestRequestTypeDef,
    GetEventBridgeRuleTemplateResponseTypeDef,
    GetSignalMapRequestRequestTypeDef,
    GetSignalMapResponseTypeDef,
    ListChannelPlacementGroupsRequestRequestTypeDef,
    ListChannelPlacementGroupsResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef,
    ListCloudWatchAlarmTemplateGroupsResponseTypeDef,
    ListCloudWatchAlarmTemplatesRequestRequestTypeDef,
    ListCloudWatchAlarmTemplatesResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef,
    ListEventBridgeRuleTemplateGroupsResponseTypeDef,
    ListEventBridgeRuleTemplatesRequestRequestTypeDef,
    ListEventBridgeRuleTemplatesResponseTypeDef,
    ListInputDevicesRequestRequestTypeDef,
    ListInputDevicesResponseTypeDef,
    ListInputDeviceTransfersRequestRequestTypeDef,
    ListInputDeviceTransfersResponseTypeDef,
    ListInputSecurityGroupsRequestRequestTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsRequestRequestTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexesRequestRequestTypeDef,
    ListMultiplexesResponseTypeDef,
    ListMultiplexProgramsRequestRequestTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListNetworksRequestRequestTypeDef,
    ListNetworksResponseTypeDef,
    ListNodesRequestRequestTypeDef,
    ListNodesResponseTypeDef,
    ListOfferingsRequestRequestTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestRequestTypeDef,
    ListReservationsResponseTypeDef,
    ListSignalMapsRequestRequestTypeDef,
    ListSignalMapsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PurchaseOfferingRequestRequestTypeDef,
    PurchaseOfferingResponseTypeDef,
    RebootInputDeviceRequestRequestTypeDef,
    RejectInputDeviceTransferRequestRequestTypeDef,
    RestartChannelPipelinesRequestRequestTypeDef,
    RestartChannelPipelinesResponseTypeDef,
    StartChannelRequestRequestTypeDef,
    StartChannelResponseTypeDef,
    StartDeleteMonitorDeploymentRequestRequestTypeDef,
    StartDeleteMonitorDeploymentResponseTypeDef,
    StartInputDeviceMaintenanceWindowRequestRequestTypeDef,
    StartInputDeviceRequestRequestTypeDef,
    StartMonitorDeploymentRequestRequestTypeDef,
    StartMonitorDeploymentResponseTypeDef,
    StartMultiplexRequestRequestTypeDef,
    StartMultiplexResponseTypeDef,
    StartUpdateSignalMapRequestRequestTypeDef,
    StartUpdateSignalMapResponseTypeDef,
    StopChannelRequestRequestTypeDef,
    StopChannelResponseTypeDef,
    StopInputDeviceRequestRequestTypeDef,
    StopMultiplexRequestRequestTypeDef,
    StopMultiplexResponseTypeDef,
    TransferInputDeviceRequestRequestTypeDef,
    UpdateAccountConfigurationRequestRequestTypeDef,
    UpdateAccountConfigurationResponseTypeDef,
    UpdateChannelClassRequestRequestTypeDef,
    UpdateChannelClassResponseTypeDef,
    UpdateChannelPlacementGroupRequestRequestTypeDef,
    UpdateChannelPlacementGroupResponseTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    UpdateCloudWatchAlarmTemplateGroupResponseTypeDef,
    UpdateCloudWatchAlarmTemplateRequestRequestTypeDef,
    UpdateCloudWatchAlarmTemplateResponseTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    UpdateEventBridgeRuleTemplateGroupResponseTypeDef,
    UpdateEventBridgeRuleTemplateRequestRequestTypeDef,
    UpdateEventBridgeRuleTemplateResponseTypeDef,
    UpdateInputDeviceRequestRequestTypeDef,
    UpdateInputDeviceResponseTypeDef,
    UpdateInputRequestRequestTypeDef,
    UpdateInputResponseTypeDef,
    UpdateInputSecurityGroupRequestRequestTypeDef,
    UpdateInputSecurityGroupResponseTypeDef,
    UpdateMultiplexProgramRequestRequestTypeDef,
    UpdateMultiplexProgramResponseTypeDef,
    UpdateMultiplexRequestRequestTypeDef,
    UpdateMultiplexResponseTypeDef,
    UpdateNetworkRequestRequestTypeDef,
    UpdateNetworkResponseTypeDef,
    UpdateNodeRequestRequestTypeDef,
    UpdateNodeResponseTypeDef,
    UpdateNodeStateRequestRequestTypeDef,
    UpdateNodeStateResponseTypeDef,
    UpdateReservationRequestRequestTypeDef,
    UpdateReservationResponseTypeDef,
)
from .waiter import (
    ChannelCreatedWaiter,
    ChannelDeletedWaiter,
    ChannelPlacementGroupAssignedWaiter,
    ChannelPlacementGroupDeletedWaiter,
    ChannelPlacementGroupUnassignedWaiter,
    ChannelRunningWaiter,
    ChannelStoppedWaiter,
    ClusterCreatedWaiter,
    ClusterDeletedWaiter,
    InputAttachedWaiter,
    InputDeletedWaiter,
    InputDetachedWaiter,
    MultiplexCreatedWaiter,
    MultiplexDeletedWaiter,
    MultiplexRunningWaiter,
    MultiplexStoppedWaiter,
    NodeDeregisteredWaiter,
    NodeRegisteredWaiter,
    SignalMapCreatedWaiter,
    SignalMapMonitorDeletedWaiter,
    SignalMapMonitorDeployedWaiter,
    SignalMapUpdatedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MediaLiveClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadGatewayException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class MediaLiveClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaLiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#close)
        """

    def accept_input_device_transfer(
        self, **kwargs: Unpack[AcceptInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accept an incoming input device transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/accept_input_device_transfer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#accept_input_device_transfer)
        """

    def batch_delete(
        self, **kwargs: Unpack[BatchDeleteRequestRequestTypeDef]
    ) -> BatchDeleteResponseTypeDef:
        """
        Starts delete of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/batch_delete.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#batch_delete)
        """

    def batch_start(
        self, **kwargs: Unpack[BatchStartRequestRequestTypeDef]
    ) -> BatchStartResponseTypeDef:
        """
        Starts existing resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/batch_start.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#batch_start)
        """

    def batch_stop(
        self, **kwargs: Unpack[BatchStopRequestRequestTypeDef]
    ) -> BatchStopResponseTypeDef:
        """
        Stops running resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/batch_stop.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#batch_stop)
        """

    def batch_update_schedule(
        self, **kwargs: Unpack[BatchUpdateScheduleRequestRequestTypeDef]
    ) -> BatchUpdateScheduleResponseTypeDef:
        """
        Update a channel schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/batch_update_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#batch_update_schedule)
        """

    def cancel_input_device_transfer(
        self, **kwargs: Unpack[CancelInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancel an input device transfer that you have requested.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/cancel_input_device_transfer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#cancel_input_device_transfer)
        """

    def claim_device(self, **kwargs: Unpack[ClaimDeviceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Send a request to claim an AWS Elemental device that you have purchased from a
        third-party vendor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/claim_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#claim_device)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_channel)
        """

    def create_input(
        self, **kwargs: Unpack[CreateInputRequestRequestTypeDef]
    ) -> CreateInputResponseTypeDef:
        """
        Create an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_input)
        """

    def create_input_security_group(
        self, **kwargs: Unpack[CreateInputSecurityGroupRequestRequestTypeDef]
    ) -> CreateInputSecurityGroupResponseTypeDef:
        """
        Creates a Input Security Group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_input_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_input_security_group)
        """

    def create_multiplex(
        self, **kwargs: Unpack[CreateMultiplexRequestRequestTypeDef]
    ) -> CreateMultiplexResponseTypeDef:
        """
        Create a new multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_multiplex)
        """

    def create_multiplex_program(
        self, **kwargs: Unpack[CreateMultiplexProgramRequestRequestTypeDef]
    ) -> CreateMultiplexProgramResponseTypeDef:
        """
        Create a new program in the multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_multiplex_program.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_multiplex_program)
        """

    def create_partner_input(
        self, **kwargs: Unpack[CreatePartnerInputRequestRequestTypeDef]
    ) -> CreatePartnerInputResponseTypeDef:
        """
        Create a partner input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_partner_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_partner_input)
        """

    def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Create tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_tags)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> DeleteChannelResponseTypeDef:
        """
        Starts deletion of channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_channel)
        """

    def delete_input(self, **kwargs: Unpack[DeleteInputRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the input end point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_input)
        """

    def delete_input_security_group(
        self, **kwargs: Unpack[DeleteInputSecurityGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Input Security Group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_input_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_input_security_group)
        """

    def delete_multiplex(
        self, **kwargs: Unpack[DeleteMultiplexRequestRequestTypeDef]
    ) -> DeleteMultiplexResponseTypeDef:
        """
        Delete a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_multiplex)
        """

    def delete_multiplex_program(
        self, **kwargs: Unpack[DeleteMultiplexProgramRequestRequestTypeDef]
    ) -> DeleteMultiplexProgramResponseTypeDef:
        """
        Delete a program from a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_multiplex_program.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_multiplex_program)
        """

    def delete_reservation(
        self, **kwargs: Unpack[DeleteReservationRequestRequestTypeDef]
    ) -> DeleteReservationResponseTypeDef:
        """
        Delete an expired reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_reservation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_reservation)
        """

    def delete_schedule(
        self, **kwargs: Unpack[DeleteScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete all schedule actions on a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_schedule)
        """

    def delete_tags(
        self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_tags)
        """

    def describe_account_configuration(self) -> DescribeAccountConfigurationResponseTypeDef:
        """
        Describe account configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_account_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_account_configuration)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Gets details about a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_channel)
        """

    def describe_input(
        self, **kwargs: Unpack[DescribeInputRequestRequestTypeDef]
    ) -> DescribeInputResponseTypeDef:
        """
        Produces details about an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_input)
        """

    def describe_input_device(
        self, **kwargs: Unpack[DescribeInputDeviceRequestRequestTypeDef]
    ) -> DescribeInputDeviceResponseTypeDef:
        """
        Gets the details for the input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_input_device)
        """

    def describe_input_device_thumbnail(
        self, **kwargs: Unpack[DescribeInputDeviceThumbnailRequestRequestTypeDef]
    ) -> DescribeInputDeviceThumbnailResponseTypeDef:
        """
        Get the latest thumbnail data for the input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_input_device_thumbnail.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_input_device_thumbnail)
        """

    def describe_input_security_group(
        self, **kwargs: Unpack[DescribeInputSecurityGroupRequestRequestTypeDef]
    ) -> DescribeInputSecurityGroupResponseTypeDef:
        """
        Produces a summary of an Input Security Group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_input_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_input_security_group)
        """

    def describe_multiplex(
        self, **kwargs: Unpack[DescribeMultiplexRequestRequestTypeDef]
    ) -> DescribeMultiplexResponseTypeDef:
        """
        Gets details about a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_multiplex)
        """

    def describe_multiplex_program(
        self, **kwargs: Unpack[DescribeMultiplexProgramRequestRequestTypeDef]
    ) -> DescribeMultiplexProgramResponseTypeDef:
        """
        Get the details for a program in a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_multiplex_program.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_multiplex_program)
        """

    def describe_offering(
        self, **kwargs: Unpack[DescribeOfferingRequestRequestTypeDef]
    ) -> DescribeOfferingResponseTypeDef:
        """
        Get details for an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_offering.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_offering)
        """

    def describe_reservation(
        self, **kwargs: Unpack[DescribeReservationRequestRequestTypeDef]
    ) -> DescribeReservationResponseTypeDef:
        """
        Get details for a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_reservation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_reservation)
        """

    def describe_schedule(
        self, **kwargs: Unpack[DescribeScheduleRequestRequestTypeDef]
    ) -> DescribeScheduleResponseTypeDef:
        """
        Get a channel schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_schedule)
        """

    def describe_thumbnails(
        self, **kwargs: Unpack[DescribeThumbnailsRequestRequestTypeDef]
    ) -> DescribeThumbnailsResponseTypeDef:
        """
        Describe the latest thumbnails data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_thumbnails.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_thumbnails)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Produces list of channels that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_channels)
        """

    def list_input_device_transfers(
        self, **kwargs: Unpack[ListInputDeviceTransfersRequestRequestTypeDef]
    ) -> ListInputDeviceTransfersResponseTypeDef:
        """
        List input devices that are currently being transferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_input_device_transfers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_input_device_transfers)
        """

    def list_input_devices(
        self, **kwargs: Unpack[ListInputDevicesRequestRequestTypeDef]
    ) -> ListInputDevicesResponseTypeDef:
        """
        List input devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_input_devices.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_input_devices)
        """

    def list_input_security_groups(
        self, **kwargs: Unpack[ListInputSecurityGroupsRequestRequestTypeDef]
    ) -> ListInputSecurityGroupsResponseTypeDef:
        """
        Produces a list of Input Security Groups for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_input_security_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_input_security_groups)
        """

    def list_inputs(
        self, **kwargs: Unpack[ListInputsRequestRequestTypeDef]
    ) -> ListInputsResponseTypeDef:
        """
        Produces list of inputs that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_inputs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_inputs)
        """

    def list_multiplex_programs(
        self, **kwargs: Unpack[ListMultiplexProgramsRequestRequestTypeDef]
    ) -> ListMultiplexProgramsResponseTypeDef:
        """
        List the programs that currently exist for a specific multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_multiplex_programs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_multiplex_programs)
        """

    def list_multiplexes(
        self, **kwargs: Unpack[ListMultiplexesRequestRequestTypeDef]
    ) -> ListMultiplexesResponseTypeDef:
        """
        Retrieve a list of the existing multiplexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_multiplexes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_multiplexes)
        """

    def list_offerings(
        self, **kwargs: Unpack[ListOfferingsRequestRequestTypeDef]
    ) -> ListOfferingsResponseTypeDef:
        """
        List offerings available for purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_offerings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_offerings)
        """

    def list_reservations(
        self, **kwargs: Unpack[ListReservationsRequestRequestTypeDef]
    ) -> ListReservationsResponseTypeDef:
        """
        List purchased reservations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_reservations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_reservations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Produces list of tags that have been created for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_tags_for_resource)
        """

    def purchase_offering(
        self, **kwargs: Unpack[PurchaseOfferingRequestRequestTypeDef]
    ) -> PurchaseOfferingResponseTypeDef:
        """
        Purchase an offering and create a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/purchase_offering.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#purchase_offering)
        """

    def reboot_input_device(
        self, **kwargs: Unpack[RebootInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Send a reboot command to the specified input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/reboot_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#reboot_input_device)
        """

    def reject_input_device_transfer(
        self, **kwargs: Unpack[RejectInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Reject the transfer of the specified input device to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/reject_input_device_transfer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#reject_input_device_transfer)
        """

    def start_channel(
        self, **kwargs: Unpack[StartChannelRequestRequestTypeDef]
    ) -> StartChannelResponseTypeDef:
        """
        Starts an existing channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_channel)
        """

    def start_input_device(
        self, **kwargs: Unpack[StartInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start an input device that is attached to a MediaConnect flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_input_device)
        """

    def start_input_device_maintenance_window(
        self, **kwargs: Unpack[StartInputDeviceMaintenanceWindowRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start a maintenance window for the specified input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_input_device_maintenance_window.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_input_device_maintenance_window)
        """

    def start_multiplex(
        self, **kwargs: Unpack[StartMultiplexRequestRequestTypeDef]
    ) -> StartMultiplexResponseTypeDef:
        """
        Start (run) the multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_multiplex)
        """

    def stop_channel(
        self, **kwargs: Unpack[StopChannelRequestRequestTypeDef]
    ) -> StopChannelResponseTypeDef:
        """
        Stops a running channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/stop_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#stop_channel)
        """

    def stop_input_device(
        self, **kwargs: Unpack[StopInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stop an input device that is attached to a MediaConnect flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/stop_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#stop_input_device)
        """

    def stop_multiplex(
        self, **kwargs: Unpack[StopMultiplexRequestRequestTypeDef]
    ) -> StopMultiplexResponseTypeDef:
        """
        Stops a running multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/stop_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#stop_multiplex)
        """

    def transfer_input_device(
        self, **kwargs: Unpack[TransferInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start an input device transfer to another AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/transfer_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#transfer_input_device)
        """

    def update_account_configuration(
        self, **kwargs: Unpack[UpdateAccountConfigurationRequestRequestTypeDef]
    ) -> UpdateAccountConfigurationResponseTypeDef:
        """
        Update account configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_account_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_account_configuration)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_channel)
        """

    def update_channel_class(
        self, **kwargs: Unpack[UpdateChannelClassRequestRequestTypeDef]
    ) -> UpdateChannelClassResponseTypeDef:
        """
        Changes the class of the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_channel_class.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_channel_class)
        """

    def update_input(
        self, **kwargs: Unpack[UpdateInputRequestRequestTypeDef]
    ) -> UpdateInputResponseTypeDef:
        """
        Updates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_input)
        """

    def update_input_device(
        self, **kwargs: Unpack[UpdateInputDeviceRequestRequestTypeDef]
    ) -> UpdateInputDeviceResponseTypeDef:
        """
        Updates the parameters for the input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_input_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_input_device)
        """

    def update_input_security_group(
        self, **kwargs: Unpack[UpdateInputSecurityGroupRequestRequestTypeDef]
    ) -> UpdateInputSecurityGroupResponseTypeDef:
        """
        Update an Input Security Group's Whilelists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_input_security_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_input_security_group)
        """

    def update_multiplex(
        self, **kwargs: Unpack[UpdateMultiplexRequestRequestTypeDef]
    ) -> UpdateMultiplexResponseTypeDef:
        """
        Updates a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_multiplex.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_multiplex)
        """

    def update_multiplex_program(
        self, **kwargs: Unpack[UpdateMultiplexProgramRequestRequestTypeDef]
    ) -> UpdateMultiplexProgramResponseTypeDef:
        """
        Update a program in a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_multiplex_program.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_multiplex_program)
        """

    def update_reservation(
        self, **kwargs: Unpack[UpdateReservationRequestRequestTypeDef]
    ) -> UpdateReservationResponseTypeDef:
        """
        Update reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_reservation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_reservation)
        """

    def restart_channel_pipelines(
        self, **kwargs: Unpack[RestartChannelPipelinesRequestRequestTypeDef]
    ) -> RestartChannelPipelinesResponseTypeDef:
        """
        Restart pipelines in one channel that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/restart_channel_pipelines.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#restart_channel_pipelines)
        """

    def create_cloud_watch_alarm_template(
        self, **kwargs: Unpack[CreateCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> CreateCloudWatchAlarmTemplateResponseTypeDef:
        """
        Creates a cloudwatch alarm template to dynamically generate cloudwatch metric
        alarms on targeted resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_cloud_watch_alarm_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_cloud_watch_alarm_template)
        """

    def create_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> CreateCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Creates a cloudwatch alarm template group to group your cloudwatch alarm
        templates and to attach to signal maps for dynamically creating alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_cloud_watch_alarm_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_cloud_watch_alarm_template_group)
        """

    def create_event_bridge_rule_template(
        self, **kwargs: Unpack[CreateEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> CreateEventBridgeRuleTemplateResponseTypeDef:
        """
        Creates an eventbridge rule template to monitor events and send notifications
        to your targeted resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_event_bridge_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_event_bridge_rule_template)
        """

    def create_event_bridge_rule_template_group(
        self, **kwargs: Unpack[CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> CreateEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Creates an eventbridge rule template group to group your eventbridge rule
        templates and to attach to signal maps for dynamically creating notification
        rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_event_bridge_rule_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_event_bridge_rule_template_group)
        """

    def create_signal_map(
        self, **kwargs: Unpack[CreateSignalMapRequestRequestTypeDef]
    ) -> CreateSignalMapResponseTypeDef:
        """
        Initiates the creation of a new signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_signal_map.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_signal_map)
        """

    def delete_cloud_watch_alarm_template(
        self, **kwargs: Unpack[DeleteCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_cloud_watch_alarm_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_cloud_watch_alarm_template)
        """

    def delete_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_cloud_watch_alarm_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_cloud_watch_alarm_template_group)
        """

    def delete_event_bridge_rule_template(
        self, **kwargs: Unpack[DeleteEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_event_bridge_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_event_bridge_rule_template)
        """

    def delete_event_bridge_rule_template_group(
        self, **kwargs: Unpack[DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_event_bridge_rule_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_event_bridge_rule_template_group)
        """

    def delete_signal_map(
        self, **kwargs: Unpack[DeleteSignalMapRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_signal_map.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_signal_map)
        """

    def get_cloud_watch_alarm_template(
        self, **kwargs: Unpack[GetCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> GetCloudWatchAlarmTemplateResponseTypeDef:
        """
        Retrieves the specified cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_cloud_watch_alarm_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_cloud_watch_alarm_template)
        """

    def get_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> GetCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Retrieves the specified cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_cloud_watch_alarm_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_cloud_watch_alarm_template_group)
        """

    def get_event_bridge_rule_template(
        self, **kwargs: Unpack[GetEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> GetEventBridgeRuleTemplateResponseTypeDef:
        """
        Retrieves the specified eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_event_bridge_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_event_bridge_rule_template)
        """

    def get_event_bridge_rule_template_group(
        self, **kwargs: Unpack[GetEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> GetEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Retrieves the specified eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_event_bridge_rule_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_event_bridge_rule_template_group)
        """

    def get_signal_map(
        self, **kwargs: Unpack[GetSignalMapRequestRequestTypeDef]
    ) -> GetSignalMapResponseTypeDef:
        """
        Retrieves the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_signal_map.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_signal_map)
        """

    def list_cloud_watch_alarm_template_groups(
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef]
    ) -> ListCloudWatchAlarmTemplateGroupsResponseTypeDef:
        """
        Lists cloudwatch alarm template groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_cloud_watch_alarm_template_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_cloud_watch_alarm_template_groups)
        """

    def list_cloud_watch_alarm_templates(
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplatesRequestRequestTypeDef]
    ) -> ListCloudWatchAlarmTemplatesResponseTypeDef:
        """
        Lists cloudwatch alarm templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_cloud_watch_alarm_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_cloud_watch_alarm_templates)
        """

    def list_event_bridge_rule_template_groups(
        self, **kwargs: Unpack[ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef]
    ) -> ListEventBridgeRuleTemplateGroupsResponseTypeDef:
        """
        Lists eventbridge rule template groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_event_bridge_rule_template_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_event_bridge_rule_template_groups)
        """

    def list_event_bridge_rule_templates(
        self, **kwargs: Unpack[ListEventBridgeRuleTemplatesRequestRequestTypeDef]
    ) -> ListEventBridgeRuleTemplatesResponseTypeDef:
        """
        Lists eventbridge rule templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_event_bridge_rule_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_event_bridge_rule_templates)
        """

    def list_signal_maps(
        self, **kwargs: Unpack[ListSignalMapsRequestRequestTypeDef]
    ) -> ListSignalMapsResponseTypeDef:
        """
        Lists signal maps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_signal_maps.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_signal_maps)
        """

    def start_delete_monitor_deployment(
        self, **kwargs: Unpack[StartDeleteMonitorDeploymentRequestRequestTypeDef]
    ) -> StartDeleteMonitorDeploymentResponseTypeDef:
        """
        Initiates a deployment to delete the monitor of the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_delete_monitor_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_delete_monitor_deployment)
        """

    def start_monitor_deployment(
        self, **kwargs: Unpack[StartMonitorDeploymentRequestRequestTypeDef]
    ) -> StartMonitorDeploymentResponseTypeDef:
        """
        Initiates a deployment to deploy the latest monitor of the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_monitor_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_monitor_deployment)
        """

    def start_update_signal_map(
        self, **kwargs: Unpack[StartUpdateSignalMapRequestRequestTypeDef]
    ) -> StartUpdateSignalMapResponseTypeDef:
        """
        Initiates an update for the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/start_update_signal_map.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#start_update_signal_map)
        """

    def update_cloud_watch_alarm_template(
        self, **kwargs: Unpack[UpdateCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> UpdateCloudWatchAlarmTemplateResponseTypeDef:
        """
        Updates the specified cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_cloud_watch_alarm_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_cloud_watch_alarm_template)
        """

    def update_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> UpdateCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Updates the specified cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_cloud_watch_alarm_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_cloud_watch_alarm_template_group)
        """

    def update_event_bridge_rule_template(
        self, **kwargs: Unpack[UpdateEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> UpdateEventBridgeRuleTemplateResponseTypeDef:
        """
        Updates the specified eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_event_bridge_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_event_bridge_rule_template)
        """

    def update_event_bridge_rule_template_group(
        self, **kwargs: Unpack[UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> UpdateEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Updates the specified eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_event_bridge_rule_template_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_event_bridge_rule_template_group)
        """

    def create_channel_placement_group(
        self, **kwargs: Unpack[CreateChannelPlacementGroupRequestRequestTypeDef]
    ) -> CreateChannelPlacementGroupResponseTypeDef:
        """
        Create a ChannelPlacementGroup in the specified Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_channel_placement_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_channel_placement_group)
        """

    def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Create a new Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_cluster)
        """

    def create_network(
        self, **kwargs: Unpack[CreateNetworkRequestRequestTypeDef]
    ) -> CreateNetworkResponseTypeDef:
        """
        Create as many Networks as you need.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_network.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_network)
        """

    def create_node(
        self, **kwargs: Unpack[CreateNodeRequestRequestTypeDef]
    ) -> CreateNodeResponseTypeDef:
        """
        Create a Node in the specified Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_node)
        """

    def create_node_registration_script(
        self, **kwargs: Unpack[CreateNodeRegistrationScriptRequestRequestTypeDef]
    ) -> CreateNodeRegistrationScriptResponseTypeDef:
        """
        Create the Register Node script for all the nodes intended for a specific
        Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/create_node_registration_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#create_node_registration_script)
        """

    def delete_channel_placement_group(
        self, **kwargs: Unpack[DeleteChannelPlacementGroupRequestRequestTypeDef]
    ) -> DeleteChannelPlacementGroupResponseTypeDef:
        """
        Delete the specified ChannelPlacementGroup that exists in the specified Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_channel_placement_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_channel_placement_group)
        """

    def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Delete a Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_cluster)
        """

    def delete_network(
        self, **kwargs: Unpack[DeleteNetworkRequestRequestTypeDef]
    ) -> DeleteNetworkResponseTypeDef:
        """
        Delete a Network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_network.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_network)
        """

    def delete_node(
        self, **kwargs: Unpack[DeleteNodeRequestRequestTypeDef]
    ) -> DeleteNodeResponseTypeDef:
        """
        Delete a Node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/delete_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#delete_node)
        """

    def describe_channel_placement_group(
        self, **kwargs: Unpack[DescribeChannelPlacementGroupRequestRequestTypeDef]
    ) -> DescribeChannelPlacementGroupResponseTypeDef:
        """
        Get details about a ChannelPlacementGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_channel_placement_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_channel_placement_group)
        """

    def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResponseTypeDef:
        """
        Get details about a Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_cluster)
        """

    def describe_network(
        self, **kwargs: Unpack[DescribeNetworkRequestRequestTypeDef]
    ) -> DescribeNetworkResponseTypeDef:
        """
        Get details about a Network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_network.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_network)
        """

    def describe_node(
        self, **kwargs: Unpack[DescribeNodeRequestRequestTypeDef]
    ) -> DescribeNodeResponseTypeDef:
        """
        Get details about a Node in the specified Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/describe_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#describe_node)
        """

    def list_channel_placement_groups(
        self, **kwargs: Unpack[ListChannelPlacementGroupsRequestRequestTypeDef]
    ) -> ListChannelPlacementGroupsResponseTypeDef:
        """
        Retrieve the list of ChannelPlacementGroups in the specified Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_channel_placement_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_channel_placement_groups)
        """

    def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Retrieve the list of Clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_clusters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_clusters)
        """

    def list_networks(
        self, **kwargs: Unpack[ListNetworksRequestRequestTypeDef]
    ) -> ListNetworksResponseTypeDef:
        """
        Retrieve the list of Networks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_networks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_networks)
        """

    def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestRequestTypeDef]
    ) -> ListNodesResponseTypeDef:
        """
        Retrieve the list of Nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/list_nodes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#list_nodes)
        """

    def update_channel_placement_group(
        self, **kwargs: Unpack[UpdateChannelPlacementGroupRequestRequestTypeDef]
    ) -> UpdateChannelPlacementGroupResponseTypeDef:
        """
        Change the settings for a ChannelPlacementGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_channel_placement_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_channel_placement_group)
        """

    def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Change the settings for a Cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_cluster.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_cluster)
        """

    def update_network(
        self, **kwargs: Unpack[UpdateNetworkRequestRequestTypeDef]
    ) -> UpdateNetworkResponseTypeDef:
        """
        Change the settings for a Network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_network.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_network)
        """

    def update_node(
        self, **kwargs: Unpack[UpdateNodeRequestRequestTypeDef]
    ) -> UpdateNodeResponseTypeDef:
        """
        Change the settings for a Node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_node)
        """

    def update_node_state(
        self, **kwargs: Unpack[UpdateNodeStateRequestRequestTypeDef]
    ) -> UpdateNodeStateResponseTypeDef:
        """
        Update the state of a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/update_node_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#update_node_state)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_schedule"]
    ) -> DescribeSchedulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_channel_placement_groups"]
    ) -> ListChannelPlacementGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_watch_alarm_template_groups"]
    ) -> ListCloudWatchAlarmTemplateGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_watch_alarm_templates"]
    ) -> ListCloudWatchAlarmTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_bridge_rule_template_groups"]
    ) -> ListEventBridgeRuleTemplateGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_bridge_rule_templates"]
    ) -> ListEventBridgeRuleTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_device_transfers"]
    ) -> ListInputDeviceTransfersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_devices"]
    ) -> ListInputDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_security_groups"]
    ) -> ListInputSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_inputs"]) -> ListInputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplex_programs"]
    ) -> ListMultiplexProgramsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplexes"]
    ) -> ListMultiplexesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_networks"]) -> ListNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_nodes"]) -> ListNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reservations"]
    ) -> ListReservationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_signal_maps"]) -> ListSignalMapsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_created"]) -> ChannelCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_deleted"]) -> ChannelDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["channel_placement_group_assigned"]
    ) -> ChannelPlacementGroupAssignedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["channel_placement_group_deleted"]
    ) -> ChannelPlacementGroupDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["channel_placement_group_unassigned"]
    ) -> ChannelPlacementGroupUnassignedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_running"]) -> ChannelRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_stopped"]) -> ChannelStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_created"]) -> ClusterCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_deleted"]) -> ClusterDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_attached"]) -> InputAttachedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_deleted"]) -> InputDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_detached"]) -> InputDetachedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_created"]) -> MultiplexCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_deleted"]) -> MultiplexDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_running"]) -> MultiplexRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_stopped"]) -> MultiplexStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["node_deregistered"]) -> NodeDeregisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["node_registered"]) -> NodeRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["signal_map_created"]) -> SignalMapCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["signal_map_monitor_deleted"]
    ) -> SignalMapMonitorDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["signal_map_monitor_deployed"]
    ) -> SignalMapMonitorDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["signal_map_updated"]) -> SignalMapUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/client/#get_waiter)
        """
