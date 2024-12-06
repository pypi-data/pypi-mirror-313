"""
Main interface for observabilityadmin service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_observabilityadmin import (
        Client,
        CloudWatchObservabilityAdminServiceClient,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
    )

    session = Session()
    client: CloudWatchObservabilityAdminServiceClient = session.client("observabilityadmin")

    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchObservabilityAdminServiceClient
from .paginator import ListResourceTelemetryForOrganizationPaginator, ListResourceTelemetryPaginator

Client = CloudWatchObservabilityAdminServiceClient


__all__ = (
    "Client",
    "CloudWatchObservabilityAdminServiceClient",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
)
