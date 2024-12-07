"""
Type annotations for acm service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_acm.client import ACMClient

    session = Session()
    client: ACMClient = session.client("acm")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListCertificatesPaginator
from .type_defs import (
    AddTagsToCertificateRequestRequestTypeDef,
    DeleteCertificateRequestRequestTypeDef,
    DescribeCertificateRequestRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportCertificateRequestRequestTypeDef,
    ExportCertificateResponseTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetCertificateRequestRequestTypeDef,
    GetCertificateResponseTypeDef,
    ImportCertificateRequestRequestTypeDef,
    ImportCertificateResponseTypeDef,
    ListCertificatesRequestRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListTagsForCertificateRequestRequestTypeDef,
    ListTagsForCertificateResponseTypeDef,
    PutAccountConfigurationRequestRequestTypeDef,
    RemoveTagsFromCertificateRequestRequestTypeDef,
    RenewCertificateRequestRequestTypeDef,
    RequestCertificateRequestRequestTypeDef,
    RequestCertificateResponseTypeDef,
    ResendValidationEmailRequestRequestTypeDef,
    UpdateCertificateOptionsRequestRequestTypeDef,
)
from .waiter import CertificateValidatedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ACMClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidDomainValidationOptionsException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ACMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ACMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#close)
        """

    def add_tags_to_certificate(
        self, **kwargs: Unpack[AddTagsToCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/add_tags_to_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#add_tags_to_certificate)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a certificate and its associated private key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#delete_certificate)
        """

    def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Returns detailed metadata about the specified ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#describe_certificate)
        """

    def export_certificate(
        self, **kwargs: Unpack[ExportCertificateRequestRequestTypeDef]
    ) -> ExportCertificateResponseTypeDef:
        """
        Exports a private certificate issued by a private certificate authority (CA)
        for use anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/export_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#export_certificate)
        """

    def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Returns the account configuration options associated with an Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_account_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#get_account_configuration)
        """

    def get_certificate(
        self, **kwargs: Unpack[GetCertificateRequestRequestTypeDef]
    ) -> GetCertificateResponseTypeDef:
        """
        Retrieves a certificate and its certificate chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#get_certificate)
        """

    def import_certificate(
        self, **kwargs: Unpack[ImportCertificateRequestRequestTypeDef]
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports a certificate into Certificate Manager (ACM) to use with services that
        are integrated with ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/import_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#import_certificate)
        """

    def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Retrieves a list of certificate ARNs and domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_certificates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#list_certificates)
        """

    def list_tags_for_certificate(
        self, **kwargs: Unpack[ListTagsForCertificateRequestRequestTypeDef]
    ) -> ListTagsForCertificateResponseTypeDef:
        """
        Lists the tags that have been applied to the ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_tags_for_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#list_tags_for_certificate)
        """

    def put_account_configuration(
        self, **kwargs: Unpack[PutAccountConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or modifies account-level configurations in ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/put_account_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#put_account_configuration)
        """

    def remove_tags_from_certificate(
        self, **kwargs: Unpack[RemoveTagsFromCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove one or more tags from an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/remove_tags_from_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#remove_tags_from_certificate)
        """

    def renew_certificate(
        self, **kwargs: Unpack[RenewCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renews an eligible ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/renew_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#renew_certificate)
        """

    def request_certificate(
        self, **kwargs: Unpack[RequestCertificateRequestRequestTypeDef]
    ) -> RequestCertificateResponseTypeDef:
        """
        Requests an ACM certificate for use with other Amazon Web Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/request_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#request_certificate)
        """

    def resend_validation_email(
        self, **kwargs: Unpack[ResendValidationEmailRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resends the email that requests domain ownership validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/resend_validation_email.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#resend_validation_email)
        """

    def update_certificate_options(
        self, **kwargs: Unpack[UpdateCertificateOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/update_certificate_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#update_certificate_options)
        """

    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["certificate_validated"]
    ) -> CertificateValidatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/client/#get_waiter)
        """
