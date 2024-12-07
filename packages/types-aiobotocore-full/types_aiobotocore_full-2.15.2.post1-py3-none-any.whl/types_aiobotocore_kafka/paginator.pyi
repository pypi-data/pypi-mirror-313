"""
Type annotations for kafka service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kafka.client import KafkaClient
    from types_aiobotocore_kafka.paginator import (
        ListClientVpcConnectionsPaginator,
        ListClusterOperationsPaginator,
        ListClusterOperationsV2Paginator,
        ListClustersPaginator,
        ListClustersV2Paginator,
        ListConfigurationRevisionsPaginator,
        ListConfigurationsPaginator,
        ListKafkaVersionsPaginator,
        ListNodesPaginator,
        ListReplicatorsPaginator,
        ListScramSecretsPaginator,
        ListVpcConnectionsPaginator,
    )

    session = get_session()
    with session.create_client("kafka") as client:
        client: KafkaClient

        list_client_vpc_connections_paginator: ListClientVpcConnectionsPaginator = client.get_paginator("list_client_vpc_connections")
        list_cluster_operations_paginator: ListClusterOperationsPaginator = client.get_paginator("list_cluster_operations")
        list_cluster_operations_v2_paginator: ListClusterOperationsV2Paginator = client.get_paginator("list_cluster_operations_v2")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_clusters_v2_paginator: ListClustersV2Paginator = client.get_paginator("list_clusters_v2")
        list_configuration_revisions_paginator: ListConfigurationRevisionsPaginator = client.get_paginator("list_configuration_revisions")
        list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
        list_kafka_versions_paginator: ListKafkaVersionsPaginator = client.get_paginator("list_kafka_versions")
        list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
        list_replicators_paginator: ListReplicatorsPaginator = client.get_paginator("list_replicators")
        list_scram_secrets_paginator: ListScramSecretsPaginator = client.get_paginator("list_scram_secrets")
        list_vpc_connections_paginator: ListVpcConnectionsPaginator = client.get_paginator("list_vpc_connections")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef,
    ListClientVpcConnectionsResponseTypeDef,
    ListClusterOperationsRequestListClusterOperationsPaginateTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef,
    ListClusterOperationsV2ResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListClustersV2RequestListClustersV2PaginateTypeDef,
    ListClustersV2ResponseTypeDef,
    ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsRequestListConfigurationsPaginateTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesRequestListNodesPaginateTypeDef,
    ListNodesResponseTypeDef,
    ListReplicatorsRequestListReplicatorsPaginateTypeDef,
    ListReplicatorsResponseTypeDef,
    ListScramSecretsRequestListScramSecretsPaginateTypeDef,
    ListScramSecretsResponseTypeDef,
    ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef,
    ListVpcConnectionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListClientVpcConnectionsPaginator",
    "ListClusterOperationsPaginator",
    "ListClusterOperationsV2Paginator",
    "ListClustersPaginator",
    "ListClustersV2Paginator",
    "ListConfigurationRevisionsPaginator",
    "ListConfigurationsPaginator",
    "ListKafkaVersionsPaginator",
    "ListNodesPaginator",
    "ListReplicatorsPaginator",
    "ListScramSecretsPaginator",
    "ListVpcConnectionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListClientVpcConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClientVpcConnections.html#Kafka.Paginator.ListClientVpcConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclientvpcconnectionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef],
    ) -> AsyncIterator[ListClientVpcConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClientVpcConnections.html#Kafka.Paginator.ListClientVpcConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclientvpcconnectionspaginator)
        """

class ListClusterOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperations.html#Kafka.Paginator.ListClusterOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusteroperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClusterOperationsRequestListClusterOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListClusterOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperations.html#Kafka.Paginator.ListClusterOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusteroperationspaginator)
        """

class ListClusterOperationsV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperationsV2.html#Kafka.Paginator.ListClusterOperationsV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusteroperationsv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef]
    ) -> AsyncIterator[ListClusterOperationsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusterOperationsV2.html#Kafka.Paginator.ListClusterOperationsV2.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusteroperationsv2paginator)
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusters.html#Kafka.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClusters.html#Kafka.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclusterspaginator)
        """

class ListClustersV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClustersV2.html#Kafka.Paginator.ListClustersV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclustersv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersV2RequestListClustersV2PaginateTypeDef]
    ) -> AsyncIterator[ListClustersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListClustersV2.html#Kafka.Paginator.ListClustersV2.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listclustersv2paginator)
        """

class ListConfigurationRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurationRevisions.html#Kafka.Paginator.ListConfigurationRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listconfigurationrevisionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListConfigurationRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurationRevisions.html#Kafka.Paginator.ListConfigurationRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listconfigurationrevisionspaginator)
        """

class ListConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurations.html#Kafka.Paginator.ListConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listconfigurationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConfigurationsRequestListConfigurationsPaginateTypeDef]
    ) -> AsyncIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListConfigurations.html#Kafka.Paginator.ListConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listconfigurationspaginator)
        """

class ListKafkaVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListKafkaVersions.html#Kafka.Paginator.ListKafkaVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listkafkaversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListKafkaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListKafkaVersions.html#Kafka.Paginator.ListKafkaVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listkafkaversionspaginator)
        """

class ListNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListNodes.html#Kafka.Paginator.ListNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listnodespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNodesRequestListNodesPaginateTypeDef]
    ) -> AsyncIterator[ListNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListNodes.html#Kafka.Paginator.ListNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listnodespaginator)
        """

class ListReplicatorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListReplicators.html#Kafka.Paginator.ListReplicators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listreplicatorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReplicatorsRequestListReplicatorsPaginateTypeDef]
    ) -> AsyncIterator[ListReplicatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListReplicators.html#Kafka.Paginator.ListReplicators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listreplicatorspaginator)
        """

class ListScramSecretsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListScramSecrets.html#Kafka.Paginator.ListScramSecrets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listscramsecretspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScramSecretsRequestListScramSecretsPaginateTypeDef]
    ) -> AsyncIterator[ListScramSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListScramSecrets.html#Kafka.Paginator.ListScramSecrets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listscramsecretspaginator)
        """

class ListVpcConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListVpcConnections.html#Kafka.Paginator.ListVpcConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listvpcconnectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef]
    ) -> AsyncIterator[ListVpcConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka/paginator/ListVpcConnections.html#Kafka.Paginator.ListVpcConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/paginators/#listvpcconnectionspaginator)
        """
