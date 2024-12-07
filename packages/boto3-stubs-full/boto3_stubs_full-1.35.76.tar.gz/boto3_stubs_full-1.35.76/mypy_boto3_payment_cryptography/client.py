"""
Type annotations for payment-cryptography service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_payment_cryptography.client import PaymentCryptographyControlPlaneClient

    session = Session()
    client: PaymentCryptographyControlPlaneClient = session.client("payment-cryptography")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAliasesPaginator, ListKeysPaginator, ListTagsForResourcePaginator
from .type_defs import (
    CreateAliasInputRequestTypeDef,
    CreateAliasOutputTypeDef,
    CreateKeyInputRequestTypeDef,
    CreateKeyOutputTypeDef,
    DeleteAliasInputRequestTypeDef,
    DeleteKeyInputRequestTypeDef,
    DeleteKeyOutputTypeDef,
    ExportKeyInputRequestTypeDef,
    ExportKeyOutputTypeDef,
    GetAliasInputRequestTypeDef,
    GetAliasOutputTypeDef,
    GetKeyInputRequestTypeDef,
    GetKeyOutputTypeDef,
    GetParametersForExportInputRequestTypeDef,
    GetParametersForExportOutputTypeDef,
    GetParametersForImportInputRequestTypeDef,
    GetParametersForImportOutputTypeDef,
    GetPublicKeyCertificateInputRequestTypeDef,
    GetPublicKeyCertificateOutputTypeDef,
    ImportKeyInputRequestTypeDef,
    ImportKeyOutputTypeDef,
    ListAliasesInputRequestTypeDef,
    ListAliasesOutputTypeDef,
    ListKeysInputRequestTypeDef,
    ListKeysOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    RestoreKeyInputRequestTypeDef,
    RestoreKeyOutputTypeDef,
    StartKeyUsageInputRequestTypeDef,
    StartKeyUsageOutputTypeDef,
    StopKeyUsageInputRequestTypeDef,
    StopKeyUsageOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateAliasInputRequestTypeDef,
    UpdateAliasOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("PaymentCryptographyControlPlaneClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class PaymentCryptographyControlPlaneClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PaymentCryptographyControlPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#close)
        """

    def create_alias(
        self, **kwargs: Unpack[CreateAliasInputRequestTypeDef]
    ) -> CreateAliasOutputTypeDef:
        """
        Creates an <i>alias</i>, or a friendly name, for an Amazon Web Services Payment
        Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/create_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#create_alias)
        """

    def create_key(self, **kwargs: Unpack[CreateKeyInputRequestTypeDef]) -> CreateKeyOutputTypeDef:
        """
        Creates an Amazon Web Services Payment Cryptography key, a logical
        representation of a cryptographic key, that is unique in your account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/create_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#create_key)
        """

    def delete_alias(self, **kwargs: Unpack[DeleteAliasInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the alias, but doesn't affect the underlying key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/delete_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#delete_alias)
        """

    def delete_key(self, **kwargs: Unpack[DeleteKeyInputRequestTypeDef]) -> DeleteKeyOutputTypeDef:
        """
        Deletes the key material and metadata associated with Amazon Web Services
        Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/delete_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#delete_key)
        """

    def export_key(self, **kwargs: Unpack[ExportKeyInputRequestTypeDef]) -> ExportKeyOutputTypeDef:
        """
        Exports a key from Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/export_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#export_key)
        """

    def get_alias(self, **kwargs: Unpack[GetAliasInputRequestTypeDef]) -> GetAliasOutputTypeDef:
        """
        Gets the Amazon Web Services Payment Cryptography key associated with the alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_alias)
        """

    def get_key(self, **kwargs: Unpack[GetKeyInputRequestTypeDef]) -> GetKeyOutputTypeDef:
        """
        Gets the key material for an Amazon Web Services Payment Cryptography key,
        including the immutable and mutable data specified when the key was created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_key)
        """

    def get_parameters_for_export(
        self, **kwargs: Unpack[GetParametersForExportInputRequestTypeDef]
    ) -> GetParametersForExportOutputTypeDef:
        """
        Gets the export token and the signing key certificate to initiate a TR-34 key
        export from Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_parameters_for_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_parameters_for_export)
        """

    def get_parameters_for_import(
        self, **kwargs: Unpack[GetParametersForImportInputRequestTypeDef]
    ) -> GetParametersForImportOutputTypeDef:
        """
        Gets the import token and the wrapping key certificate in PEM format (base64
        encoded) to initiate a TR-34 WrappedKeyBlock or a RSA WrappedKeyCryptogram
        import into Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_parameters_for_import.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_parameters_for_import)
        """

    def get_public_key_certificate(
        self, **kwargs: Unpack[GetPublicKeyCertificateInputRequestTypeDef]
    ) -> GetPublicKeyCertificateOutputTypeDef:
        """
        Gets the public key certificate of the asymmetric key pair that exists within
        Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_public_key_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_public_key_certificate)
        """

    def import_key(self, **kwargs: Unpack[ImportKeyInputRequestTypeDef]) -> ImportKeyOutputTypeDef:
        """
        Imports symmetric keys and public key certificates in PEM format (base64
        encoded) into Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/import_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#import_key)
        """

    def list_aliases(
        self, **kwargs: Unpack[ListAliasesInputRequestTypeDef]
    ) -> ListAliasesOutputTypeDef:
        """
        Lists the aliases for all keys in the caller's Amazon Web Services account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_aliases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#list_aliases)
        """

    def list_keys(self, **kwargs: Unpack[ListKeysInputRequestTypeDef]) -> ListKeysOutputTypeDef:
        """
        Lists the keys in the caller's Amazon Web Services account and Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_keys.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#list_keys)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags for an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#list_tags_for_resource)
        """

    def restore_key(
        self, **kwargs: Unpack[RestoreKeyInputRequestTypeDef]
    ) -> RestoreKeyOutputTypeDef:
        """
        Cancels a scheduled key deletion during the waiting period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/restore_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#restore_key)
        """

    def start_key_usage(
        self, **kwargs: Unpack[StartKeyUsageInputRequestTypeDef]
    ) -> StartKeyUsageOutputTypeDef:
        """
        Enables an Amazon Web Services Payment Cryptography key, which makes it active
        for cryptographic operations within Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/start_key_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#start_key_usage)
        """

    def stop_key_usage(
        self, **kwargs: Unpack[StopKeyUsageInputRequestTypeDef]
    ) -> StopKeyUsageOutputTypeDef:
        """
        Disables an Amazon Web Services Payment Cryptography key, which makes it
        inactive within Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/stop_key_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#stop_key_usage)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or edits tags on an Amazon Web Services Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a tag from an Amazon Web Services Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#untag_resource)
        """

    def update_alias(
        self, **kwargs: Unpack[UpdateAliasInputRequestTypeDef]
    ) -> UpdateAliasOutputTypeDef:
        """
        Associates an existing Amazon Web Services Payment Cryptography alias with a
        different key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/update_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#update_alias)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/client/#get_paginator)
        """
