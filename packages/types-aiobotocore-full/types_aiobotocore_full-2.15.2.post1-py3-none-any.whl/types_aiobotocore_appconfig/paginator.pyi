"""
Type annotations for appconfig service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appconfig.client import AppConfigClient
    from types_aiobotocore_appconfig.paginator import (
        ListApplicationsPaginator,
        ListConfigurationProfilesPaginator,
        ListDeploymentStrategiesPaginator,
        ListDeploymentsPaginator,
        ListEnvironmentsPaginator,
        ListExtensionAssociationsPaginator,
        ListExtensionsPaginator,
        ListHostedConfigurationVersionsPaginator,
    )

    session = get_session()
    with session.create_client("appconfig") as client:
        client: AppConfigClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_configuration_profiles_paginator: ListConfigurationProfilesPaginator = client.get_paginator("list_configuration_profiles")
        list_deployment_strategies_paginator: ListDeploymentStrategiesPaginator = client.get_paginator("list_deployment_strategies")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_extension_associations_paginator: ListExtensionAssociationsPaginator = client.get_paginator("list_extension_associations")
        list_extensions_paginator: ListExtensionsPaginator = client.get_paginator("list_extensions")
        list_hosted_configuration_versions_paginator: ListHostedConfigurationVersionsPaginator = client.get_paginator("list_hosted_configuration_versions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ApplicationsTypeDef,
    ConfigurationProfilesTypeDef,
    DeploymentStrategiesTypeDef,
    DeploymentsTypeDef,
    EnvironmentsTypeDef,
    ExtensionAssociationsTypeDef,
    ExtensionsTypeDef,
    HostedConfigurationVersionsTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListConfigurationProfilesRequestListConfigurationProfilesPaginateTypeDef,
    ListDeploymentsRequestListDeploymentsPaginateTypeDef,
    ListDeploymentStrategiesRequestListDeploymentStrategiesPaginateTypeDef,
    ListEnvironmentsRequestListEnvironmentsPaginateTypeDef,
    ListExtensionAssociationsRequestListExtensionAssociationsPaginateTypeDef,
    ListExtensionsRequestListExtensionsPaginateTypeDef,
    ListHostedConfigurationVersionsRequestListHostedConfigurationVersionsPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListConfigurationProfilesPaginator",
    "ListDeploymentStrategiesPaginator",
    "ListDeploymentsPaginator",
    "ListEnvironmentsPaginator",
    "ListExtensionAssociationsPaginator",
    "ListExtensionsPaginator",
    "ListHostedConfigurationVersionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ApplicationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listapplicationspaginator)
        """

class ListConfigurationProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listconfigurationprofilespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationProfilesRequestListConfigurationProfilesPaginateTypeDef],
    ) -> AsyncIterator[ConfigurationProfilesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listconfigurationprofilespaginator)
        """

class ListDeploymentStrategiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentstrategiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDeploymentStrategiesRequestListDeploymentStrategiesPaginateTypeDef],
    ) -> AsyncIterator[DeploymentStrategiesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentstrategiespaginator)
        """

class ListDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeploymentsRequestListDeploymentsPaginateTypeDef]
    ) -> AsyncIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentspaginator)
        """

class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsRequestListEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[EnvironmentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listenvironmentspaginator)
        """

class ListExtensionAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListExtensionAssociationsRequestListExtensionAssociationsPaginateTypeDef],
    ) -> AsyncIterator[ExtensionAssociationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionassociationspaginator)
        """

class ListExtensionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExtensionsRequestListExtensionsPaginateTypeDef]
    ) -> AsyncIterator[ExtensionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionspaginator)
        """

class ListHostedConfigurationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listhostedconfigurationversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListHostedConfigurationVersionsRequestListHostedConfigurationVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[HostedConfigurationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listhostedconfigurationversionspaginator)
        """
