"""
Main interface for application-insights service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_application_insights import (
        ApplicationInsightsClient,
        Client,
    )

    session = Session()
    client: ApplicationInsightsClient = session.client("application-insights")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ApplicationInsightsClient

Client = ApplicationInsightsClient


__all__ = ("ApplicationInsightsClient", "Client")
