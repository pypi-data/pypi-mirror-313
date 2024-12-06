"""
Type annotations for connectcampaignsv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connectcampaignsv2.client import ConnectCampaignServiceV2Client

    session = Session()
    client: ConnectCampaignServiceV2Client = session.client("connectcampaignsv2")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListCampaignsPaginator, ListConnectInstanceIntegrationsPaginator
from .type_defs import (
    CreateCampaignRequestRequestTypeDef,
    CreateCampaignResponseTypeDef,
    DeleteCampaignChannelSubtypeConfigRequestRequestTypeDef,
    DeleteCampaignCommunicationLimitsRequestRequestTypeDef,
    DeleteCampaignCommunicationTimeRequestRequestTypeDef,
    DeleteCampaignRequestRequestTypeDef,
    DeleteConnectInstanceConfigRequestRequestTypeDef,
    DeleteConnectInstanceIntegrationRequestRequestTypeDef,
    DeleteInstanceOnboardingJobRequestRequestTypeDef,
    DescribeCampaignRequestRequestTypeDef,
    DescribeCampaignResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCampaignStateBatchRequestRequestTypeDef,
    GetCampaignStateBatchResponseTypeDef,
    GetCampaignStateRequestRequestTypeDef,
    GetCampaignStateResponseTypeDef,
    GetConnectInstanceConfigRequestRequestTypeDef,
    GetConnectInstanceConfigResponseTypeDef,
    GetInstanceOnboardingJobStatusRequestRequestTypeDef,
    GetInstanceOnboardingJobStatusResponseTypeDef,
    ListCampaignsRequestRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListConnectInstanceIntegrationsRequestRequestTypeDef,
    ListConnectInstanceIntegrationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PauseCampaignRequestRequestTypeDef,
    PutConnectInstanceIntegrationRequestRequestTypeDef,
    PutOutboundRequestBatchRequestRequestTypeDef,
    PutOutboundRequestBatchResponseTypeDef,
    PutProfileOutboundRequestBatchRequestRequestTypeDef,
    PutProfileOutboundRequestBatchResponseTypeDef,
    ResumeCampaignRequestRequestTypeDef,
    StartCampaignRequestRequestTypeDef,
    StartInstanceOnboardingJobRequestRequestTypeDef,
    StartInstanceOnboardingJobResponseTypeDef,
    StopCampaignRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCampaignChannelSubtypeConfigRequestRequestTypeDef,
    UpdateCampaignCommunicationLimitsRequestRequestTypeDef,
    UpdateCampaignCommunicationTimeRequestRequestTypeDef,
    UpdateCampaignFlowAssociationRequestRequestTypeDef,
    UpdateCampaignNameRequestRequestTypeDef,
    UpdateCampaignScheduleRequestRequestTypeDef,
    UpdateCampaignSourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ConnectCampaignServiceV2Client",)

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
    InvalidCampaignStateException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ConnectCampaignServiceV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCampaignServiceV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#close)
        """

    def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/create_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#create_campaign)
        """

    def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a campaign from the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_campaign)
        """

    def delete_campaign_channel_subtype_config(
        self, **kwargs: Unpack[DeleteCampaignChannelSubtypeConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the channel subtype config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_channel_subtype_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_campaign_channel_subtype_config)
        """

    def delete_campaign_communication_limits(
        self, **kwargs: Unpack[DeleteCampaignCommunicationLimitsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the communication limits config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_communication_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_campaign_communication_limits)
        """

    def delete_campaign_communication_time(
        self, **kwargs: Unpack[DeleteCampaignCommunicationTimeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the communication time config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_communication_time.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_campaign_communication_time)
        """

    def delete_connect_instance_config(
        self, **kwargs: Unpack[DeleteConnectInstanceConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connect instance config from the specified AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_connect_instance_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_connect_instance_config)
        """

    def delete_connect_instance_integration(
        self, **kwargs: Unpack[DeleteConnectInstanceIntegrationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the integration for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_connect_instance_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_connect_instance_integration)
        """

    def delete_instance_onboarding_job(
        self, **kwargs: Unpack[DeleteInstanceOnboardingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the Connect Campaigns onboarding job for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_instance_onboarding_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#delete_instance_onboarding_job)
        """

    def describe_campaign(
        self, **kwargs: Unpack[DescribeCampaignRequestRequestTypeDef]
    ) -> DescribeCampaignResponseTypeDef:
        """
        Describes the specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/describe_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#describe_campaign)
        """

    def get_campaign_state(
        self, **kwargs: Unpack[GetCampaignStateRequestRequestTypeDef]
    ) -> GetCampaignStateResponseTypeDef:
        """
        Get state of a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_campaign_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_campaign_state)
        """

    def get_campaign_state_batch(
        self, **kwargs: Unpack[GetCampaignStateBatchRequestRequestTypeDef]
    ) -> GetCampaignStateBatchResponseTypeDef:
        """
        Get state of campaigns for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_campaign_state_batch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_campaign_state_batch)
        """

    def get_connect_instance_config(
        self, **kwargs: Unpack[GetConnectInstanceConfigRequestRequestTypeDef]
    ) -> GetConnectInstanceConfigResponseTypeDef:
        """
        Get the specific Connect instance config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_connect_instance_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_connect_instance_config)
        """

    def get_instance_onboarding_job_status(
        self, **kwargs: Unpack[GetInstanceOnboardingJobStatusRequestRequestTypeDef]
    ) -> GetInstanceOnboardingJobStatusResponseTypeDef:
        """
        Get the specific instance onboarding job status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_instance_onboarding_job_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_instance_onboarding_job_status)
        """

    def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Provides summary information about the campaigns under the specified Amazon
        Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_campaigns.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#list_campaigns)
        """

    def list_connect_instance_integrations(
        self, **kwargs: Unpack[ListConnectInstanceIntegrationsRequestRequestTypeDef]
    ) -> ListConnectInstanceIntegrationsResponseTypeDef:
        """
        Provides summary information about the integration under the specified Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_connect_instance_integrations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#list_connect_instance_integrations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#list_tags_for_resource)
        """

    def pause_campaign(
        self, **kwargs: Unpack[PauseCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Pauses a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/pause_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#pause_campaign)
        """

    def put_connect_instance_integration(
        self, **kwargs: Unpack[PutConnectInstanceIntegrationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Put or update the integration for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_connect_instance_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#put_connect_instance_integration)
        """

    def put_outbound_request_batch(
        self, **kwargs: Unpack[PutOutboundRequestBatchRequestRequestTypeDef]
    ) -> PutOutboundRequestBatchResponseTypeDef:
        """
        Creates outbound requests for the specified campaign Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_outbound_request_batch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#put_outbound_request_batch)
        """

    def put_profile_outbound_request_batch(
        self, **kwargs: Unpack[PutProfileOutboundRequestBatchRequestRequestTypeDef]
    ) -> PutProfileOutboundRequestBatchResponseTypeDef:
        """
        Takes in a list of profile outbound requests to be placed as part of an
        outbound campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_profile_outbound_request_batch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#put_profile_outbound_request_batch)
        """

    def resume_campaign(
        self, **kwargs: Unpack[ResumeCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/resume_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#resume_campaign)
        """

    def start_campaign(
        self, **kwargs: Unpack[StartCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/start_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#start_campaign)
        """

    def start_instance_onboarding_job(
        self, **kwargs: Unpack[StartInstanceOnboardingJobRequestRequestTypeDef]
    ) -> StartInstanceOnboardingJobResponseTypeDef:
        """
        Onboard the specific Amazon Connect instance to Connect Campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/start_instance_onboarding_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#start_instance_onboarding_job)
        """

    def stop_campaign(
        self, **kwargs: Unpack[StopCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/stop_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#stop_campaign)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#untag_resource)
        """

    def update_campaign_channel_subtype_config(
        self, **kwargs: Unpack[UpdateCampaignChannelSubtypeConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the channel subtype config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_channel_subtype_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_channel_subtype_config)
        """

    def update_campaign_communication_limits(
        self, **kwargs: Unpack[UpdateCampaignCommunicationLimitsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the communication limits config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_communication_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_communication_limits)
        """

    def update_campaign_communication_time(
        self, **kwargs: Unpack[UpdateCampaignCommunicationTimeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the communication time config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_communication_time.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_communication_time)
        """

    def update_campaign_flow_association(
        self, **kwargs: Unpack[UpdateCampaignFlowAssociationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the campaign flow associated with a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_flow_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_flow_association)
        """

    def update_campaign_name(
        self, **kwargs: Unpack[UpdateCampaignNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_name)
        """

    def update_campaign_schedule(
        self, **kwargs: Unpack[UpdateCampaignScheduleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the schedule for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_schedule)
        """

    def update_campaign_source(
        self, **kwargs: Unpack[UpdateCampaignSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the campaign source with a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#update_campaign_source)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_campaigns"]) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connect_instance_integrations"]
    ) -> ListConnectInstanceIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaignsv2/client/#get_paginator)
        """
