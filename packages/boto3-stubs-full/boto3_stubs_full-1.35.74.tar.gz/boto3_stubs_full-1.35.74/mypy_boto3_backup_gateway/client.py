"""
Type annotations for backup-gateway service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_backup_gateway.client import BackupGatewayClient

    session = Session()
    client: BackupGatewayClient = session.client("backup-gateway")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListGatewaysPaginator, ListHypervisorsPaginator, ListVirtualMachinesPaginator
from .type_defs import (
    AssociateGatewayToServerInputRequestTypeDef,
    AssociateGatewayToServerOutputTypeDef,
    CreateGatewayInputRequestTypeDef,
    CreateGatewayOutputTypeDef,
    DeleteGatewayInputRequestTypeDef,
    DeleteGatewayOutputTypeDef,
    DeleteHypervisorInputRequestTypeDef,
    DeleteHypervisorOutputTypeDef,
    DisassociateGatewayFromServerInputRequestTypeDef,
    DisassociateGatewayFromServerOutputTypeDef,
    GetBandwidthRateLimitScheduleInputRequestTypeDef,
    GetBandwidthRateLimitScheduleOutputTypeDef,
    GetGatewayInputRequestTypeDef,
    GetGatewayOutputTypeDef,
    GetHypervisorInputRequestTypeDef,
    GetHypervisorOutputTypeDef,
    GetHypervisorPropertyMappingsInputRequestTypeDef,
    GetHypervisorPropertyMappingsOutputTypeDef,
    GetVirtualMachineInputRequestTypeDef,
    GetVirtualMachineOutputTypeDef,
    ImportHypervisorConfigurationInputRequestTypeDef,
    ImportHypervisorConfigurationOutputTypeDef,
    ListGatewaysInputRequestTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsInputRequestTypeDef,
    ListHypervisorsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualMachinesInputRequestTypeDef,
    ListVirtualMachinesOutputTypeDef,
    PutBandwidthRateLimitScheduleInputRequestTypeDef,
    PutBandwidthRateLimitScheduleOutputTypeDef,
    PutHypervisorPropertyMappingsInputRequestTypeDef,
    PutHypervisorPropertyMappingsOutputTypeDef,
    PutMaintenanceStartTimeInputRequestTypeDef,
    PutMaintenanceStartTimeOutputTypeDef,
    StartVirtualMachinesMetadataSyncInputRequestTypeDef,
    StartVirtualMachinesMetadataSyncOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TagResourceOutputTypeDef,
    TestHypervisorConfigurationInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UntagResourceOutputTypeDef,
    UpdateGatewayInformationInputRequestTypeDef,
    UpdateGatewayInformationOutputTypeDef,
    UpdateGatewaySoftwareNowInputRequestTypeDef,
    UpdateGatewaySoftwareNowOutputTypeDef,
    UpdateHypervisorInputRequestTypeDef,
    UpdateHypervisorOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BackupGatewayClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BackupGatewayClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#close)
        """

    def associate_gateway_to_server(
        self, **kwargs: Unpack[AssociateGatewayToServerInputRequestTypeDef]
    ) -> AssociateGatewayToServerOutputTypeDef:
        """
        Associates a backup gateway with your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/associate_gateway_to_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#associate_gateway_to_server)
        """

    def create_gateway(
        self, **kwargs: Unpack[CreateGatewayInputRequestTypeDef]
    ) -> CreateGatewayOutputTypeDef:
        """
        Creates a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/create_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#create_gateway)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayInputRequestTypeDef]
    ) -> DeleteGatewayOutputTypeDef:
        """
        Deletes a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/delete_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#delete_gateway)
        """

    def delete_hypervisor(
        self, **kwargs: Unpack[DeleteHypervisorInputRequestTypeDef]
    ) -> DeleteHypervisorOutputTypeDef:
        """
        Deletes a hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/delete_hypervisor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#delete_hypervisor)
        """

    def disassociate_gateway_from_server(
        self, **kwargs: Unpack[DisassociateGatewayFromServerInputRequestTypeDef]
    ) -> DisassociateGatewayFromServerOutputTypeDef:
        """
        Disassociates a backup gateway from the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/disassociate_gateway_from_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#disassociate_gateway_from_server)
        """

    def get_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[GetBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> GetBandwidthRateLimitScheduleOutputTypeDef:
        """
        Retrieves the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_bandwidth_rate_limit_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_bandwidth_rate_limit_schedule)
        """

    def get_gateway(
        self, **kwargs: Unpack[GetGatewayInputRequestTypeDef]
    ) -> GetGatewayOutputTypeDef:
        """
        By providing the ARN (Amazon Resource Name), this API returns the gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_gateway)
        """

    def get_hypervisor(
        self, **kwargs: Unpack[GetHypervisorInputRequestTypeDef]
    ) -> GetHypervisorOutputTypeDef:
        """
        This action requests information about the specified hypervisor to which the
        gateway will connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_hypervisor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_hypervisor)
        """

    def get_hypervisor_property_mappings(
        self, **kwargs: Unpack[GetHypervisorPropertyMappingsInputRequestTypeDef]
    ) -> GetHypervisorPropertyMappingsOutputTypeDef:
        """
        This action retrieves the property mappings for the specified hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_hypervisor_property_mappings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_hypervisor_property_mappings)
        """

    def get_virtual_machine(
        self, **kwargs: Unpack[GetVirtualMachineInputRequestTypeDef]
    ) -> GetVirtualMachineOutputTypeDef:
        """
        By providing the ARN (Amazon Resource Name), this API returns the virtual
        machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_virtual_machine.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_virtual_machine)
        """

    def import_hypervisor_configuration(
        self, **kwargs: Unpack[ImportHypervisorConfigurationInputRequestTypeDef]
    ) -> ImportHypervisorConfigurationOutputTypeDef:
        """
        Connect to a hypervisor by importing its configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/import_hypervisor_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#import_hypervisor_configuration)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysInputRequestTypeDef]
    ) -> ListGatewaysOutputTypeDef:
        """
        Lists backup gateways owned by an Amazon Web Services account in an Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/list_gateways.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#list_gateways)
        """

    def list_hypervisors(
        self, **kwargs: Unpack[ListHypervisorsInputRequestTypeDef]
    ) -> ListHypervisorsOutputTypeDef:
        """
        Lists your hypervisors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/list_hypervisors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#list_hypervisors)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags applied to the resource identified by its Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#list_tags_for_resource)
        """

    def list_virtual_machines(
        self, **kwargs: Unpack[ListVirtualMachinesInputRequestTypeDef]
    ) -> ListVirtualMachinesOutputTypeDef:
        """
        Lists your virtual machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/list_virtual_machines.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#list_virtual_machines)
        """

    def put_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[PutBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> PutBandwidthRateLimitScheduleOutputTypeDef:
        """
        This action sets the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/put_bandwidth_rate_limit_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#put_bandwidth_rate_limit_schedule)
        """

    def put_hypervisor_property_mappings(
        self, **kwargs: Unpack[PutHypervisorPropertyMappingsInputRequestTypeDef]
    ) -> PutHypervisorPropertyMappingsOutputTypeDef:
        """
        This action sets the property mappings for the specified hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/put_hypervisor_property_mappings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#put_hypervisor_property_mappings)
        """

    def put_maintenance_start_time(
        self, **kwargs: Unpack[PutMaintenanceStartTimeInputRequestTypeDef]
    ) -> PutMaintenanceStartTimeOutputTypeDef:
        """
        Set the maintenance start time for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/put_maintenance_start_time.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#put_maintenance_start_time)
        """

    def start_virtual_machines_metadata_sync(
        self, **kwargs: Unpack[StartVirtualMachinesMetadataSyncInputRequestTypeDef]
    ) -> StartVirtualMachinesMetadataSyncOutputTypeDef:
        """
        This action sends a request to sync metadata across the specified virtual
        machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/start_virtual_machines_metadata_sync.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#start_virtual_machines_metadata_sync)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> TagResourceOutputTypeDef:
        """
        Tag the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#tag_resource)
        """

    def test_hypervisor_configuration(
        self, **kwargs: Unpack[TestHypervisorConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Tests your hypervisor configuration to validate that backup gateway can connect
        with the hypervisor and its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/test_hypervisor_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#test_hypervisor_configuration)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> UntagResourceOutputTypeDef:
        """
        Removes tags from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#untag_resource)
        """

    def update_gateway_information(
        self, **kwargs: Unpack[UpdateGatewayInformationInputRequestTypeDef]
    ) -> UpdateGatewayInformationOutputTypeDef:
        """
        Updates a gateway's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/update_gateway_information.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#update_gateway_information)
        """

    def update_gateway_software_now(
        self, **kwargs: Unpack[UpdateGatewaySoftwareNowInputRequestTypeDef]
    ) -> UpdateGatewaySoftwareNowOutputTypeDef:
        """
        Updates the gateway virtual machine (VM) software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/update_gateway_software_now.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#update_gateway_software_now)
        """

    def update_hypervisor(
        self, **kwargs: Unpack[UpdateHypervisorInputRequestTypeDef]
    ) -> UpdateHypervisorOutputTypeDef:
        """
        Updates a hypervisor metadata, including its host, username, and password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/update_hypervisor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#update_hypervisor)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hypervisors"]
    ) -> ListHypervisorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_machines"]
    ) -> ListVirtualMachinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/client/#get_paginator)
        """
