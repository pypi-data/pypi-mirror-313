"""
Type annotations for iot1click-devices service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iot1click_devices.client import IoT1ClickDevicesServiceClient

    session = Session()
    client: IoT1ClickDevicesServiceClient = session.client("iot1click-devices")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListDeviceEventsPaginator, ListDevicesPaginator
from .type_defs import (
    ClaimDevicesByClaimCodeRequestRequestTypeDef,
    ClaimDevicesByClaimCodeResponseTypeDef,
    DescribeDeviceRequestRequestTypeDef,
    DescribeDeviceResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FinalizeDeviceClaimRequestRequestTypeDef,
    FinalizeDeviceClaimResponseTypeDef,
    GetDeviceMethodsRequestRequestTypeDef,
    GetDeviceMethodsResponseTypeDef,
    InitiateDeviceClaimRequestRequestTypeDef,
    InitiateDeviceClaimResponseTypeDef,
    InvokeDeviceMethodRequestRequestTypeDef,
    InvokeDeviceMethodResponseTypeDef,
    ListDeviceEventsRequestRequestTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListDevicesRequestRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UnclaimDeviceRequestRequestTypeDef,
    UnclaimDeviceResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDeviceStateRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IoT1ClickDevicesServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    RangeNotSatisfiableException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class IoT1ClickDevicesServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoT1ClickDevicesServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#close)
        """

    def claim_devices_by_claim_code(
        self, **kwargs: Unpack[ClaimDevicesByClaimCodeRequestRequestTypeDef]
    ) -> ClaimDevicesByClaimCodeResponseTypeDef:
        """
        Adds device(s) to your account (i.e., claim one or more devices) if and only if
        you received a claim code with the device(s).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/claim_devices_by_claim_code.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#claim_devices_by_claim_code)
        """

    def describe_device(
        self, **kwargs: Unpack[DescribeDeviceRequestRequestTypeDef]
    ) -> DescribeDeviceResponseTypeDef:
        """
        Given a device ID, returns a DescribeDeviceResponse object describing the
        details of the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/describe_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#describe_device)
        """

    def finalize_device_claim(
        self, **kwargs: Unpack[FinalizeDeviceClaimRequestRequestTypeDef]
    ) -> FinalizeDeviceClaimResponseTypeDef:
        """
        Given a device ID, finalizes the claim request for the associated device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/finalize_device_claim.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#finalize_device_claim)
        """

    def get_device_methods(
        self, **kwargs: Unpack[GetDeviceMethodsRequestRequestTypeDef]
    ) -> GetDeviceMethodsResponseTypeDef:
        """
        Given a device ID, returns the invokable methods associated with the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/get_device_methods.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#get_device_methods)
        """

    def initiate_device_claim(
        self, **kwargs: Unpack[InitiateDeviceClaimRequestRequestTypeDef]
    ) -> InitiateDeviceClaimResponseTypeDef:
        """
        Given a device ID, initiates a claim request for the associated device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/initiate_device_claim.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#initiate_device_claim)
        """

    def invoke_device_method(
        self, **kwargs: Unpack[InvokeDeviceMethodRequestRequestTypeDef]
    ) -> InvokeDeviceMethodResponseTypeDef:
        """
        Given a device ID, issues a request to invoke a named device method (with
        possible parameters).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/invoke_device_method.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#invoke_device_method)
        """

    def list_device_events(
        self, **kwargs: Unpack[ListDeviceEventsRequestRequestTypeDef]
    ) -> ListDeviceEventsResponseTypeDef:
        """
        Using a device ID, returns a DeviceEventsResponse object containing an array of
        events for the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/list_device_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#list_device_events)
        """

    def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        Lists the 1-Click compatible devices associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/list_devices.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#list_devices)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with the specified resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#list_tags_for_resource)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates the tags associated with the resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#tag_resource)
        """

    def unclaim_device(
        self, **kwargs: Unpack[UnclaimDeviceRequestRequestTypeDef]
    ) -> UnclaimDeviceResponseTypeDef:
        """
        Disassociates a device from your AWS account using its device ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/unclaim_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#unclaim_device)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Using tag keys, deletes the tags (key/value pairs) associated with the
        specified resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#untag_resource)
        """

    def update_device_state(
        self, **kwargs: Unpack[UpdateDeviceStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Using a Boolean value (true or false), this operation enables or disables the
        device given a device ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/update_device_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#update_device_state)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_events"]
    ) -> ListDeviceEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/client/#get_paginator)
        """
