"""
Type annotations for acm-pca service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm_pca.client import ACMPCAClient
    from mypy_boto3_acm_pca.waiter import (
        AuditReportCreatedWaiter,
        CertificateAuthorityCSRCreatedWaiter,
        CertificateIssuedWaiter,
    )

    session = Session()
    client: ACMPCAClient = session.client("acm-pca")

    audit_report_created_waiter: AuditReportCreatedWaiter = client.get_waiter("audit_report_created")
    certificate_authority_csr_created_waiter: CertificateAuthorityCSRCreatedWaiter = client.get_waiter("certificate_authority_csr_created")
    certificate_issued_waiter: CertificateIssuedWaiter = client.get_waiter("certificate_issued")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeCertificateAuthorityAuditReportRequestAuditReportCreatedWaitTypeDef,
    GetCertificateAuthorityCsrRequestCertificateAuthorityCSRCreatedWaitTypeDef,
    GetCertificateRequestCertificateIssuedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AuditReportCreatedWaiter",
    "CertificateAuthorityCSRCreatedWaiter",
    "CertificateIssuedWaiter",
)

class AuditReportCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/AuditReportCreated.html#ACMPCA.Waiter.AuditReportCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#auditreportcreatedwaiter)
    """
    def wait(
        self,
        **kwargs: Unpack[
            DescribeCertificateAuthorityAuditReportRequestAuditReportCreatedWaitTypeDef
        ],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/AuditReportCreated.html#ACMPCA.Waiter.AuditReportCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#auditreportcreatedwaiter)
        """

class CertificateAuthorityCSRCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateAuthorityCSRCreated.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
    """
    def wait(
        self,
        **kwargs: Unpack[
            GetCertificateAuthorityCsrRequestCertificateAuthorityCSRCreatedWaitTypeDef
        ],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateAuthorityCSRCreated.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
        """

class CertificateIssuedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateIssued.html#ACMPCA.Waiter.CertificateIssued)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateissuedwaiter)
    """
    def wait(self, **kwargs: Unpack[GetCertificateRequestCertificateIssuedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateIssued.html#ACMPCA.Waiter.CertificateIssued.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateissuedwaiter)
        """
