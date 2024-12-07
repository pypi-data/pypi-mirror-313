"""
Main interface for redshift-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_redshift_data import (
        Client,
        DescribeTablePaginator,
        GetStatementResultPaginator,
        ListDatabasesPaginator,
        ListSchemasPaginator,
        ListStatementsPaginator,
        ListTablesPaginator,
        RedshiftDataAPIServiceClient,
    )

    session = get_session()
    async with session.create_client("redshift-data") as client:
        client: RedshiftDataAPIServiceClient
        ...


    describe_table_paginator: DescribeTablePaginator = client.get_paginator("describe_table")
    get_statement_result_paginator: GetStatementResultPaginator = client.get_paginator("get_statement_result")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_statements_paginator: ListStatementsPaginator = client.get_paginator("list_statements")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RedshiftDataAPIServiceClient
from .paginator import (
    DescribeTablePaginator,
    GetStatementResultPaginator,
    ListDatabasesPaginator,
    ListSchemasPaginator,
    ListStatementsPaginator,
    ListTablesPaginator,
)

Client = RedshiftDataAPIServiceClient

__all__ = (
    "Client",
    "DescribeTablePaginator",
    "GetStatementResultPaginator",
    "ListDatabasesPaginator",
    "ListSchemasPaginator",
    "ListStatementsPaginator",
    "ListTablesPaginator",
    "RedshiftDataAPIServiceClient",
)
