"""
Type annotations for qldb service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb.client import QLDBClient

    session = get_session()
    async with session.create_client("qldb") as client:
        client: QLDBClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CancelJournalKinesisStreamRequestRequestTypeDef,
    CancelJournalKinesisStreamResponseTypeDef,
    CreateLedgerRequestRequestTypeDef,
    CreateLedgerResponseTypeDef,
    DeleteLedgerRequestRequestTypeDef,
    DescribeJournalKinesisStreamRequestRequestTypeDef,
    DescribeJournalKinesisStreamResponseTypeDef,
    DescribeJournalS3ExportRequestRequestTypeDef,
    DescribeJournalS3ExportResponseTypeDef,
    DescribeLedgerRequestRequestTypeDef,
    DescribeLedgerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportJournalToS3RequestRequestTypeDef,
    ExportJournalToS3ResponseTypeDef,
    GetBlockRequestRequestTypeDef,
    GetBlockResponseTypeDef,
    GetDigestRequestRequestTypeDef,
    GetDigestResponseTypeDef,
    GetRevisionRequestRequestTypeDef,
    GetRevisionResponseTypeDef,
    ListJournalKinesisStreamsForLedgerRequestRequestTypeDef,
    ListJournalKinesisStreamsForLedgerResponseTypeDef,
    ListJournalS3ExportsForLedgerRequestRequestTypeDef,
    ListJournalS3ExportsForLedgerResponseTypeDef,
    ListJournalS3ExportsRequestRequestTypeDef,
    ListJournalS3ExportsResponseTypeDef,
    ListLedgersRequestRequestTypeDef,
    ListLedgersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StreamJournalToKinesisRequestRequestTypeDef,
    StreamJournalToKinesisResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateLedgerPermissionsModeRequestRequestTypeDef,
    UpdateLedgerPermissionsModeResponseTypeDef,
    UpdateLedgerRequestRequestTypeDef,
    UpdateLedgerResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("QLDBClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourcePreconditionNotMetException: Type[BotocoreClientError]

class QLDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb.html#QLDB.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QLDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb.html#QLDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#close)
        """

    async def cancel_journal_kinesis_stream(
        self, **kwargs: Unpack[CancelJournalKinesisStreamRequestRequestTypeDef]
    ) -> CancelJournalKinesisStreamResponseTypeDef:
        """
        Ends a given Amazon QLDB journal stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/cancel_journal_kinesis_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#cancel_journal_kinesis_stream)
        """

    async def create_ledger(
        self, **kwargs: Unpack[CreateLedgerRequestRequestTypeDef]
    ) -> CreateLedgerResponseTypeDef:
        """
        Creates a new ledger in your Amazon Web Services account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/create_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#create_ledger)
        """

    async def delete_ledger(
        self, **kwargs: Unpack[DeleteLedgerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a ledger and all of its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/delete_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#delete_ledger)
        """

    async def describe_journal_kinesis_stream(
        self, **kwargs: Unpack[DescribeJournalKinesisStreamRequestRequestTypeDef]
    ) -> DescribeJournalKinesisStreamResponseTypeDef:
        """
        Returns detailed information about a given Amazon QLDB journal stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/describe_journal_kinesis_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#describe_journal_kinesis_stream)
        """

    async def describe_journal_s3_export(
        self, **kwargs: Unpack[DescribeJournalS3ExportRequestRequestTypeDef]
    ) -> DescribeJournalS3ExportResponseTypeDef:
        """
        Returns information about a journal export job, including the ledger name,
        export ID, creation time, current status, and the parameters of the original
        export creation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/describe_journal_s3_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#describe_journal_s3_export)
        """

    async def describe_ledger(
        self, **kwargs: Unpack[DescribeLedgerRequestRequestTypeDef]
    ) -> DescribeLedgerResponseTypeDef:
        """
        Returns information about a ledger, including its state, permissions mode,
        encryption at rest settings, and when it was created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/describe_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#describe_ledger)
        """

    async def export_journal_to_s3(
        self, **kwargs: Unpack[ExportJournalToS3RequestRequestTypeDef]
    ) -> ExportJournalToS3ResponseTypeDef:
        """
        Exports journal contents within a date and time range from a ledger into a
        specified Amazon Simple Storage Service (Amazon S3) bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/export_journal_to_s3.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#export_journal_to_s3)
        """

    async def get_block(
        self, **kwargs: Unpack[GetBlockRequestRequestTypeDef]
    ) -> GetBlockResponseTypeDef:
        """
        Returns a block object at a specified address in a journal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/get_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#get_block)
        """

    async def get_digest(
        self, **kwargs: Unpack[GetDigestRequestRequestTypeDef]
    ) -> GetDigestResponseTypeDef:
        """
        Returns the digest of a ledger at the latest committed block in the journal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/get_digest.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#get_digest)
        """

    async def get_revision(
        self, **kwargs: Unpack[GetRevisionRequestRequestTypeDef]
    ) -> GetRevisionResponseTypeDef:
        """
        Returns a revision data object for a specified document ID and block address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/get_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#get_revision)
        """

    async def list_journal_kinesis_streams_for_ledger(
        self, **kwargs: Unpack[ListJournalKinesisStreamsForLedgerRequestRequestTypeDef]
    ) -> ListJournalKinesisStreamsForLedgerResponseTypeDef:
        """
        Returns all Amazon QLDB journal streams for a given ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/list_journal_kinesis_streams_for_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#list_journal_kinesis_streams_for_ledger)
        """

    async def list_journal_s3_exports(
        self, **kwargs: Unpack[ListJournalS3ExportsRequestRequestTypeDef]
    ) -> ListJournalS3ExportsResponseTypeDef:
        """
        Returns all journal export jobs for all ledgers that are associated with the
        current Amazon Web Services account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/list_journal_s3_exports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#list_journal_s3_exports)
        """

    async def list_journal_s3_exports_for_ledger(
        self, **kwargs: Unpack[ListJournalS3ExportsForLedgerRequestRequestTypeDef]
    ) -> ListJournalS3ExportsForLedgerResponseTypeDef:
        """
        Returns all journal export jobs for a specified ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/list_journal_s3_exports_for_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#list_journal_s3_exports_for_ledger)
        """

    async def list_ledgers(
        self, **kwargs: Unpack[ListLedgersRequestRequestTypeDef]
    ) -> ListLedgersResponseTypeDef:
        """
        Returns all ledgers that are associated with the current Amazon Web Services
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/list_ledgers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#list_ledgers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns all tags for a specified Amazon QLDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#list_tags_for_resource)
        """

    async def stream_journal_to_kinesis(
        self, **kwargs: Unpack[StreamJournalToKinesisRequestRequestTypeDef]
    ) -> StreamJournalToKinesisResponseTypeDef:
        """
        Creates a journal stream for a given Amazon QLDB ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/stream_journal_to_kinesis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#stream_journal_to_kinesis)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified Amazon QLDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified Amazon QLDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#untag_resource)
        """

    async def update_ledger(
        self, **kwargs: Unpack[UpdateLedgerRequestRequestTypeDef]
    ) -> UpdateLedgerResponseTypeDef:
        """
        Updates properties on a ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/update_ledger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#update_ledger)
        """

    async def update_ledger_permissions_mode(
        self, **kwargs: Unpack[UpdateLedgerPermissionsModeRequestRequestTypeDef]
    ) -> UpdateLedgerPermissionsModeResponseTypeDef:
        """
        Updates the permissions mode of a ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb/client/update_ledger_permissions_mode.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/#update_ledger_permissions_mode)
        """

    async def __aenter__(self) -> "QLDBClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb.html#QLDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb.html#QLDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/client/)
        """
