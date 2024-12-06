"""
Type annotations for pinpoint-sms-voice-v2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pinpoint_sms_voice_v2.client import PinpointSMSVoiceV2Client
    from mypy_boto3_pinpoint_sms_voice_v2.paginator import (
        DescribeAccountAttributesPaginator,
        DescribeAccountLimitsPaginator,
        DescribeConfigurationSetsPaginator,
        DescribeKeywordsPaginator,
        DescribeOptOutListsPaginator,
        DescribeOptedOutNumbersPaginator,
        DescribePhoneNumbersPaginator,
        DescribePoolsPaginator,
        DescribeProtectConfigurationsPaginator,
        DescribeRegistrationAttachmentsPaginator,
        DescribeRegistrationFieldDefinitionsPaginator,
        DescribeRegistrationFieldValuesPaginator,
        DescribeRegistrationSectionDefinitionsPaginator,
        DescribeRegistrationTypeDefinitionsPaginator,
        DescribeRegistrationVersionsPaginator,
        DescribeRegistrationsPaginator,
        DescribeSenderIdsPaginator,
        DescribeSpendLimitsPaginator,
        DescribeVerifiedDestinationNumbersPaginator,
        ListPoolOriginationIdentitiesPaginator,
        ListProtectConfigurationRuleSetNumberOverridesPaginator,
        ListRegistrationAssociationsPaginator,
    )

    session = Session()
    client: PinpointSMSVoiceV2Client = session.client("pinpoint-sms-voice-v2")

    describe_account_attributes_paginator: DescribeAccountAttributesPaginator = client.get_paginator("describe_account_attributes")
    describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
    describe_configuration_sets_paginator: DescribeConfigurationSetsPaginator = client.get_paginator("describe_configuration_sets")
    describe_keywords_paginator: DescribeKeywordsPaginator = client.get_paginator("describe_keywords")
    describe_opt_out_lists_paginator: DescribeOptOutListsPaginator = client.get_paginator("describe_opt_out_lists")
    describe_opted_out_numbers_paginator: DescribeOptedOutNumbersPaginator = client.get_paginator("describe_opted_out_numbers")
    describe_phone_numbers_paginator: DescribePhoneNumbersPaginator = client.get_paginator("describe_phone_numbers")
    describe_pools_paginator: DescribePoolsPaginator = client.get_paginator("describe_pools")
    describe_protect_configurations_paginator: DescribeProtectConfigurationsPaginator = client.get_paginator("describe_protect_configurations")
    describe_registration_attachments_paginator: DescribeRegistrationAttachmentsPaginator = client.get_paginator("describe_registration_attachments")
    describe_registration_field_definitions_paginator: DescribeRegistrationFieldDefinitionsPaginator = client.get_paginator("describe_registration_field_definitions")
    describe_registration_field_values_paginator: DescribeRegistrationFieldValuesPaginator = client.get_paginator("describe_registration_field_values")
    describe_registration_section_definitions_paginator: DescribeRegistrationSectionDefinitionsPaginator = client.get_paginator("describe_registration_section_definitions")
    describe_registration_type_definitions_paginator: DescribeRegistrationTypeDefinitionsPaginator = client.get_paginator("describe_registration_type_definitions")
    describe_registration_versions_paginator: DescribeRegistrationVersionsPaginator = client.get_paginator("describe_registration_versions")
    describe_registrations_paginator: DescribeRegistrationsPaginator = client.get_paginator("describe_registrations")
    describe_sender_ids_paginator: DescribeSenderIdsPaginator = client.get_paginator("describe_sender_ids")
    describe_spend_limits_paginator: DescribeSpendLimitsPaginator = client.get_paginator("describe_spend_limits")
    describe_verified_destination_numbers_paginator: DescribeVerifiedDestinationNumbersPaginator = client.get_paginator("describe_verified_destination_numbers")
    list_pool_origination_identities_paginator: ListPoolOriginationIdentitiesPaginator = client.get_paginator("list_pool_origination_identities")
    list_protect_configuration_rule_set_number_overrides_paginator: ListProtectConfigurationRuleSetNumberOverridesPaginator = client.get_paginator("list_protect_configuration_rule_set_number_overrides")
    list_registration_associations_paginator: ListRegistrationAssociationsPaginator = client.get_paginator("list_registration_associations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef,
    DescribeAccountAttributesResultTypeDef,
    DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef,
    DescribeAccountLimitsResultTypeDef,
    DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef,
    DescribeConfigurationSetsResultTypeDef,
    DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef,
    DescribeKeywordsResultTypeDef,
    DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef,
    DescribeOptedOutNumbersResultTypeDef,
    DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef,
    DescribeOptOutListsResultTypeDef,
    DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef,
    DescribePhoneNumbersResultTypeDef,
    DescribePoolsRequestDescribePoolsPaginateTypeDef,
    DescribePoolsResultTypeDef,
    DescribeProtectConfigurationsRequestDescribeProtectConfigurationsPaginateTypeDef,
    DescribeProtectConfigurationsResultTypeDef,
    DescribeRegistrationAttachmentsRequestDescribeRegistrationAttachmentsPaginateTypeDef,
    DescribeRegistrationAttachmentsResultTypeDef,
    DescribeRegistrationFieldDefinitionsRequestDescribeRegistrationFieldDefinitionsPaginateTypeDef,
    DescribeRegistrationFieldDefinitionsResultTypeDef,
    DescribeRegistrationFieldValuesRequestDescribeRegistrationFieldValuesPaginateTypeDef,
    DescribeRegistrationFieldValuesResultTypeDef,
    DescribeRegistrationSectionDefinitionsRequestDescribeRegistrationSectionDefinitionsPaginateTypeDef,
    DescribeRegistrationSectionDefinitionsResultTypeDef,
    DescribeRegistrationsRequestDescribeRegistrationsPaginateTypeDef,
    DescribeRegistrationsResultTypeDef,
    DescribeRegistrationTypeDefinitionsRequestDescribeRegistrationTypeDefinitionsPaginateTypeDef,
    DescribeRegistrationTypeDefinitionsResultTypeDef,
    DescribeRegistrationVersionsRequestDescribeRegistrationVersionsPaginateTypeDef,
    DescribeRegistrationVersionsResultTypeDef,
    DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef,
    DescribeSenderIdsResultTypeDef,
    DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef,
    DescribeSpendLimitsResultTypeDef,
    DescribeVerifiedDestinationNumbersRequestDescribeVerifiedDestinationNumbersPaginateTypeDef,
    DescribeVerifiedDestinationNumbersResultTypeDef,
    ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef,
    ListPoolOriginationIdentitiesResultTypeDef,
    ListProtectConfigurationRuleSetNumberOverridesRequestListProtectConfigurationRuleSetNumberOverridesPaginateTypeDef,
    ListProtectConfigurationRuleSetNumberOverridesResultTypeDef,
    ListRegistrationAssociationsRequestListRegistrationAssociationsPaginateTypeDef,
    ListRegistrationAssociationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountAttributesPaginator",
    "DescribeAccountLimitsPaginator",
    "DescribeConfigurationSetsPaginator",
    "DescribeKeywordsPaginator",
    "DescribeOptOutListsPaginator",
    "DescribeOptedOutNumbersPaginator",
    "DescribePhoneNumbersPaginator",
    "DescribePoolsPaginator",
    "DescribeProtectConfigurationsPaginator",
    "DescribeRegistrationAttachmentsPaginator",
    "DescribeRegistrationFieldDefinitionsPaginator",
    "DescribeRegistrationFieldValuesPaginator",
    "DescribeRegistrationSectionDefinitionsPaginator",
    "DescribeRegistrationTypeDefinitionsPaginator",
    "DescribeRegistrationVersionsPaginator",
    "DescribeRegistrationsPaginator",
    "DescribeSenderIdsPaginator",
    "DescribeSpendLimitsPaginator",
    "DescribeVerifiedDestinationNumbersPaginator",
    "ListPoolOriginationIdentitiesPaginator",
    "ListProtectConfigurationRuleSetNumberOverridesPaginator",
    "ListRegistrationAssociationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountAttributes.html#PinpointSMSVoiceV2.Paginator.DescribeAccountAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeaccountattributespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeAccountAttributesRequestDescribeAccountAttributesPaginateTypeDef],
    ) -> _PageIterator[DescribeAccountAttributesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountAttributes.html#PinpointSMSVoiceV2.Paginator.DescribeAccountAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeaccountattributespaginator)
        """


class DescribeAccountLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountLimits.html#PinpointSMSVoiceV2.Paginator.DescribeAccountLimits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeaccountlimitspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeAccountLimitsRequestDescribeAccountLimitsPaginateTypeDef]
    ) -> _PageIterator[DescribeAccountLimitsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountLimits.html#PinpointSMSVoiceV2.Paginator.DescribeAccountLimits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeaccountlimitspaginator)
        """


class DescribeConfigurationSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeConfigurationSets.html#PinpointSMSVoiceV2.Paginator.DescribeConfigurationSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeconfigurationsetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeConfigurationSetsRequestDescribeConfigurationSetsPaginateTypeDef],
    ) -> _PageIterator[DescribeConfigurationSetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeConfigurationSets.html#PinpointSMSVoiceV2.Paginator.DescribeConfigurationSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeconfigurationsetspaginator)
        """


class DescribeKeywordsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeKeywords.html#PinpointSMSVoiceV2.Paginator.DescribeKeywords)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describekeywordspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeKeywordsRequestDescribeKeywordsPaginateTypeDef]
    ) -> _PageIterator[DescribeKeywordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeKeywords.html#PinpointSMSVoiceV2.Paginator.DescribeKeywords.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describekeywordspaginator)
        """


class DescribeOptOutListsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptOutLists.html#PinpointSMSVoiceV2.Paginator.DescribeOptOutLists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeoptoutlistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeOptOutListsRequestDescribeOptOutListsPaginateTypeDef]
    ) -> _PageIterator[DescribeOptOutListsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptOutLists.html#PinpointSMSVoiceV2.Paginator.DescribeOptOutLists.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeoptoutlistspaginator)
        """


class DescribeOptedOutNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptedOutNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeOptedOutNumbers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeoptedoutnumberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeOptedOutNumbersRequestDescribeOptedOutNumbersPaginateTypeDef]
    ) -> _PageIterator[DescribeOptedOutNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptedOutNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeOptedOutNumbers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeoptedoutnumberspaginator)
        """


class DescribePhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePhoneNumbers.html#PinpointSMSVoiceV2.Paginator.DescribePhoneNumbers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describephonenumberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePhoneNumbersRequestDescribePhoneNumbersPaginateTypeDef]
    ) -> _PageIterator[DescribePhoneNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePhoneNumbers.html#PinpointSMSVoiceV2.Paginator.DescribePhoneNumbers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describephonenumberspaginator)
        """


class DescribePoolsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePools.html#PinpointSMSVoiceV2.Paginator.DescribePools)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describepoolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePoolsRequestDescribePoolsPaginateTypeDef]
    ) -> _PageIterator[DescribePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePools.html#PinpointSMSVoiceV2.Paginator.DescribePools.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describepoolspaginator)
        """


class DescribeProtectConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeProtectConfigurations.html#PinpointSMSVoiceV2.Paginator.DescribeProtectConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeprotectconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeProtectConfigurationsRequestDescribeProtectConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeProtectConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeProtectConfigurations.html#PinpointSMSVoiceV2.Paginator.DescribeProtectConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeprotectconfigurationspaginator)
        """


class DescribeRegistrationAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationAttachments.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationattachmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationAttachmentsRequestDescribeRegistrationAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationAttachments.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationattachmentspaginator)
        """


class DescribeRegistrationFieldDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationfielddefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationFieldDefinitionsRequestDescribeRegistrationFieldDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationFieldDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationfielddefinitionspaginator)
        """


class DescribeRegistrationFieldValuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldValues.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldValues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationfieldvaluespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationFieldValuesRequestDescribeRegistrationFieldValuesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationFieldValuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldValues.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldValues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationfieldvaluespaginator)
        """


class DescribeRegistrationSectionDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationSectionDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationSectionDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationsectiondefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationSectionDefinitionsRequestDescribeRegistrationSectionDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationSectionDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationSectionDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationSectionDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationsectiondefinitionspaginator)
        """


class DescribeRegistrationTypeDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationTypeDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationTypeDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationtypedefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationTypeDefinitionsRequestDescribeRegistrationTypeDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationTypeDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationTypeDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationTypeDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationtypedefinitionspaginator)
        """


class DescribeRegistrationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationVersions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRegistrationVersionsRequestDescribeRegistrationVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRegistrationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationVersions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationversionspaginator)
        """


class DescribeRegistrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrations.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeRegistrationsRequestDescribeRegistrationsPaginateTypeDef]
    ) -> _PageIterator[DescribeRegistrationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrations.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeregistrationspaginator)
        """


class DescribeSenderIdsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSenderIds.html#PinpointSMSVoiceV2.Paginator.DescribeSenderIds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describesenderidspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSenderIdsRequestDescribeSenderIdsPaginateTypeDef]
    ) -> _PageIterator[DescribeSenderIdsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSenderIds.html#PinpointSMSVoiceV2.Paginator.DescribeSenderIds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describesenderidspaginator)
        """


class DescribeSpendLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSpendLimits.html#PinpointSMSVoiceV2.Paginator.DescribeSpendLimits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describespendlimitspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSpendLimitsRequestDescribeSpendLimitsPaginateTypeDef]
    ) -> _PageIterator[DescribeSpendLimitsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSpendLimits.html#PinpointSMSVoiceV2.Paginator.DescribeSpendLimits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describespendlimitspaginator)
        """


class DescribeVerifiedDestinationNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeVerifiedDestinationNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeVerifiedDestinationNumbers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeverifieddestinationnumberspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeVerifiedDestinationNumbersRequestDescribeVerifiedDestinationNumbersPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeVerifiedDestinationNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeVerifiedDestinationNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeVerifiedDestinationNumbers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#describeverifieddestinationnumberspaginator)
        """


class ListPoolOriginationIdentitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListPoolOriginationIdentities.html#PinpointSMSVoiceV2.Paginator.ListPoolOriginationIdentities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listpooloriginationidentitiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPoolOriginationIdentitiesRequestListPoolOriginationIdentitiesPaginateTypeDef
        ],
    ) -> _PageIterator[ListPoolOriginationIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListPoolOriginationIdentities.html#PinpointSMSVoiceV2.Paginator.ListPoolOriginationIdentities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listpooloriginationidentitiespaginator)
        """


class ListProtectConfigurationRuleSetNumberOverridesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListProtectConfigurationRuleSetNumberOverrides.html#PinpointSMSVoiceV2.Paginator.ListProtectConfigurationRuleSetNumberOverrides)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listprotectconfigurationrulesetnumberoverridespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListProtectConfigurationRuleSetNumberOverridesRequestListProtectConfigurationRuleSetNumberOverridesPaginateTypeDef
        ],
    ) -> _PageIterator[ListProtectConfigurationRuleSetNumberOverridesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListProtectConfigurationRuleSetNumberOverrides.html#PinpointSMSVoiceV2.Paginator.ListProtectConfigurationRuleSetNumberOverrides.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listprotectconfigurationrulesetnumberoverridespaginator)
        """


class ListRegistrationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListRegistrationAssociations.html#PinpointSMSVoiceV2.Paginator.ListRegistrationAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listregistrationassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRegistrationAssociationsRequestListRegistrationAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListRegistrationAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListRegistrationAssociations.html#PinpointSMSVoiceV2.Paginator.ListRegistrationAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice_v2/paginators/#listregistrationassociationspaginator)
        """
