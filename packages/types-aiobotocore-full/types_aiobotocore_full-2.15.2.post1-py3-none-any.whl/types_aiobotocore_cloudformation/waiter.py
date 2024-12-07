"""
Type annotations for cloudformation service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudformation.client import CloudFormationClient
    from types_aiobotocore_cloudformation.waiter import (
        ChangeSetCreateCompleteWaiter,
        StackCreateCompleteWaiter,
        StackDeleteCompleteWaiter,
        StackExistsWaiter,
        StackImportCompleteWaiter,
        StackRollbackCompleteWaiter,
        StackUpdateCompleteWaiter,
        TypeRegistrationCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("cloudformation") as client:
        client: CloudFormationClient

        change_set_create_complete_waiter: ChangeSetCreateCompleteWaiter = client.get_waiter("change_set_create_complete")
        stack_create_complete_waiter: StackCreateCompleteWaiter = client.get_waiter("stack_create_complete")
        stack_delete_complete_waiter: StackDeleteCompleteWaiter = client.get_waiter("stack_delete_complete")
        stack_exists_waiter: StackExistsWaiter = client.get_waiter("stack_exists")
        stack_import_complete_waiter: StackImportCompleteWaiter = client.get_waiter("stack_import_complete")
        stack_rollback_complete_waiter: StackRollbackCompleteWaiter = client.get_waiter("stack_rollback_complete")
        stack_update_complete_waiter: StackUpdateCompleteWaiter = client.get_waiter("stack_update_complete")
        type_registration_complete_waiter: TypeRegistrationCompleteWaiter = client.get_waiter("type_registration_complete")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeChangeSetInputChangeSetCreateCompleteWaitTypeDef,
    DescribeStacksInputStackCreateCompleteWaitTypeDef,
    DescribeStacksInputStackDeleteCompleteWaitTypeDef,
    DescribeStacksInputStackExistsWaitTypeDef,
    DescribeStacksInputStackImportCompleteWaitTypeDef,
    DescribeStacksInputStackRollbackCompleteWaitTypeDef,
    DescribeStacksInputStackUpdateCompleteWaitTypeDef,
    DescribeTypeRegistrationInputTypeRegistrationCompleteWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ChangeSetCreateCompleteWaiter",
    "StackCreateCompleteWaiter",
    "StackDeleteCompleteWaiter",
    "StackExistsWaiter",
    "StackImportCompleteWaiter",
    "StackRollbackCompleteWaiter",
    "StackUpdateCompleteWaiter",
    "TypeRegistrationCompleteWaiter",
)


class ChangeSetCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/ChangeSetCreateComplete.html#CloudFormation.Waiter.ChangeSetCreateComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#changesetcreatecompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeChangeSetInputChangeSetCreateCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/ChangeSetCreateComplete.html#CloudFormation.Waiter.ChangeSetCreateComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#changesetcreatecompletewaiter)
        """


class StackCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackCreateComplete.html#CloudFormation.Waiter.StackCreateComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackcreatecompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeStacksInputStackCreateCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackCreateComplete.html#CloudFormation.Waiter.StackCreateComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackcreatecompletewaiter)
        """


class StackDeleteCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackDeleteComplete.html#CloudFormation.Waiter.StackDeleteComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackdeletecompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeStacksInputStackDeleteCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackDeleteComplete.html#CloudFormation.Waiter.StackDeleteComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackdeletecompletewaiter)
        """


class StackExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackExists.html#CloudFormation.Waiter.StackExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackexistswaiter)
    """

    async def wait(self, **kwargs: Unpack[DescribeStacksInputStackExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackExists.html#CloudFormation.Waiter.StackExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackexistswaiter)
        """


class StackImportCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackImportComplete.html#CloudFormation.Waiter.StackImportComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackimportcompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeStacksInputStackImportCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackImportComplete.html#CloudFormation.Waiter.StackImportComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackimportcompletewaiter)
        """


class StackRollbackCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRollbackComplete.html#CloudFormation.Waiter.StackRollbackComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrollbackcompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeStacksInputStackRollbackCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackRollbackComplete.html#CloudFormation.Waiter.StackRollbackComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackrollbackcompletewaiter)
        """


class StackUpdateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackUpdateComplete.html#CloudFormation.Waiter.StackUpdateComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackupdatecompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeStacksInputStackUpdateCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/StackUpdateComplete.html#CloudFormation.Waiter.StackUpdateComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#stackupdatecompletewaiter)
        """


class TypeRegistrationCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/TypeRegistrationComplete.html#CloudFormation.Waiter.TypeRegistrationComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#typeregistrationcompletewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeTypeRegistrationInputTypeRegistrationCompleteWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/waiter/TypeRegistrationComplete.html#CloudFormation.Waiter.TypeRegistrationComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/waiters/#typeregistrationcompletewaiter)
        """
