"""
Type annotations for pinpoint service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pinpoint.client import PinpointClient

    session = Session()
    client: PinpointClient = session.client("pinpoint")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateAppRequestRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateCampaignRequestRequestTypeDef,
    CreateCampaignResponseTypeDef,
    CreateEmailTemplateRequestRequestTypeDef,
    CreateEmailTemplateResponseTypeDef,
    CreateExportJobRequestRequestTypeDef,
    CreateExportJobResponseTypeDef,
    CreateImportJobRequestRequestTypeDef,
    CreateImportJobResponseTypeDef,
    CreateInAppTemplateRequestRequestTypeDef,
    CreateInAppTemplateResponseTypeDef,
    CreateJourneyRequestRequestTypeDef,
    CreateJourneyResponseTypeDef,
    CreatePushTemplateRequestRequestTypeDef,
    CreatePushTemplateResponseTypeDef,
    CreateRecommenderConfigurationRequestRequestTypeDef,
    CreateRecommenderConfigurationResponseTypeDef,
    CreateSegmentRequestRequestTypeDef,
    CreateSegmentResponseTypeDef,
    CreateSmsTemplateRequestRequestTypeDef,
    CreateSmsTemplateResponseTypeDef,
    CreateVoiceTemplateRequestRequestTypeDef,
    CreateVoiceTemplateResponseTypeDef,
    DeleteAdmChannelRequestRequestTypeDef,
    DeleteAdmChannelResponseTypeDef,
    DeleteApnsChannelRequestRequestTypeDef,
    DeleteApnsChannelResponseTypeDef,
    DeleteApnsSandboxChannelRequestRequestTypeDef,
    DeleteApnsSandboxChannelResponseTypeDef,
    DeleteApnsVoipChannelRequestRequestTypeDef,
    DeleteApnsVoipChannelResponseTypeDef,
    DeleteApnsVoipSandboxChannelRequestRequestTypeDef,
    DeleteApnsVoipSandboxChannelResponseTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteAppResponseTypeDef,
    DeleteBaiduChannelRequestRequestTypeDef,
    DeleteBaiduChannelResponseTypeDef,
    DeleteCampaignRequestRequestTypeDef,
    DeleteCampaignResponseTypeDef,
    DeleteEmailChannelRequestRequestTypeDef,
    DeleteEmailChannelResponseTypeDef,
    DeleteEmailTemplateRequestRequestTypeDef,
    DeleteEmailTemplateResponseTypeDef,
    DeleteEndpointRequestRequestTypeDef,
    DeleteEndpointResponseTypeDef,
    DeleteEventStreamRequestRequestTypeDef,
    DeleteEventStreamResponseTypeDef,
    DeleteGcmChannelRequestRequestTypeDef,
    DeleteGcmChannelResponseTypeDef,
    DeleteInAppTemplateRequestRequestTypeDef,
    DeleteInAppTemplateResponseTypeDef,
    DeleteJourneyRequestRequestTypeDef,
    DeleteJourneyResponseTypeDef,
    DeletePushTemplateRequestRequestTypeDef,
    DeletePushTemplateResponseTypeDef,
    DeleteRecommenderConfigurationRequestRequestTypeDef,
    DeleteRecommenderConfigurationResponseTypeDef,
    DeleteSegmentRequestRequestTypeDef,
    DeleteSegmentResponseTypeDef,
    DeleteSmsChannelRequestRequestTypeDef,
    DeleteSmsChannelResponseTypeDef,
    DeleteSmsTemplateRequestRequestTypeDef,
    DeleteSmsTemplateResponseTypeDef,
    DeleteUserEndpointsRequestRequestTypeDef,
    DeleteUserEndpointsResponseTypeDef,
    DeleteVoiceChannelRequestRequestTypeDef,
    DeleteVoiceChannelResponseTypeDef,
    DeleteVoiceTemplateRequestRequestTypeDef,
    DeleteVoiceTemplateResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAdmChannelRequestRequestTypeDef,
    GetAdmChannelResponseTypeDef,
    GetApnsChannelRequestRequestTypeDef,
    GetApnsChannelResponseTypeDef,
    GetApnsSandboxChannelRequestRequestTypeDef,
    GetApnsSandboxChannelResponseTypeDef,
    GetApnsVoipChannelRequestRequestTypeDef,
    GetApnsVoipChannelResponseTypeDef,
    GetApnsVoipSandboxChannelRequestRequestTypeDef,
    GetApnsVoipSandboxChannelResponseTypeDef,
    GetApplicationDateRangeKpiRequestRequestTypeDef,
    GetApplicationDateRangeKpiResponseTypeDef,
    GetApplicationSettingsRequestRequestTypeDef,
    GetApplicationSettingsResponseTypeDef,
    GetAppRequestRequestTypeDef,
    GetAppResponseTypeDef,
    GetAppsRequestRequestTypeDef,
    GetAppsResponseTypeDef,
    GetBaiduChannelRequestRequestTypeDef,
    GetBaiduChannelResponseTypeDef,
    GetCampaignActivitiesRequestRequestTypeDef,
    GetCampaignActivitiesResponseTypeDef,
    GetCampaignDateRangeKpiRequestRequestTypeDef,
    GetCampaignDateRangeKpiResponseTypeDef,
    GetCampaignRequestRequestTypeDef,
    GetCampaignResponseTypeDef,
    GetCampaignsRequestRequestTypeDef,
    GetCampaignsResponseTypeDef,
    GetCampaignVersionRequestRequestTypeDef,
    GetCampaignVersionResponseTypeDef,
    GetCampaignVersionsRequestRequestTypeDef,
    GetCampaignVersionsResponseTypeDef,
    GetChannelsRequestRequestTypeDef,
    GetChannelsResponseTypeDef,
    GetEmailChannelRequestRequestTypeDef,
    GetEmailChannelResponseTypeDef,
    GetEmailTemplateRequestRequestTypeDef,
    GetEmailTemplateResponseTypeDef,
    GetEndpointRequestRequestTypeDef,
    GetEndpointResponseTypeDef,
    GetEventStreamRequestRequestTypeDef,
    GetEventStreamResponseTypeDef,
    GetExportJobRequestRequestTypeDef,
    GetExportJobResponseTypeDef,
    GetExportJobsRequestRequestTypeDef,
    GetExportJobsResponseTypeDef,
    GetGcmChannelRequestRequestTypeDef,
    GetGcmChannelResponseTypeDef,
    GetImportJobRequestRequestTypeDef,
    GetImportJobResponseTypeDef,
    GetImportJobsRequestRequestTypeDef,
    GetImportJobsResponseTypeDef,
    GetInAppMessagesRequestRequestTypeDef,
    GetInAppMessagesResponseTypeDef,
    GetInAppTemplateRequestRequestTypeDef,
    GetInAppTemplateResponseTypeDef,
    GetJourneyDateRangeKpiRequestRequestTypeDef,
    GetJourneyDateRangeKpiResponseTypeDef,
    GetJourneyExecutionActivityMetricsRequestRequestTypeDef,
    GetJourneyExecutionActivityMetricsResponseTypeDef,
    GetJourneyExecutionMetricsRequestRequestTypeDef,
    GetJourneyExecutionMetricsResponseTypeDef,
    GetJourneyRequestRequestTypeDef,
    GetJourneyResponseTypeDef,
    GetJourneyRunExecutionActivityMetricsRequestRequestTypeDef,
    GetJourneyRunExecutionActivityMetricsResponseTypeDef,
    GetJourneyRunExecutionMetricsRequestRequestTypeDef,
    GetJourneyRunExecutionMetricsResponseTypeDef,
    GetJourneyRunsRequestRequestTypeDef,
    GetJourneyRunsResponseTypeDef,
    GetPushTemplateRequestRequestTypeDef,
    GetPushTemplateResponseTypeDef,
    GetRecommenderConfigurationRequestRequestTypeDef,
    GetRecommenderConfigurationResponseTypeDef,
    GetRecommenderConfigurationsRequestRequestTypeDef,
    GetRecommenderConfigurationsResponseTypeDef,
    GetSegmentExportJobsRequestRequestTypeDef,
    GetSegmentExportJobsResponseTypeDef,
    GetSegmentImportJobsRequestRequestTypeDef,
    GetSegmentImportJobsResponseTypeDef,
    GetSegmentRequestRequestTypeDef,
    GetSegmentResponseTypeDef,
    GetSegmentsRequestRequestTypeDef,
    GetSegmentsResponseTypeDef,
    GetSegmentVersionRequestRequestTypeDef,
    GetSegmentVersionResponseTypeDef,
    GetSegmentVersionsRequestRequestTypeDef,
    GetSegmentVersionsResponseTypeDef,
    GetSmsChannelRequestRequestTypeDef,
    GetSmsChannelResponseTypeDef,
    GetSmsTemplateRequestRequestTypeDef,
    GetSmsTemplateResponseTypeDef,
    GetUserEndpointsRequestRequestTypeDef,
    GetUserEndpointsResponseTypeDef,
    GetVoiceChannelRequestRequestTypeDef,
    GetVoiceChannelResponseTypeDef,
    GetVoiceTemplateRequestRequestTypeDef,
    GetVoiceTemplateResponseTypeDef,
    ListJourneysRequestRequestTypeDef,
    ListJourneysResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplatesRequestRequestTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsRequestRequestTypeDef,
    ListTemplateVersionsResponseTypeDef,
    PhoneNumberValidateRequestRequestTypeDef,
    PhoneNumberValidateResponseTypeDef,
    PutEventsRequestRequestTypeDef,
    PutEventsResponseTypeDef,
    PutEventStreamRequestRequestTypeDef,
    PutEventStreamResponseTypeDef,
    RemoveAttributesRequestRequestTypeDef,
    RemoveAttributesResponseTypeDef,
    SendMessagesRequestRequestTypeDef,
    SendMessagesResponseTypeDef,
    SendOTPMessageRequestRequestTypeDef,
    SendOTPMessageResponseTypeDef,
    SendUsersMessagesRequestRequestTypeDef,
    SendUsersMessagesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAdmChannelRequestRequestTypeDef,
    UpdateAdmChannelResponseTypeDef,
    UpdateApnsChannelRequestRequestTypeDef,
    UpdateApnsChannelResponseTypeDef,
    UpdateApnsSandboxChannelRequestRequestTypeDef,
    UpdateApnsSandboxChannelResponseTypeDef,
    UpdateApnsVoipChannelRequestRequestTypeDef,
    UpdateApnsVoipChannelResponseTypeDef,
    UpdateApnsVoipSandboxChannelRequestRequestTypeDef,
    UpdateApnsVoipSandboxChannelResponseTypeDef,
    UpdateApplicationSettingsRequestRequestTypeDef,
    UpdateApplicationSettingsResponseTypeDef,
    UpdateBaiduChannelRequestRequestTypeDef,
    UpdateBaiduChannelResponseTypeDef,
    UpdateCampaignRequestRequestTypeDef,
    UpdateCampaignResponseTypeDef,
    UpdateEmailChannelRequestRequestTypeDef,
    UpdateEmailChannelResponseTypeDef,
    UpdateEmailTemplateRequestRequestTypeDef,
    UpdateEmailTemplateResponseTypeDef,
    UpdateEndpointRequestRequestTypeDef,
    UpdateEndpointResponseTypeDef,
    UpdateEndpointsBatchRequestRequestTypeDef,
    UpdateEndpointsBatchResponseTypeDef,
    UpdateGcmChannelRequestRequestTypeDef,
    UpdateGcmChannelResponseTypeDef,
    UpdateInAppTemplateRequestRequestTypeDef,
    UpdateInAppTemplateResponseTypeDef,
    UpdateJourneyRequestRequestTypeDef,
    UpdateJourneyResponseTypeDef,
    UpdateJourneyStateRequestRequestTypeDef,
    UpdateJourneyStateResponseTypeDef,
    UpdatePushTemplateRequestRequestTypeDef,
    UpdatePushTemplateResponseTypeDef,
    UpdateRecommenderConfigurationRequestRequestTypeDef,
    UpdateRecommenderConfigurationResponseTypeDef,
    UpdateSegmentRequestRequestTypeDef,
    UpdateSegmentResponseTypeDef,
    UpdateSmsChannelRequestRequestTypeDef,
    UpdateSmsChannelResponseTypeDef,
    UpdateSmsTemplateRequestRequestTypeDef,
    UpdateSmsTemplateResponseTypeDef,
    UpdateTemplateActiveVersionRequestRequestTypeDef,
    UpdateTemplateActiveVersionResponseTypeDef,
    UpdateVoiceChannelRequestRequestTypeDef,
    UpdateVoiceChannelResponseTypeDef,
    UpdateVoiceTemplateRequestRequestTypeDef,
    UpdateVoiceTemplateResponseTypeDef,
    VerifyOTPMessageRequestRequestTypeDef,
    VerifyOTPMessageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("PinpointClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    PayloadTooLargeException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class PinpointClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#close)
        """

    def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_app)
        """

    def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a new campaign for an application or updates the settings of an
        existing campaign for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_campaign)
        """

    def create_email_template(
        self, **kwargs: Unpack[CreateEmailTemplateRequestRequestTypeDef]
    ) -> CreateEmailTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_email_template)
        """

    def create_export_job(
        self, **kwargs: Unpack[CreateExportJobRequestRequestTypeDef]
    ) -> CreateExportJobResponseTypeDef:
        """
        Creates an export job for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_export_job)
        """

    def create_import_job(
        self, **kwargs: Unpack[CreateImportJobRequestRequestTypeDef]
    ) -> CreateImportJobResponseTypeDef:
        """
        Creates an import job for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_import_job)
        """

    def create_in_app_template(
        self, **kwargs: Unpack[CreateInAppTemplateRequestRequestTypeDef]
    ) -> CreateInAppTemplateResponseTypeDef:
        """
        Creates a new message template for messages using the in-app message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_in_app_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_in_app_template)
        """

    def create_journey(
        self, **kwargs: Unpack[CreateJourneyRequestRequestTypeDef]
    ) -> CreateJourneyResponseTypeDef:
        """
        Creates a journey for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_journey.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_journey)
        """

    def create_push_template(
        self, **kwargs: Unpack[CreatePushTemplateRequestRequestTypeDef]
    ) -> CreatePushTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_push_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_push_template)
        """

    def create_recommender_configuration(
        self, **kwargs: Unpack[CreateRecommenderConfigurationRequestRequestTypeDef]
    ) -> CreateRecommenderConfigurationResponseTypeDef:
        """
        Creates an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_recommender_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_recommender_configuration)
        """

    def create_segment(
        self, **kwargs: Unpack[CreateSegmentRequestRequestTypeDef]
    ) -> CreateSegmentResponseTypeDef:
        """
        Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_segment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_segment)
        """

    def create_sms_template(
        self, **kwargs: Unpack[CreateSmsTemplateRequestRequestTypeDef]
    ) -> CreateSmsTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_sms_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_sms_template)
        """

    def create_voice_template(
        self, **kwargs: Unpack[CreateVoiceTemplateRequestRequestTypeDef]
    ) -> CreateVoiceTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_voice_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#create_voice_template)
        """

    def delete_adm_channel(
        self, **kwargs: Unpack[DeleteAdmChannelRequestRequestTypeDef]
    ) -> DeleteAdmChannelResponseTypeDef:
        """
        Disables the ADM channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_adm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_adm_channel)
        """

    def delete_apns_channel(
        self, **kwargs: Unpack[DeleteApnsChannelRequestRequestTypeDef]
    ) -> DeleteApnsChannelResponseTypeDef:
        """
        Disables the APNs channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_apns_channel)
        """

    def delete_apns_sandbox_channel(
        self, **kwargs: Unpack[DeleteApnsSandboxChannelRequestRequestTypeDef]
    ) -> DeleteApnsSandboxChannelResponseTypeDef:
        """
        Disables the APNs sandbox channel for an application and deletes any existing
        settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_apns_sandbox_channel)
        """

    def delete_apns_voip_channel(
        self, **kwargs: Unpack[DeleteApnsVoipChannelRequestRequestTypeDef]
    ) -> DeleteApnsVoipChannelResponseTypeDef:
        """
        Disables the APNs VoIP channel for an application and deletes any existing
        settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_voip_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_apns_voip_channel)
        """

    def delete_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[DeleteApnsVoipSandboxChannelRequestRequestTypeDef]
    ) -> DeleteApnsVoipSandboxChannelResponseTypeDef:
        """
        Disables the APNs VoIP sandbox channel for an application and deletes any
        existing settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_voip_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_apns_voip_sandbox_channel)
        """

    def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]
    ) -> DeleteAppResponseTypeDef:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_app)
        """

    def delete_baidu_channel(
        self, **kwargs: Unpack[DeleteBaiduChannelRequestRequestTypeDef]
    ) -> DeleteBaiduChannelResponseTypeDef:
        """
        Disables the Baidu channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_baidu_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_baidu_channel)
        """

    def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestRequestTypeDef]
    ) -> DeleteCampaignResponseTypeDef:
        """
        Deletes a campaign from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_campaign)
        """

    def delete_email_channel(
        self, **kwargs: Unpack[DeleteEmailChannelRequestRequestTypeDef]
    ) -> DeleteEmailChannelResponseTypeDef:
        """
        Disables the email channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_email_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_email_channel)
        """

    def delete_email_template(
        self, **kwargs: Unpack[DeleteEmailTemplateRequestRequestTypeDef]
    ) -> DeleteEmailTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the email
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_email_template)
        """

    def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointRequestRequestTypeDef]
    ) -> DeleteEndpointResponseTypeDef:
        """
        Deletes an endpoint from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_endpoint)
        """

    def delete_event_stream(
        self, **kwargs: Unpack[DeleteEventStreamRequestRequestTypeDef]
    ) -> DeleteEventStreamResponseTypeDef:
        """
        Deletes the event stream for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_event_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_event_stream)
        """

    def delete_gcm_channel(
        self, **kwargs: Unpack[DeleteGcmChannelRequestRequestTypeDef]
    ) -> DeleteGcmChannelResponseTypeDef:
        """
        Disables the GCM channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_gcm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_gcm_channel)
        """

    def delete_in_app_template(
        self, **kwargs: Unpack[DeleteInAppTemplateRequestRequestTypeDef]
    ) -> DeleteInAppTemplateResponseTypeDef:
        """
        Deletes a message template for messages sent using the in-app message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_in_app_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_in_app_template)
        """

    def delete_journey(
        self, **kwargs: Unpack[DeleteJourneyRequestRequestTypeDef]
    ) -> DeleteJourneyResponseTypeDef:
        """
        Deletes a journey from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_journey.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_journey)
        """

    def delete_push_template(
        self, **kwargs: Unpack[DeletePushTemplateRequestRequestTypeDef]
    ) -> DeletePushTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_push_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_push_template)
        """

    def delete_recommender_configuration(
        self, **kwargs: Unpack[DeleteRecommenderConfigurationRequestRequestTypeDef]
    ) -> DeleteRecommenderConfigurationResponseTypeDef:
        """
        Deletes an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_recommender_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_recommender_configuration)
        """

    def delete_segment(
        self, **kwargs: Unpack[DeleteSegmentRequestRequestTypeDef]
    ) -> DeleteSegmentResponseTypeDef:
        """
        Deletes a segment from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_segment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_segment)
        """

    def delete_sms_channel(
        self, **kwargs: Unpack[DeleteSmsChannelRequestRequestTypeDef]
    ) -> DeleteSmsChannelResponseTypeDef:
        """
        Disables the SMS channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_sms_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_sms_channel)
        """

    def delete_sms_template(
        self, **kwargs: Unpack[DeleteSmsTemplateRequestRequestTypeDef]
    ) -> DeleteSmsTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_sms_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_sms_template)
        """

    def delete_user_endpoints(
        self, **kwargs: Unpack[DeleteUserEndpointsRequestRequestTypeDef]
    ) -> DeleteUserEndpointsResponseTypeDef:
        """
        Deletes all the endpoints that are associated with a specific user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_user_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_user_endpoints)
        """

    def delete_voice_channel(
        self, **kwargs: Unpack[DeleteVoiceChannelRequestRequestTypeDef]
    ) -> DeleteVoiceChannelResponseTypeDef:
        """
        Disables the voice channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_voice_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_voice_channel)
        """

    def delete_voice_template(
        self, **kwargs: Unpack[DeleteVoiceTemplateRequestRequestTypeDef]
    ) -> DeleteVoiceTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the voice
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_voice_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#delete_voice_template)
        """

    def get_adm_channel(
        self, **kwargs: Unpack[GetAdmChannelRequestRequestTypeDef]
    ) -> GetAdmChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the ADM channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_adm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_adm_channel)
        """

    def get_apns_channel(
        self, **kwargs: Unpack[GetApnsChannelRequestRequestTypeDef]
    ) -> GetApnsChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_apns_channel)
        """

    def get_apns_sandbox_channel(
        self, **kwargs: Unpack[GetApnsSandboxChannelRequestRequestTypeDef]
    ) -> GetApnsSandboxChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs sandbox channel
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_apns_sandbox_channel)
        """

    def get_apns_voip_channel(
        self, **kwargs: Unpack[GetApnsVoipChannelRequestRequestTypeDef]
    ) -> GetApnsVoipChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs VoIP channel
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_voip_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_apns_voip_channel)
        """

    def get_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[GetApnsVoipSandboxChannelRequestRequestTypeDef]
    ) -> GetApnsVoipSandboxChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs VoIP sandbox
        channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_voip_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_apns_voip_sandbox_channel)
        """

    def get_app(self, **kwargs: Unpack[GetAppRequestRequestTypeDef]) -> GetAppResponseTypeDef:
        """
        Retrieves information about an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_app.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_app)
        """

    def get_application_date_range_kpi(
        self, **kwargs: Unpack[GetApplicationDateRangeKpiRequestRequestTypeDef]
    ) -> GetApplicationDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard metric that applies to
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_application_date_range_kpi.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_application_date_range_kpi)
        """

    def get_application_settings(
        self, **kwargs: Unpack[GetApplicationSettingsRequestRequestTypeDef]
    ) -> GetApplicationSettingsResponseTypeDef:
        """
        Retrieves information about the settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_application_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_application_settings)
        """

    def get_apps(self, **kwargs: Unpack[GetAppsRequestRequestTypeDef]) -> GetAppsResponseTypeDef:
        """
        Retrieves information about all the applications that are associated with your
        Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apps.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_apps)
        """

    def get_baidu_channel(
        self, **kwargs: Unpack[GetBaiduChannelRequestRequestTypeDef]
    ) -> GetBaiduChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the Baidu channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_baidu_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_baidu_channel)
        """

    def get_campaign(
        self, **kwargs: Unpack[GetCampaignRequestRequestTypeDef]
    ) -> GetCampaignResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaign)
        """

    def get_campaign_activities(
        self, **kwargs: Unpack[GetCampaignActivitiesRequestRequestTypeDef]
    ) -> GetCampaignActivitiesResponseTypeDef:
        """
        Retrieves information about all the activities for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_activities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaign_activities)
        """

    def get_campaign_date_range_kpi(
        self, **kwargs: Unpack[GetCampaignDateRangeKpiRequestRequestTypeDef]
    ) -> GetCampaignDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard metric that applies to a
        campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_date_range_kpi.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaign_date_range_kpi)
        """

    def get_campaign_version(
        self, **kwargs: Unpack[GetCampaignVersionRequestRequestTypeDef]
    ) -> GetCampaignVersionResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        specific version of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaign_version)
        """

    def get_campaign_versions(
        self, **kwargs: Unpack[GetCampaignVersionsRequestRequestTypeDef]
    ) -> GetCampaignVersionsResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all versions of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaign_versions)
        """

    def get_campaigns(
        self, **kwargs: Unpack[GetCampaignsRequestRequestTypeDef]
    ) -> GetCampaignsResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all the campaigns that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaigns.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_campaigns)
        """

    def get_channels(
        self, **kwargs: Unpack[GetChannelsRequestRequestTypeDef]
    ) -> GetChannelsResponseTypeDef:
        """
        Retrieves information about the history and status of each channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_channels)
        """

    def get_email_channel(
        self, **kwargs: Unpack[GetEmailChannelRequestRequestTypeDef]
    ) -> GetEmailChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the email channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_email_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_email_channel)
        """

    def get_email_template(
        self, **kwargs: Unpack[GetEmailTemplateRequestRequestTypeDef]
    ) -> GetEmailTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_email_template)
        """

    def get_endpoint(
        self, **kwargs: Unpack[GetEndpointRequestRequestTypeDef]
    ) -> GetEndpointResponseTypeDef:
        """
        Retrieves information about the settings and attributes of a specific endpoint
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_endpoint)
        """

    def get_event_stream(
        self, **kwargs: Unpack[GetEventStreamRequestRequestTypeDef]
    ) -> GetEventStreamResponseTypeDef:
        """
        Retrieves information about the event stream settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_event_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_event_stream)
        """

    def get_export_job(
        self, **kwargs: Unpack[GetExportJobRequestRequestTypeDef]
    ) -> GetExportJobResponseTypeDef:
        """
        Retrieves information about the status and settings of a specific export job
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_export_job)
        """

    def get_export_jobs(
        self, **kwargs: Unpack[GetExportJobsRequestRequestTypeDef]
    ) -> GetExportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of all the export jobs for
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_export_jobs)
        """

    def get_gcm_channel(
        self, **kwargs: Unpack[GetGcmChannelRequestRequestTypeDef]
    ) -> GetGcmChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the GCM channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_gcm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_gcm_channel)
        """

    def get_import_job(
        self, **kwargs: Unpack[GetImportJobRequestRequestTypeDef]
    ) -> GetImportJobResponseTypeDef:
        """
        Retrieves information about the status and settings of a specific import job
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_import_job)
        """

    def get_import_jobs(
        self, **kwargs: Unpack[GetImportJobsRequestRequestTypeDef]
    ) -> GetImportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of all the import jobs for
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_import_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_import_jobs)
        """

    def get_in_app_messages(
        self, **kwargs: Unpack[GetInAppMessagesRequestRequestTypeDef]
    ) -> GetInAppMessagesResponseTypeDef:
        """
        Retrieves the in-app messages targeted for the provided endpoint ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_in_app_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_in_app_messages)
        """

    def get_in_app_template(
        self, **kwargs: Unpack[GetInAppTemplateRequestRequestTypeDef]
    ) -> GetInAppTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages sent
        through the in-app channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_in_app_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_in_app_template)
        """

    def get_journey(
        self, **kwargs: Unpack[GetJourneyRequestRequestTypeDef]
    ) -> GetJourneyResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey)
        """

    def get_journey_date_range_kpi(
        self, **kwargs: Unpack[GetJourneyDateRangeKpiRequestRequestTypeDef]
    ) -> GetJourneyDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard engagement metric that
        applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_date_range_kpi.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_date_range_kpi)
        """

    def get_journey_execution_activity_metrics(
        self, **kwargs: Unpack[GetJourneyExecutionActivityMetricsRequestRequestTypeDef]
    ) -> GetJourneyExecutionActivityMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard execution metric that
        applies to a journey activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_execution_activity_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_execution_activity_metrics)
        """

    def get_journey_execution_metrics(
        self, **kwargs: Unpack[GetJourneyExecutionMetricsRequestRequestTypeDef]
    ) -> GetJourneyExecutionMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard execution metric that
        applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_execution_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_execution_metrics)
        """

    def get_journey_run_execution_activity_metrics(
        self, **kwargs: Unpack[GetJourneyRunExecutionActivityMetricsRequestRequestTypeDef]
    ) -> GetJourneyRunExecutionActivityMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard run execution metric
        that applies to a journey activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_run_execution_activity_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_run_execution_activity_metrics)
        """

    def get_journey_run_execution_metrics(
        self, **kwargs: Unpack[GetJourneyRunExecutionMetricsRequestRequestTypeDef]
    ) -> GetJourneyRunExecutionMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard run execution metric
        that applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_run_execution_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_run_execution_metrics)
        """

    def get_journey_runs(
        self, **kwargs: Unpack[GetJourneyRunsRequestRequestTypeDef]
    ) -> GetJourneyRunsResponseTypeDef:
        """
        Provides information about the runs of a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_journey_runs)
        """

    def get_push_template(
        self, **kwargs: Unpack[GetPushTemplateRequestRequestTypeDef]
    ) -> GetPushTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through a push notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_push_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_push_template)
        """

    def get_recommender_configuration(
        self, **kwargs: Unpack[GetRecommenderConfigurationRequestRequestTypeDef]
    ) -> GetRecommenderConfigurationResponseTypeDef:
        """
        Retrieves information about an Amazon Pinpoint configuration for a recommender
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_recommender_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_recommender_configuration)
        """

    def get_recommender_configurations(
        self, **kwargs: Unpack[GetRecommenderConfigurationsRequestRequestTypeDef]
    ) -> GetRecommenderConfigurationsResponseTypeDef:
        """
        Retrieves information about all the recommender model configurations that are
        associated with your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_recommender_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_recommender_configurations)
        """

    def get_segment(
        self, **kwargs: Unpack[GetSegmentRequestRequestTypeDef]
    ) -> GetSegmentResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for a specific segment that's associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segment)
        """

    def get_segment_export_jobs(
        self, **kwargs: Unpack[GetSegmentExportJobsRequestRequestTypeDef]
    ) -> GetSegmentExportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of the export jobs for a
        segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segment_export_jobs)
        """

    def get_segment_import_jobs(
        self, **kwargs: Unpack[GetSegmentImportJobsRequestRequestTypeDef]
    ) -> GetSegmentImportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of the import jobs for a
        segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_import_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segment_import_jobs)
        """

    def get_segment_version(
        self, **kwargs: Unpack[GetSegmentVersionRequestRequestTypeDef]
    ) -> GetSegmentVersionResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for a specific version of a segment that's associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segment_version)
        """

    def get_segment_versions(
        self, **kwargs: Unpack[GetSegmentVersionsRequestRequestTypeDef]
    ) -> GetSegmentVersionsResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for all the versions of a specific segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segment_versions)
        """

    def get_segments(
        self, **kwargs: Unpack[GetSegmentsRequestRequestTypeDef]
    ) -> GetSegmentsResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for all the segments that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_segments)
        """

    def get_sms_channel(
        self, **kwargs: Unpack[GetSmsChannelRequestRequestTypeDef]
    ) -> GetSmsChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the SMS channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_sms_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_sms_channel)
        """

    def get_sms_template(
        self, **kwargs: Unpack[GetSmsTemplateRequestRequestTypeDef]
    ) -> GetSmsTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_sms_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_sms_template)
        """

    def get_user_endpoints(
        self, **kwargs: Unpack[GetUserEndpointsRequestRequestTypeDef]
    ) -> GetUserEndpointsResponseTypeDef:
        """
        Retrieves information about all the endpoints that are associated with a
        specific user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_user_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_user_endpoints)
        """

    def get_voice_channel(
        self, **kwargs: Unpack[GetVoiceChannelRequestRequestTypeDef]
    ) -> GetVoiceChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the voice channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_voice_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_voice_channel)
        """

    def get_voice_template(
        self, **kwargs: Unpack[GetVoiceTemplateRequestRequestTypeDef]
    ) -> GetVoiceTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_voice_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#get_voice_template)
        """

    def list_journeys(
        self, **kwargs: Unpack[ListJourneysRequestRequestTypeDef]
    ) -> ListJourneysResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all the journeys that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_journeys.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#list_journeys)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all the tags (keys and values) that are associated with an
        application, campaign, message template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#list_tags_for_resource)
        """

    def list_template_versions(
        self, **kwargs: Unpack[ListTemplateVersionsRequestRequestTypeDef]
    ) -> ListTemplateVersionsResponseTypeDef:
        """
        Retrieves information about all the versions of a specific message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_template_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#list_template_versions)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Retrieves information about all the message templates that are associated with
        your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#list_templates)
        """

    def phone_number_validate(
        self, **kwargs: Unpack[PhoneNumberValidateRequestRequestTypeDef]
    ) -> PhoneNumberValidateResponseTypeDef:
        """
        Retrieves information about a phone number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/phone_number_validate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#phone_number_validate)
        """

    def put_event_stream(
        self, **kwargs: Unpack[PutEventStreamRequestRequestTypeDef]
    ) -> PutEventStreamResponseTypeDef:
        """
        Creates a new event stream for an application or updates the settings of an
        existing event stream for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/put_event_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#put_event_stream)
        """

    def put_events(
        self, **kwargs: Unpack[PutEventsRequestRequestTypeDef]
    ) -> PutEventsResponseTypeDef:
        """
        Creates a new event to record for endpoints, or creates or updates endpoint
        data that existing events are associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/put_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#put_events)
        """

    def remove_attributes(
        self, **kwargs: Unpack[RemoveAttributesRequestRequestTypeDef]
    ) -> RemoveAttributesResponseTypeDef:
        """
        Removes one or more custom attributes, of the same attribute type, from the
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/remove_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#remove_attributes)
        """

    def send_messages(
        self, **kwargs: Unpack[SendMessagesRequestRequestTypeDef]
    ) -> SendMessagesResponseTypeDef:
        """
        Creates and sends a direct message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#send_messages)
        """

    def send_otp_message(
        self, **kwargs: Unpack[SendOTPMessageRequestRequestTypeDef]
    ) -> SendOTPMessageResponseTypeDef:
        """
        Send an OTP message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_otp_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#send_otp_message)
        """

    def send_users_messages(
        self, **kwargs: Unpack[SendUsersMessagesRequestRequestTypeDef]
    ) -> SendUsersMessagesResponseTypeDef:
        """
        Creates and sends a message to a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_users_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#send_users_messages)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags (keys and values) to an application, campaign, message
        template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags (keys and values) from an application, campaign,
        message template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#untag_resource)
        """

    def update_adm_channel(
        self, **kwargs: Unpack[UpdateAdmChannelRequestRequestTypeDef]
    ) -> UpdateAdmChannelResponseTypeDef:
        """
        Enables the ADM channel for an application or updates the status and settings
        of the ADM channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_adm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_adm_channel)
        """

    def update_apns_channel(
        self, **kwargs: Unpack[UpdateApnsChannelRequestRequestTypeDef]
    ) -> UpdateApnsChannelResponseTypeDef:
        """
        Enables the APNs channel for an application or updates the status and settings
        of the APNs channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_apns_channel)
        """

    def update_apns_sandbox_channel(
        self, **kwargs: Unpack[UpdateApnsSandboxChannelRequestRequestTypeDef]
    ) -> UpdateApnsSandboxChannelResponseTypeDef:
        """
        Enables the APNs sandbox channel for an application or updates the status and
        settings of the APNs sandbox channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_apns_sandbox_channel)
        """

    def update_apns_voip_channel(
        self, **kwargs: Unpack[UpdateApnsVoipChannelRequestRequestTypeDef]
    ) -> UpdateApnsVoipChannelResponseTypeDef:
        """
        Enables the APNs VoIP channel for an application or updates the status and
        settings of the APNs VoIP channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_voip_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_apns_voip_channel)
        """

    def update_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[UpdateApnsVoipSandboxChannelRequestRequestTypeDef]
    ) -> UpdateApnsVoipSandboxChannelResponseTypeDef:
        """
        Enables the APNs VoIP sandbox channel for an application or updates the status
        and settings of the APNs VoIP sandbox channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_voip_sandbox_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_apns_voip_sandbox_channel)
        """

    def update_application_settings(
        self, **kwargs: Unpack[UpdateApplicationSettingsRequestRequestTypeDef]
    ) -> UpdateApplicationSettingsResponseTypeDef:
        """
        Updates the settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_application_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_application_settings)
        """

    def update_baidu_channel(
        self, **kwargs: Unpack[UpdateBaiduChannelRequestRequestTypeDef]
    ) -> UpdateBaiduChannelResponseTypeDef:
        """
        Enables the Baidu channel for an application or updates the status and settings
        of the Baidu channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_baidu_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_baidu_channel)
        """

    def update_campaign(
        self, **kwargs: Unpack[UpdateCampaignRequestRequestTypeDef]
    ) -> UpdateCampaignResponseTypeDef:
        """
        Updates the configuration and other settings for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_campaign)
        """

    def update_email_channel(
        self, **kwargs: Unpack[UpdateEmailChannelRequestRequestTypeDef]
    ) -> UpdateEmailChannelResponseTypeDef:
        """
        Enables the email channel for an application or updates the status and settings
        of the email channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_email_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_email_channel)
        """

    def update_email_template(
        self, **kwargs: Unpack[UpdateEmailTemplateRequestRequestTypeDef]
    ) -> UpdateEmailTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the
        email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_email_template)
        """

    def update_endpoint(
        self, **kwargs: Unpack[UpdateEndpointRequestRequestTypeDef]
    ) -> UpdateEndpointResponseTypeDef:
        """
        Creates a new endpoint for an application or updates the settings and
        attributes of an existing endpoint for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_endpoint)
        """

    def update_endpoints_batch(
        self, **kwargs: Unpack[UpdateEndpointsBatchRequestRequestTypeDef]
    ) -> UpdateEndpointsBatchResponseTypeDef:
        """
        Creates a new batch of endpoints for an application or updates the settings and
        attributes of a batch of existing endpoints for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_endpoints_batch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_endpoints_batch)
        """

    def update_gcm_channel(
        self, **kwargs: Unpack[UpdateGcmChannelRequestRequestTypeDef]
    ) -> UpdateGcmChannelResponseTypeDef:
        """
        Enables the GCM channel for an application or updates the status and settings
        of the GCM channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_gcm_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_gcm_channel)
        """

    def update_in_app_template(
        self, **kwargs: Unpack[UpdateInAppTemplateRequestRequestTypeDef]
    ) -> UpdateInAppTemplateResponseTypeDef:
        """
        Updates an existing message template for messages sent through the in-app
        message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_in_app_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_in_app_template)
        """

    def update_journey(
        self, **kwargs: Unpack[UpdateJourneyRequestRequestTypeDef]
    ) -> UpdateJourneyResponseTypeDef:
        """
        Updates the configuration and other settings for a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_journey.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_journey)
        """

    def update_journey_state(
        self, **kwargs: Unpack[UpdateJourneyStateRequestRequestTypeDef]
    ) -> UpdateJourneyStateResponseTypeDef:
        """
        Cancels (stops) an active journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_journey_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_journey_state)
        """

    def update_push_template(
        self, **kwargs: Unpack[UpdatePushTemplateRequestRequestTypeDef]
    ) -> UpdatePushTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_push_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_push_template)
        """

    def update_recommender_configuration(
        self, **kwargs: Unpack[UpdateRecommenderConfigurationRequestRequestTypeDef]
    ) -> UpdateRecommenderConfigurationResponseTypeDef:
        """
        Updates an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_recommender_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_recommender_configuration)
        """

    def update_segment(
        self, **kwargs: Unpack[UpdateSegmentRequestRequestTypeDef]
    ) -> UpdateSegmentResponseTypeDef:
        """
        Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_segment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_segment)
        """

    def update_sms_channel(
        self, **kwargs: Unpack[UpdateSmsChannelRequestRequestTypeDef]
    ) -> UpdateSmsChannelResponseTypeDef:
        """
        Enables the SMS channel for an application or updates the status and settings
        of the SMS channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_sms_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_sms_channel)
        """

    def update_sms_template(
        self, **kwargs: Unpack[UpdateSmsTemplateRequestRequestTypeDef]
    ) -> UpdateSmsTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the SMS
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_sms_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_sms_template)
        """

    def update_template_active_version(
        self, **kwargs: Unpack[UpdateTemplateActiveVersionRequestRequestTypeDef]
    ) -> UpdateTemplateActiveVersionResponseTypeDef:
        """
        Changes the status of a specific version of a message template to <i>active</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_template_active_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_template_active_version)
        """

    def update_voice_channel(
        self, **kwargs: Unpack[UpdateVoiceChannelRequestRequestTypeDef]
    ) -> UpdateVoiceChannelResponseTypeDef:
        """
        Enables the voice channel for an application or updates the status and settings
        of the voice channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_voice_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_voice_channel)
        """

    def update_voice_template(
        self, **kwargs: Unpack[UpdateVoiceTemplateRequestRequestTypeDef]
    ) -> UpdateVoiceTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the
        voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_voice_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#update_voice_template)
        """

    def verify_otp_message(
        self, **kwargs: Unpack[VerifyOTPMessageRequestRequestTypeDef]
    ) -> VerifyOTPMessageResponseTypeDef:
        """
        Verify an OTP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/verify_otp_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint/client/#verify_otp_message)
        """
