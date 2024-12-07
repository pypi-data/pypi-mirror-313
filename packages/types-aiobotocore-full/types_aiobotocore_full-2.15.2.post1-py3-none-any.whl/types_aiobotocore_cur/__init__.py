"""
Main interface for cur service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cur import (
        Client,
        CostandUsageReportServiceClient,
        DescribeReportDefinitionsPaginator,
    )

    session = get_session()
    async with session.create_client("cur") as client:
        client: CostandUsageReportServiceClient
        ...


    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CostandUsageReportServiceClient
from .paginator import DescribeReportDefinitionsPaginator

Client = CostandUsageReportServiceClient


__all__ = ("Client", "CostandUsageReportServiceClient", "DescribeReportDefinitionsPaginator")
