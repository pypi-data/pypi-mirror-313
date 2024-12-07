"""
Type annotations for support service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support.client import SupportClient

    session = get_session()
    async with session.create_client("support") as client:
        client: SupportClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator
from .type_defs import (
    AddAttachmentsToSetRequestRequestTypeDef,
    AddAttachmentsToSetResponseTypeDef,
    AddCommunicationToCaseRequestRequestTypeDef,
    AddCommunicationToCaseResponseTypeDef,
    CreateCaseRequestRequestTypeDef,
    CreateCaseResponseTypeDef,
    DescribeAttachmentRequestRequestTypeDef,
    DescribeAttachmentResponseTypeDef,
    DescribeCasesRequestRequestTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsRequestRequestTypeDef,
    DescribeCommunicationsResponseTypeDef,
    DescribeCreateCaseOptionsRequestRequestTypeDef,
    DescribeCreateCaseOptionsResponseTypeDef,
    DescribeServicesRequestRequestTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeSeverityLevelsRequestRequestTypeDef,
    DescribeSeverityLevelsResponseTypeDef,
    DescribeSupportedLanguagesRequestRequestTypeDef,
    DescribeSupportedLanguagesResponseTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesRequestRequestTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef,
    DescribeTrustedAdvisorCheckResultRequestRequestTypeDef,
    DescribeTrustedAdvisorCheckResultResponseTypeDef,
    DescribeTrustedAdvisorChecksRequestRequestTypeDef,
    DescribeTrustedAdvisorChecksResponseTypeDef,
    DescribeTrustedAdvisorCheckSummariesRequestRequestTypeDef,
    DescribeTrustedAdvisorCheckSummariesResponseTypeDef,
    RefreshTrustedAdvisorCheckRequestRequestTypeDef,
    RefreshTrustedAdvisorCheckResponseTypeDef,
    ResolveCaseRequestRequestTypeDef,
    ResolveCaseResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SupportClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AttachmentIdNotFound: Type[BotocoreClientError]
    AttachmentLimitExceeded: Type[BotocoreClientError]
    AttachmentSetExpired: Type[BotocoreClientError]
    AttachmentSetIdNotFound: Type[BotocoreClientError]
    AttachmentSetSizeLimitExceeded: Type[BotocoreClientError]
    CaseCreationLimitExceeded: Type[BotocoreClientError]
    CaseIdNotFound: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DescribeAttachmentLimitExceeded: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class SupportClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#close)
        """

    async def add_attachments_to_set(
        self, **kwargs: Unpack[AddAttachmentsToSetRequestRequestTypeDef]
    ) -> AddAttachmentsToSetResponseTypeDef:
        """
        Adds one or more attachments to an attachment set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/add_attachments_to_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#add_attachments_to_set)
        """

    async def add_communication_to_case(
        self, **kwargs: Unpack[AddCommunicationToCaseRequestRequestTypeDef]
    ) -> AddCommunicationToCaseResponseTypeDef:
        """
        Adds additional customer communication to an Amazon Web Services Support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/add_communication_to_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#add_communication_to_case)
        """

    async def create_case(
        self, **kwargs: Unpack[CreateCaseRequestRequestTypeDef]
    ) -> CreateCaseResponseTypeDef:
        """
        Creates a case in the Amazon Web Services Support Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/create_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#create_case)
        """

    async def describe_attachment(
        self, **kwargs: Unpack[DescribeAttachmentRequestRequestTypeDef]
    ) -> DescribeAttachmentResponseTypeDef:
        """
        Returns the attachment that has the specified ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_attachment)
        """

    async def describe_cases(
        self, **kwargs: Unpack[DescribeCasesRequestRequestTypeDef]
    ) -> DescribeCasesResponseTypeDef:
        """
        Returns a list of cases that you specify by passing one or more case IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_cases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_cases)
        """

    async def describe_communications(
        self, **kwargs: Unpack[DescribeCommunicationsRequestRequestTypeDef]
    ) -> DescribeCommunicationsResponseTypeDef:
        """
        Returns communications and attachments for one or more support cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_communications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_communications)
        """

    async def describe_create_case_options(
        self, **kwargs: Unpack[DescribeCreateCaseOptionsRequestRequestTypeDef]
    ) -> DescribeCreateCaseOptionsResponseTypeDef:
        """
        Returns a list of CreateCaseOption types along with the corresponding supported
        hours and language availability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_create_case_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_create_case_options)
        """

    async def describe_services(
        self, **kwargs: Unpack[DescribeServicesRequestRequestTypeDef]
    ) -> DescribeServicesResponseTypeDef:
        """
        Returns the current list of Amazon Web Services services and a list of service
        categories for each service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_services)
        """

    async def describe_severity_levels(
        self, **kwargs: Unpack[DescribeSeverityLevelsRequestRequestTypeDef]
    ) -> DescribeSeverityLevelsResponseTypeDef:
        """
        Returns the list of severity levels that you can assign to a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_severity_levels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_severity_levels)
        """

    async def describe_supported_languages(
        self, **kwargs: Unpack[DescribeSupportedLanguagesRequestRequestTypeDef]
    ) -> DescribeSupportedLanguagesResponseTypeDef:
        """
        Returns a list of supported languages for a specified
        <code>categoryCode</code>, <code>issueType</code> and <code>serviceCode</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_supported_languages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_supported_languages)
        """

    async def describe_trusted_advisor_check_refresh_statuses(
        self, **kwargs: Unpack[DescribeTrustedAdvisorCheckRefreshStatusesRequestRequestTypeDef]
    ) -> DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef:
        """
        Returns the refresh status of the Trusted Advisor checks that have the
        specified check IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_trusted_advisor_check_refresh_statuses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_refresh_statuses)
        """

    async def describe_trusted_advisor_check_result(
        self, **kwargs: Unpack[DescribeTrustedAdvisorCheckResultRequestRequestTypeDef]
    ) -> DescribeTrustedAdvisorCheckResultResponseTypeDef:
        """
        Returns the results of the Trusted Advisor check that has the specified check
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_trusted_advisor_check_result.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_result)
        """

    async def describe_trusted_advisor_check_summaries(
        self, **kwargs: Unpack[DescribeTrustedAdvisorCheckSummariesRequestRequestTypeDef]
    ) -> DescribeTrustedAdvisorCheckSummariesResponseTypeDef:
        """
        Returns the results for the Trusted Advisor check summaries for the check IDs
        that you specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_trusted_advisor_check_summaries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_summaries)
        """

    async def describe_trusted_advisor_checks(
        self, **kwargs: Unpack[DescribeTrustedAdvisorChecksRequestRequestTypeDef]
    ) -> DescribeTrustedAdvisorChecksResponseTypeDef:
        """
        Returns information about all available Trusted Advisor checks, including the
        name, ID, category, description, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/describe_trusted_advisor_checks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_checks)
        """

    async def refresh_trusted_advisor_check(
        self, **kwargs: Unpack[RefreshTrustedAdvisorCheckRequestRequestTypeDef]
    ) -> RefreshTrustedAdvisorCheckResponseTypeDef:
        """
        Refreshes the Trusted Advisor check that you specify using the check ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/refresh_trusted_advisor_check.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#refresh_trusted_advisor_check)
        """

    async def resolve_case(
        self, **kwargs: Unpack[ResolveCaseRequestRequestTypeDef]
    ) -> ResolveCaseResponseTypeDef:
        """
        Resolves a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/resolve_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#resolve_case)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_cases"]) -> DescribeCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_communications"]
    ) -> DescribeCommunicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#get_paginator)
        """

    async def __aenter__(self) -> "SupportClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
        """
