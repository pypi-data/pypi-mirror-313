"""
Type annotations for amplifyuibuilder service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplifyuibuilder.client import AmplifyUIBuilderClient
    from types_aiobotocore_amplifyuibuilder.paginator import (
        ExportComponentsPaginator,
        ExportFormsPaginator,
        ExportThemesPaginator,
        ListCodegenJobsPaginator,
        ListComponentsPaginator,
        ListFormsPaginator,
        ListThemesPaginator,
    )

    session = get_session()
    with session.create_client("amplifyuibuilder") as client:
        client: AmplifyUIBuilderClient

        export_components_paginator: ExportComponentsPaginator = client.get_paginator("export_components")
        export_forms_paginator: ExportFormsPaginator = client.get_paginator("export_forms")
        export_themes_paginator: ExportThemesPaginator = client.get_paginator("export_themes")
        list_codegen_jobs_paginator: ListCodegenJobsPaginator = client.get_paginator("list_codegen_jobs")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_forms_paginator: ListFormsPaginator = client.get_paginator("list_forms")
        list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ExportComponentsRequestExportComponentsPaginateTypeDef,
    ExportComponentsResponsePaginatorTypeDef,
    ExportFormsRequestExportFormsPaginateTypeDef,
    ExportFormsResponsePaginatorTypeDef,
    ExportThemesRequestExportThemesPaginateTypeDef,
    ExportThemesResponsePaginatorTypeDef,
    ListCodegenJobsRequestListCodegenJobsPaginateTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsRequestListComponentsPaginateTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsRequestListFormsPaginateTypeDef,
    ListFormsResponseTypeDef,
    ListThemesRequestListThemesPaginateTypeDef,
    ListThemesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ExportComponentsPaginator",
    "ExportFormsPaginator",
    "ExportThemesPaginator",
    "ListCodegenJobsPaginator",
    "ListComponentsPaginator",
    "ListFormsPaginator",
    "ListThemesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ExportComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ExportComponentsRequestExportComponentsPaginateTypeDef]
    ) -> AsyncIterator[ExportComponentsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportcomponentspaginator)
        """


class ExportFormsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportformspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ExportFormsRequestExportFormsPaginateTypeDef]
    ) -> AsyncIterator[ExportFormsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportformspaginator)
        """


class ExportThemesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportthemespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ExportThemesRequestExportThemesPaginateTypeDef]
    ) -> AsyncIterator[ExportThemesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportthemespaginator)
        """


class ListCodegenJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcodegenjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCodegenJobsRequestListCodegenJobsPaginateTypeDef]
    ) -> AsyncIterator[ListCodegenJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcodegenjobspaginator)
        """


class ListComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComponentsRequestListComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcomponentspaginator)
        """


class ListFormsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listformspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFormsRequestListFormsPaginateTypeDef]
    ) -> AsyncIterator[ListFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listformspaginator)
        """


class ListThemesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listthemespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListThemesRequestListThemesPaginateTypeDef]
    ) -> AsyncIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listthemespaginator)
        """
