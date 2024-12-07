"""
Main interface for security-ir service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_security_ir import (
        Client,
        ListCaseEditsPaginator,
        ListCasesPaginator,
        ListCommentsPaginator,
        ListMembershipsPaginator,
        SecurityIncidentResponseClient,
    )

    session = Session()
    client: SecurityIncidentResponseClient = session.client("security-ir")

    list_case_edits_paginator: ListCaseEditsPaginator = client.get_paginator("list_case_edits")
    list_cases_paginator: ListCasesPaginator = client.get_paginator("list_cases")
    list_comments_paginator: ListCommentsPaginator = client.get_paginator("list_comments")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SecurityIncidentResponseClient
from .paginator import (
    ListCaseEditsPaginator,
    ListCasesPaginator,
    ListCommentsPaginator,
    ListMembershipsPaginator,
)

Client = SecurityIncidentResponseClient

__all__ = (
    "Client",
    "ListCaseEditsPaginator",
    "ListCasesPaginator",
    "ListCommentsPaginator",
    "ListMembershipsPaginator",
    "SecurityIncidentResponseClient",
)
