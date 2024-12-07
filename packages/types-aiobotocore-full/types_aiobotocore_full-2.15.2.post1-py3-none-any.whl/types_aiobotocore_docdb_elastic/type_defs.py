"""
Type annotations for docdb-elastic service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/type_defs/)

Usage::

    ```python
    from types_aiobotocore_docdb_elastic.type_defs import ClusterInListTypeDef

    data: ClusterInListTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence

from .literals import AuthType, SnapshotTypeType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ClusterInListTypeDef",
    "ClusterSnapshotInListTypeDef",
    "ClusterSnapshotTypeDef",
    "ClusterTypeDef",
    "CopyClusterSnapshotInputRequestTypeDef",
    "CopyClusterSnapshotOutputTypeDef",
    "CreateClusterInputRequestTypeDef",
    "CreateClusterOutputTypeDef",
    "CreateClusterSnapshotInputRequestTypeDef",
    "CreateClusterSnapshotOutputTypeDef",
    "DeleteClusterInputRequestTypeDef",
    "DeleteClusterOutputTypeDef",
    "DeleteClusterSnapshotInputRequestTypeDef",
    "DeleteClusterSnapshotOutputTypeDef",
    "GetClusterInputRequestTypeDef",
    "GetClusterOutputTypeDef",
    "GetClusterSnapshotInputRequestTypeDef",
    "GetClusterSnapshotOutputTypeDef",
    "ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef",
    "ListClusterSnapshotsInputRequestTypeDef",
    "ListClusterSnapshotsOutputTypeDef",
    "ListClustersInputListClustersPaginateTypeDef",
    "ListClustersInputRequestTypeDef",
    "ListClustersOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreClusterFromSnapshotInputRequestTypeDef",
    "RestoreClusterFromSnapshotOutputTypeDef",
    "ShardTypeDef",
    "StartClusterInputRequestTypeDef",
    "StartClusterOutputTypeDef",
    "StopClusterInputRequestTypeDef",
    "StopClusterOutputTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateClusterInputRequestTypeDef",
    "UpdateClusterOutputTypeDef",
)


class ClusterInListTypeDef(TypedDict):
    clusterArn: str
    clusterName: str
    status: StatusType


class ClusterSnapshotInListTypeDef(TypedDict):
    clusterArn: str
    snapshotArn: str
    snapshotCreationTime: str
    snapshotName: str
    status: StatusType


class ClusterSnapshotTypeDef(TypedDict):
    adminUserName: str
    clusterArn: str
    clusterCreationTime: str
    kmsKeyId: str
    snapshotArn: str
    snapshotCreationTime: str
    snapshotName: str
    status: StatusType
    subnetIds: List[str]
    vpcSecurityGroupIds: List[str]
    snapshotType: NotRequired[SnapshotTypeType]


class ShardTypeDef(TypedDict):
    createTime: str
    shardId: str
    status: StatusType


class CopyClusterSnapshotInputRequestTypeDef(TypedDict):
    snapshotArn: str
    targetSnapshotName: str
    copyTags: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateClusterInputRequestTypeDef(TypedDict):
    adminUserName: str
    adminUserPassword: str
    authType: AuthType
    clusterName: str
    shardCapacity: int
    shardCount: int
    backupRetentionPeriod: NotRequired[int]
    clientToken: NotRequired[str]
    kmsKeyId: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    shardInstanceCount: NotRequired[int]
    subnetIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class CreateClusterSnapshotInputRequestTypeDef(TypedDict):
    clusterArn: str
    snapshotName: str
    tags: NotRequired[Mapping[str, str]]


class DeleteClusterInputRequestTypeDef(TypedDict):
    clusterArn: str


class DeleteClusterSnapshotInputRequestTypeDef(TypedDict):
    snapshotArn: str


class GetClusterInputRequestTypeDef(TypedDict):
    clusterArn: str


class GetClusterSnapshotInputRequestTypeDef(TypedDict):
    snapshotArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListClusterSnapshotsInputRequestTypeDef(TypedDict):
    clusterArn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    snapshotType: NotRequired[str]


class ListClustersInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class RestoreClusterFromSnapshotInputRequestTypeDef(TypedDict):
    clusterName: str
    snapshotArn: str
    kmsKeyId: NotRequired[str]
    shardCapacity: NotRequired[int]
    shardInstanceCount: NotRequired[int]
    subnetIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class StartClusterInputRequestTypeDef(TypedDict):
    clusterArn: str


class StopClusterInputRequestTypeDef(TypedDict):
    clusterArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateClusterInputRequestTypeDef(TypedDict):
    clusterArn: str
    adminUserPassword: NotRequired[str]
    authType: NotRequired[AuthType]
    backupRetentionPeriod: NotRequired[int]
    clientToken: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    shardCapacity: NotRequired[int]
    shardCount: NotRequired[int]
    shardInstanceCount: NotRequired[int]
    subnetIds: NotRequired[Sequence[str]]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]


class ClusterTypeDef(TypedDict):
    adminUserName: str
    authType: AuthType
    clusterArn: str
    clusterEndpoint: str
    clusterName: str
    createTime: str
    kmsKeyId: str
    preferredMaintenanceWindow: str
    shardCapacity: int
    shardCount: int
    status: StatusType
    subnetIds: List[str]
    vpcSecurityGroupIds: List[str]
    backupRetentionPeriod: NotRequired[int]
    preferredBackupWindow: NotRequired[str]
    shardInstanceCount: NotRequired[int]
    shards: NotRequired[List[ShardTypeDef]]


class CopyClusterSnapshotOutputTypeDef(TypedDict):
    snapshot: ClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterSnapshotOutputTypeDef(TypedDict):
    snapshot: ClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterSnapshotOutputTypeDef(TypedDict):
    snapshot: ClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterSnapshotOutputTypeDef(TypedDict):
    snapshot: ClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListClusterSnapshotsOutputTypeDef(TypedDict):
    snapshots: List[ClusterSnapshotInListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListClustersOutputTypeDef(TypedDict):
    clusters: List[ClusterInListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef(TypedDict):
    clusterArn: NotRequired[str]
    snapshotType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersInputListClustersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreateClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreClusterFromSnapshotOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterOutputTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
