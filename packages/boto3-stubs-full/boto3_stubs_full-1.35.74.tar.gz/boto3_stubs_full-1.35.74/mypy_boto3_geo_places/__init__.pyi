"""
Main interface for geo-places service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_places import (
        Client,
        LocationServicePlacesV2Client,
    )

    session = Session()
    client: LocationServicePlacesV2Client = session.client("geo-places")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LocationServicePlacesV2Client

Client = LocationServicePlacesV2Client

__all__ = ("Client", "LocationServicePlacesV2Client")
