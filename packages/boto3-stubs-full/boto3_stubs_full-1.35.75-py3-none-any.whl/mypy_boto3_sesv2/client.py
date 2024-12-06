"""
Type annotations for sesv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sesv2.client import SESV2Client

    session = Session()
    client: SESV2Client = session.client("sesv2")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BatchGetMetricDataRequestRequestTypeDef,
    BatchGetMetricDataResponseTypeDef,
    CancelExportJobRequestRequestTypeDef,
    CreateConfigurationSetEventDestinationRequestRequestTypeDef,
    CreateConfigurationSetRequestRequestTypeDef,
    CreateContactListRequestRequestTypeDef,
    CreateContactRequestRequestTypeDef,
    CreateCustomVerificationEmailTemplateRequestRequestTypeDef,
    CreateDedicatedIpPoolRequestRequestTypeDef,
    CreateDeliverabilityTestReportRequestRequestTypeDef,
    CreateDeliverabilityTestReportResponseTypeDef,
    CreateEmailIdentityPolicyRequestRequestTypeDef,
    CreateEmailIdentityRequestRequestTypeDef,
    CreateEmailIdentityResponseTypeDef,
    CreateEmailTemplateRequestRequestTypeDef,
    CreateExportJobRequestRequestTypeDef,
    CreateExportJobResponseTypeDef,
    CreateImportJobRequestRequestTypeDef,
    CreateImportJobResponseTypeDef,
    DeleteConfigurationSetEventDestinationRequestRequestTypeDef,
    DeleteConfigurationSetRequestRequestTypeDef,
    DeleteContactListRequestRequestTypeDef,
    DeleteContactRequestRequestTypeDef,
    DeleteCustomVerificationEmailTemplateRequestRequestTypeDef,
    DeleteDedicatedIpPoolRequestRequestTypeDef,
    DeleteEmailIdentityPolicyRequestRequestTypeDef,
    DeleteEmailIdentityRequestRequestTypeDef,
    DeleteEmailTemplateRequestRequestTypeDef,
    DeleteSuppressedDestinationRequestRequestTypeDef,
    GetAccountResponseTypeDef,
    GetBlacklistReportsRequestRequestTypeDef,
    GetBlacklistReportsResponseTypeDef,
    GetConfigurationSetEventDestinationsRequestRequestTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    GetConfigurationSetRequestRequestTypeDef,
    GetConfigurationSetResponseTypeDef,
    GetContactListRequestRequestTypeDef,
    GetContactListResponseTypeDef,
    GetContactRequestRequestTypeDef,
    GetContactResponseTypeDef,
    GetCustomVerificationEmailTemplateRequestRequestTypeDef,
    GetCustomVerificationEmailTemplateResponseTypeDef,
    GetDedicatedIpPoolRequestRequestTypeDef,
    GetDedicatedIpPoolResponseTypeDef,
    GetDedicatedIpRequestRequestTypeDef,
    GetDedicatedIpResponseTypeDef,
    GetDedicatedIpsRequestRequestTypeDef,
    GetDedicatedIpsResponseTypeDef,
    GetDeliverabilityDashboardOptionsResponseTypeDef,
    GetDeliverabilityTestReportRequestRequestTypeDef,
    GetDeliverabilityTestReportResponseTypeDef,
    GetDomainDeliverabilityCampaignRequestRequestTypeDef,
    GetDomainDeliverabilityCampaignResponseTypeDef,
    GetDomainStatisticsReportRequestRequestTypeDef,
    GetDomainStatisticsReportResponseTypeDef,
    GetEmailIdentityPoliciesRequestRequestTypeDef,
    GetEmailIdentityPoliciesResponseTypeDef,
    GetEmailIdentityRequestRequestTypeDef,
    GetEmailIdentityResponseTypeDef,
    GetEmailTemplateRequestRequestTypeDef,
    GetEmailTemplateResponseTypeDef,
    GetExportJobRequestRequestTypeDef,
    GetExportJobResponseTypeDef,
    GetImportJobRequestRequestTypeDef,
    GetImportJobResponseTypeDef,
    GetMessageInsightsRequestRequestTypeDef,
    GetMessageInsightsResponseTypeDef,
    GetSuppressedDestinationRequestRequestTypeDef,
    GetSuppressedDestinationResponseTypeDef,
    ListConfigurationSetsRequestRequestTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListContactListsRequestRequestTypeDef,
    ListContactListsResponseTypeDef,
    ListContactsRequestRequestTypeDef,
    ListContactsResponseTypeDef,
    ListCustomVerificationEmailTemplatesRequestRequestTypeDef,
    ListCustomVerificationEmailTemplatesResponseTypeDef,
    ListDedicatedIpPoolsRequestRequestTypeDef,
    ListDedicatedIpPoolsResponseTypeDef,
    ListDeliverabilityTestReportsRequestRequestTypeDef,
    ListDeliverabilityTestReportsResponseTypeDef,
    ListDomainDeliverabilityCampaignsRequestRequestTypeDef,
    ListDomainDeliverabilityCampaignsResponseTypeDef,
    ListEmailIdentitiesRequestRequestTypeDef,
    ListEmailIdentitiesResponseTypeDef,
    ListEmailTemplatesRequestRequestTypeDef,
    ListEmailTemplatesResponseTypeDef,
    ListExportJobsRequestRequestTypeDef,
    ListExportJobsResponseTypeDef,
    ListImportJobsRequestRequestTypeDef,
    ListImportJobsResponseTypeDef,
    ListRecommendationsRequestRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    ListSuppressedDestinationsRequestRequestTypeDef,
    ListSuppressedDestinationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef,
    PutAccountDetailsRequestRequestTypeDef,
    PutAccountSendingAttributesRequestRequestTypeDef,
    PutAccountSuppressionAttributesRequestRequestTypeDef,
    PutAccountVdmAttributesRequestRequestTypeDef,
    PutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
    PutConfigurationSetReputationOptionsRequestRequestTypeDef,
    PutConfigurationSetSendingOptionsRequestRequestTypeDef,
    PutConfigurationSetSuppressionOptionsRequestRequestTypeDef,
    PutConfigurationSetTrackingOptionsRequestRequestTypeDef,
    PutConfigurationSetVdmOptionsRequestRequestTypeDef,
    PutDedicatedIpInPoolRequestRequestTypeDef,
    PutDedicatedIpPoolScalingAttributesRequestRequestTypeDef,
    PutDedicatedIpWarmupAttributesRequestRequestTypeDef,
    PutDeliverabilityDashboardOptionRequestRequestTypeDef,
    PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef,
    PutEmailIdentityDkimAttributesRequestRequestTypeDef,
    PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef,
    PutEmailIdentityDkimSigningAttributesResponseTypeDef,
    PutEmailIdentityFeedbackAttributesRequestRequestTypeDef,
    PutEmailIdentityMailFromAttributesRequestRequestTypeDef,
    PutSuppressedDestinationRequestRequestTypeDef,
    SendBulkEmailRequestRequestTypeDef,
    SendBulkEmailResponseTypeDef,
    SendCustomVerificationEmailRequestRequestTypeDef,
    SendCustomVerificationEmailResponseTypeDef,
    SendEmailRequestRequestTypeDef,
    SendEmailResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestRenderEmailTemplateRequestRequestTypeDef,
    TestRenderEmailTemplateResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConfigurationSetEventDestinationRequestRequestTypeDef,
    UpdateContactListRequestRequestTypeDef,
    UpdateContactRequestRequestTypeDef,
    UpdateCustomVerificationEmailTemplateRequestRequestTypeDef,
    UpdateEmailIdentityPolicyRequestRequestTypeDef,
    UpdateEmailTemplateRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SESV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccountSuspendedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailFromDomainNotVerifiedException: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SendingPausedException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class SESV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SESV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#close)
        """

    def batch_get_metric_data(
        self, **kwargs: Unpack[BatchGetMetricDataRequestRequestTypeDef]
    ) -> BatchGetMetricDataResponseTypeDef:
        """
        Retrieves batches of metric data collected based on your sending activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/batch_get_metric_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#batch_get_metric_data)
        """

    def cancel_export_job(
        self, **kwargs: Unpack[CancelExportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/cancel_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#cancel_export_job)
        """

    def create_configuration_set(
        self, **kwargs: Unpack[CreateConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_configuration_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self, **kwargs: Unpack[CreateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_configuration_set_event_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_configuration_set_event_destination)
        """

    def create_contact(
        self, **kwargs: Unpack[CreateContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a contact, which is an end-user who is receiving the email, and adds
        them to a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_contact)
        """

    def create_contact_list(
        self, **kwargs: Unpack[CreateContactListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_contact_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_contact_list)
        """

    def create_custom_verification_email_template(
        self, **kwargs: Unpack[CreateCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_custom_verification_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_custom_verification_email_template)
        """

    def create_dedicated_ip_pool(
        self, **kwargs: Unpack[CreateDedicatedIpPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a new pool of dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_dedicated_ip_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_dedicated_ip_pool)
        """

    def create_deliverability_test_report(
        self, **kwargs: Unpack[CreateDeliverabilityTestReportRequestRequestTypeDef]
    ) -> CreateDeliverabilityTestReportResponseTypeDef:
        """
        Create a new predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_deliverability_test_report.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_deliverability_test_report)
        """

    def create_email_identity(
        self, **kwargs: Unpack[CreateEmailIdentityRequestRequestTypeDef]
    ) -> CreateEmailIdentityResponseTypeDef:
        """
        Starts the process of verifying an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_email_identity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_email_identity)
        """

    def create_email_identity_policy(
        self, **kwargs: Unpack[CreateEmailIdentityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates the specified sending authorization policy for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_email_identity_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_email_identity_policy)
        """

    def create_email_template(
        self, **kwargs: Unpack[CreateEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_email_template)
        """

    def create_export_job(
        self, **kwargs: Unpack[CreateExportJobRequestRequestTypeDef]
    ) -> CreateExportJobResponseTypeDef:
        """
        Creates an export job for a data source and destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_export_job)
        """

    def create_import_job(
        self, **kwargs: Unpack[CreateImportJobRequestRequestTypeDef]
    ) -> CreateImportJobResponseTypeDef:
        """
        Creates an import job for a data destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/create_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#create_import_job)
        """

    def delete_configuration_set(
        self, **kwargs: Unpack[DeleteConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_configuration_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, **kwargs: Unpack[DeleteConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_configuration_set_event_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_configuration_set_event_destination)
        """

    def delete_contact(
        self, **kwargs: Unpack[DeleteContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a contact from a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_contact)
        """

    def delete_contact_list(
        self, **kwargs: Unpack[DeleteContactListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a contact list and all of the contacts on that list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_contact_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_contact_list)
        """

    def delete_custom_verification_email_template(
        self, **kwargs: Unpack[DeleteCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_custom_verification_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_custom_verification_email_template)
        """

    def delete_dedicated_ip_pool(
        self, **kwargs: Unpack[DeleteDedicatedIpPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_dedicated_ip_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_dedicated_ip_pool)
        """

    def delete_email_identity(
        self, **kwargs: Unpack[DeleteEmailIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_email_identity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_email_identity)
        """

    def delete_email_identity_policy(
        self, **kwargs: Unpack[DeleteEmailIdentityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified sending authorization policy for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_email_identity_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_email_identity_policy)
        """

    def delete_email_template(
        self, **kwargs: Unpack[DeleteEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_email_template)
        """

    def delete_suppressed_destination(
        self, **kwargs: Unpack[DeleteSuppressedDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an email address from the suppression list for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/delete_suppressed_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#delete_suppressed_destination)
        """

    def get_account(self) -> GetAccountResponseTypeDef:
        """
        Obtain information about the email-sending status and capabilities of your
        Amazon SES account in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_account)
        """

    def get_blacklist_reports(
        self, **kwargs: Unpack[GetBlacklistReportsRequestRequestTypeDef]
    ) -> GetBlacklistReportsResponseTypeDef:
        """
        Retrieve a list of the blacklists that your dedicated IP addresses appear on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_blacklist_reports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_blacklist_reports)
        """

    def get_configuration_set(
        self, **kwargs: Unpack[GetConfigurationSetRequestRequestTypeDef]
    ) -> GetConfigurationSetResponseTypeDef:
        """
        Get information about an existing configuration set, including the dedicated IP
        pool that it's associated with, whether or not it's enabled for sending email,
        and more.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_configuration_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_configuration_set)
        """

    def get_configuration_set_event_destinations(
        self, **kwargs: Unpack[GetConfigurationSetEventDestinationsRequestRequestTypeDef]
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Retrieve a list of event destinations that are associated with a configuration
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_configuration_set_event_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_configuration_set_event_destinations)
        """

    def get_contact(
        self, **kwargs: Unpack[GetContactRequestRequestTypeDef]
    ) -> GetContactResponseTypeDef:
        """
        Returns a contact from a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_contact)
        """

    def get_contact_list(
        self, **kwargs: Unpack[GetContactListRequestRequestTypeDef]
    ) -> GetContactListResponseTypeDef:
        """
        Returns contact list metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_contact_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_contact_list)
        """

    def get_custom_verification_email_template(
        self, **kwargs: Unpack[GetCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> GetCustomVerificationEmailTemplateResponseTypeDef:
        """
        Returns the custom email verification template for the template name you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_custom_verification_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_custom_verification_email_template)
        """

    def get_dedicated_ip(
        self, **kwargs: Unpack[GetDedicatedIpRequestRequestTypeDef]
    ) -> GetDedicatedIpResponseTypeDef:
        """
        Get information about a dedicated IP address, including the name of the
        dedicated IP pool that it's associated with, as well information about the
        automatic warm-up process for the address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_dedicated_ip.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_dedicated_ip)
        """

    def get_dedicated_ip_pool(
        self, **kwargs: Unpack[GetDedicatedIpPoolRequestRequestTypeDef]
    ) -> GetDedicatedIpPoolResponseTypeDef:
        """
        Retrieve information about the dedicated pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_dedicated_ip_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_dedicated_ip_pool)
        """

    def get_dedicated_ips(
        self, **kwargs: Unpack[GetDedicatedIpsRequestRequestTypeDef]
    ) -> GetDedicatedIpsResponseTypeDef:
        """
        List the dedicated IP addresses that are associated with your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_dedicated_ips.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_dedicated_ips)
        """

    def get_deliverability_dashboard_options(
        self,
    ) -> GetDeliverabilityDashboardOptionsResponseTypeDef:
        """
        Retrieve information about the status of the Deliverability dashboard for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_deliverability_dashboard_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_deliverability_dashboard_options)
        """

    def get_deliverability_test_report(
        self, **kwargs: Unpack[GetDeliverabilityTestReportRequestRequestTypeDef]
    ) -> GetDeliverabilityTestReportResponseTypeDef:
        """
        Retrieve the results of a predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_deliverability_test_report.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_deliverability_test_report)
        """

    def get_domain_deliverability_campaign(
        self, **kwargs: Unpack[GetDomainDeliverabilityCampaignRequestRequestTypeDef]
    ) -> GetDomainDeliverabilityCampaignResponseTypeDef:
        """
        Retrieve all the deliverability data for a specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_domain_deliverability_campaign.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_domain_deliverability_campaign)
        """

    def get_domain_statistics_report(
        self, **kwargs: Unpack[GetDomainStatisticsReportRequestRequestTypeDef]
    ) -> GetDomainStatisticsReportResponseTypeDef:
        """
        Retrieve inbox placement and engagement rates for the domains that you use to
        send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_domain_statistics_report.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_domain_statistics_report)
        """

    def get_email_identity(
        self, **kwargs: Unpack[GetEmailIdentityRequestRequestTypeDef]
    ) -> GetEmailIdentityResponseTypeDef:
        """
        Provides information about a specific identity, including the identity's
        verification status, sending authorization policies, its DKIM authentication
        status, and its custom Mail-From settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_email_identity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_email_identity)
        """

    def get_email_identity_policies(
        self, **kwargs: Unpack[GetEmailIdentityPoliciesRequestRequestTypeDef]
    ) -> GetEmailIdentityPoliciesResponseTypeDef:
        """
        Returns the requested sending authorization policies for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_email_identity_policies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_email_identity_policies)
        """

    def get_email_template(
        self, **kwargs: Unpack[GetEmailTemplateRequestRequestTypeDef]
    ) -> GetEmailTemplateResponseTypeDef:
        """
        Displays the template object (which includes the subject line, HTML part and
        text part) for the template you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_email_template)
        """

    def get_export_job(
        self, **kwargs: Unpack[GetExportJobRequestRequestTypeDef]
    ) -> GetExportJobResponseTypeDef:
        """
        Provides information about an export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_export_job)
        """

    def get_import_job(
        self, **kwargs: Unpack[GetImportJobRequestRequestTypeDef]
    ) -> GetImportJobResponseTypeDef:
        """
        Provides information about an import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_import_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_import_job)
        """

    def get_message_insights(
        self, **kwargs: Unpack[GetMessageInsightsRequestRequestTypeDef]
    ) -> GetMessageInsightsResponseTypeDef:
        """
        Provides information about a specific message, including the from address, the
        subject, the recipient address, email tags, as well as events associated with
        the message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_message_insights.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_message_insights)
        """

    def get_suppressed_destination(
        self, **kwargs: Unpack[GetSuppressedDestinationRequestRequestTypeDef]
    ) -> GetSuppressedDestinationResponseTypeDef:
        """
        Retrieves information about a specific email address that's on the suppression
        list for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/get_suppressed_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#get_suppressed_destination)
        """

    def list_configuration_sets(
        self, **kwargs: Unpack[ListConfigurationSetsRequestRequestTypeDef]
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        List all of the configuration sets associated with your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_configuration_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_configuration_sets)
        """

    def list_contact_lists(
        self, **kwargs: Unpack[ListContactListsRequestRequestTypeDef]
    ) -> ListContactListsResponseTypeDef:
        """
        Lists all of the contact lists available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_contact_lists.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_contact_lists)
        """

    def list_contacts(
        self, **kwargs: Unpack[ListContactsRequestRequestTypeDef]
    ) -> ListContactsResponseTypeDef:
        """
        Lists the contacts present in a specific contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_contacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_contacts)
        """

    def list_custom_verification_email_templates(
        self, **kwargs: Unpack[ListCustomVerificationEmailTemplatesRequestRequestTypeDef]
    ) -> ListCustomVerificationEmailTemplatesResponseTypeDef:
        """
        Lists the existing custom verification email templates for your account in the
        current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_custom_verification_email_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_custom_verification_email_templates)
        """

    def list_dedicated_ip_pools(
        self, **kwargs: Unpack[ListDedicatedIpPoolsRequestRequestTypeDef]
    ) -> ListDedicatedIpPoolsResponseTypeDef:
        """
        List all of the dedicated IP pools that exist in your Amazon Web Services
        account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_dedicated_ip_pools.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_dedicated_ip_pools)
        """

    def list_deliverability_test_reports(
        self, **kwargs: Unpack[ListDeliverabilityTestReportsRequestRequestTypeDef]
    ) -> ListDeliverabilityTestReportsResponseTypeDef:
        """
        Show a list of the predictive inbox placement tests that you've performed,
        regardless of their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_deliverability_test_reports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_deliverability_test_reports)
        """

    def list_domain_deliverability_campaigns(
        self, **kwargs: Unpack[ListDomainDeliverabilityCampaignsRequestRequestTypeDef]
    ) -> ListDomainDeliverabilityCampaignsResponseTypeDef:
        """
        Retrieve deliverability data for all the campaigns that used a specific domain
        to send email during a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_domain_deliverability_campaigns.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_domain_deliverability_campaigns)
        """

    def list_email_identities(
        self, **kwargs: Unpack[ListEmailIdentitiesRequestRequestTypeDef]
    ) -> ListEmailIdentitiesResponseTypeDef:
        """
        Returns a list of all of the email identities that are associated with your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_email_identities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_email_identities)
        """

    def list_email_templates(
        self, **kwargs: Unpack[ListEmailTemplatesRequestRequestTypeDef]
    ) -> ListEmailTemplatesResponseTypeDef:
        """
        Lists the email templates present in your Amazon SES account in the current
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_email_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_email_templates)
        """

    def list_export_jobs(
        self, **kwargs: Unpack[ListExportJobsRequestRequestTypeDef]
    ) -> ListExportJobsResponseTypeDef:
        """
        Lists all of the export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_export_jobs)
        """

    def list_import_jobs(
        self, **kwargs: Unpack[ListImportJobsRequestRequestTypeDef]
    ) -> ListImportJobsResponseTypeDef:
        """
        Lists all of the import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_import_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_import_jobs)
        """

    def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Lists the recommendations present in your Amazon SES account in the current
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_recommendations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_recommendations)
        """

    def list_suppressed_destinations(
        self, **kwargs: Unpack[ListSuppressedDestinationsRequestRequestTypeDef]
    ) -> ListSuppressedDestinationsResponseTypeDef:
        """
        Retrieves a list of email addresses that are on the suppression list for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_suppressed_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_suppressed_destinations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#list_tags_for_resource)
        """

    def put_account_dedicated_ip_warmup_attributes(
        self, **kwargs: Unpack[PutAccountDedicatedIpWarmupAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the automatic warm-up feature for dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_account_dedicated_ip_warmup_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_account_dedicated_ip_warmup_attributes)
        """

    def put_account_details(
        self, **kwargs: Unpack[PutAccountDetailsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update your Amazon SES account details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_account_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_account_details)
        """

    def put_account_sending_attributes(
        self, **kwargs: Unpack[PutAccountSendingAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the ability of your account to send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_account_sending_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_account_sending_attributes)
        """

    def put_account_suppression_attributes(
        self, **kwargs: Unpack[PutAccountSuppressionAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Change the settings for the account-level suppression list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_account_suppression_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_account_suppression_attributes)
        """

    def put_account_vdm_attributes(
        self, **kwargs: Unpack[PutAccountVdmAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update your Amazon SES account VDM attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_account_vdm_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_account_vdm_attributes)
        """

    def put_configuration_set_delivery_options(
        self, **kwargs: Unpack[PutConfigurationSetDeliveryOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate a configuration set with a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_delivery_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_delivery_options)
        """

    def put_configuration_set_reputation_options(
        self, **kwargs: Unpack[PutConfigurationSetReputationOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable collection of reputation metrics for emails that you send
        using a particular configuration set in a specific Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_reputation_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_reputation_options)
        """

    def put_configuration_set_sending_options(
        self, **kwargs: Unpack[PutConfigurationSetSendingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable email sending for messages that use a particular
        configuration set in a specific Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_sending_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_sending_options)
        """

    def put_configuration_set_suppression_options(
        self, **kwargs: Unpack[PutConfigurationSetSuppressionOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specify the account suppression list preferences for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_suppression_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_suppression_options)
        """

    def put_configuration_set_tracking_options(
        self, **kwargs: Unpack[PutConfigurationSetTrackingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specify a custom domain to use for open and click tracking elements in email
        that you send.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_tracking_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_tracking_options)
        """

    def put_configuration_set_vdm_options(
        self, **kwargs: Unpack[PutConfigurationSetVdmOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specify VDM preferences for email that you send using the configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_configuration_set_vdm_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_configuration_set_vdm_options)
        """

    def put_dedicated_ip_in_pool(
        self, **kwargs: Unpack[PutDedicatedIpInPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Move a dedicated IP address to an existing dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_dedicated_ip_in_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_dedicated_ip_in_pool)
        """

    def put_dedicated_ip_pool_scaling_attributes(
        self, **kwargs: Unpack[PutDedicatedIpPoolScalingAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to convert a dedicated IP pool to a different scaling mode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_dedicated_ip_pool_scaling_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_dedicated_ip_pool_scaling_attributes)
        """

    def put_dedicated_ip_warmup_attributes(
        self, **kwargs: Unpack[PutDedicatedIpWarmupAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <p/>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_dedicated_ip_warmup_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_dedicated_ip_warmup_attributes)
        """

    def put_deliverability_dashboard_option(
        self, **kwargs: Unpack[PutDeliverabilityDashboardOptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enable or disable the Deliverability dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_deliverability_dashboard_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_deliverability_dashboard_option)
        """

    def put_email_identity_configuration_set_attributes(
        self, **kwargs: Unpack[PutEmailIdentityConfigurationSetAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to associate a configuration set with an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_email_identity_configuration_set_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_email_identity_configuration_set_attributes)
        """

    def put_email_identity_dkim_attributes(
        self, **kwargs: Unpack[PutEmailIdentityDkimAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable DKIM authentication for an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_email_identity_dkim_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_email_identity_dkim_attributes)
        """

    def put_email_identity_dkim_signing_attributes(
        self, **kwargs: Unpack[PutEmailIdentityDkimSigningAttributesRequestRequestTypeDef]
    ) -> PutEmailIdentityDkimSigningAttributesResponseTypeDef:
        """
        Used to configure or change the DKIM authentication settings for an email
        domain identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_email_identity_dkim_signing_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_email_identity_dkim_signing_attributes)
        """

    def put_email_identity_feedback_attributes(
        self, **kwargs: Unpack[PutEmailIdentityFeedbackAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable feedback forwarding for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_email_identity_feedback_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_email_identity_feedback_attributes)
        """

    def put_email_identity_mail_from_attributes(
        self, **kwargs: Unpack[PutEmailIdentityMailFromAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to enable or disable the custom Mail-From domain configuration for an
        email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_email_identity_mail_from_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_email_identity_mail_from_attributes)
        """

    def put_suppressed_destination(
        self, **kwargs: Unpack[PutSuppressedDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds an email address to the suppression list for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/put_suppressed_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#put_suppressed_destination)
        """

    def send_bulk_email(
        self, **kwargs: Unpack[SendBulkEmailRequestRequestTypeDef]
    ) -> SendBulkEmailResponseTypeDef:
        """
        Composes an email message to multiple destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/send_bulk_email.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#send_bulk_email)
        """

    def send_custom_verification_email(
        self, **kwargs: Unpack[SendCustomVerificationEmailRequestRequestTypeDef]
    ) -> SendCustomVerificationEmailResponseTypeDef:
        """
        Adds an email address to the list of identities for your Amazon SES account in
        the current Amazon Web Services Region and attempts to verify it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/send_custom_verification_email.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#send_custom_verification_email)
        """

    def send_email(
        self, **kwargs: Unpack[SendEmailRequestRequestTypeDef]
    ) -> SendEmailResponseTypeDef:
        """
        Sends an email message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/send_email.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#send_email)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#tag_resource)
        """

    def test_render_email_template(
        self, **kwargs: Unpack[TestRenderEmailTemplateRequestRequestTypeDef]
    ) -> TestRenderEmailTemplateResponseTypeDef:
        """
        Creates a preview of the MIME content of an email when provided with a template
        and a set of replacement data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/test_render_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#test_render_email_template)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#untag_resource)
        """

    def update_configuration_set_event_destination(
        self, **kwargs: Unpack[UpdateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the configuration of an event destination for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_configuration_set_event_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_configuration_set_event_destination)
        """

    def update_contact(
        self, **kwargs: Unpack[UpdateContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a contact's preferences for a list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_contact)
        """

    def update_contact_list(
        self, **kwargs: Unpack[UpdateContactListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates contact list metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_contact_list.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_contact_list)
        """

    def update_custom_verification_email_template(
        self, **kwargs: Unpack[UpdateCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_custom_verification_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_custom_verification_email_template)
        """

    def update_email_identity_policy(
        self, **kwargs: Unpack[UpdateEmailIdentityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified sending authorization policy for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_email_identity_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_email_identity_policy)
        """

    def update_email_template(
        self, **kwargs: Unpack[UpdateEmailTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/client/update_email_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sesv2/client/#update_email_template)
        """
