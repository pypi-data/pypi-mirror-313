"""
Main interface for geo-routes service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_routes import (
        Client,
        LocationServiceRoutesV2Client,
    )

    session = Session()
    client: LocationServiceRoutesV2Client = session.client("geo-routes")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LocationServiceRoutesV2Client

Client = LocationServiceRoutesV2Client


__all__ = ("Client", "LocationServiceRoutesV2Client")
