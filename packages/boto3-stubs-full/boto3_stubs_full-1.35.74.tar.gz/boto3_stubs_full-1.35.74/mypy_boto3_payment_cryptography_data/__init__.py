"""
Main interface for payment-cryptography-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_payment_cryptography_data import (
        Client,
        PaymentCryptographyDataPlaneClient,
    )

    session = Session()
    client: PaymentCryptographyDataPlaneClient = session.client("payment-cryptography-data")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PaymentCryptographyDataPlaneClient

Client = PaymentCryptographyDataPlaneClient


__all__ = ("Client", "PaymentCryptographyDataPlaneClient")
