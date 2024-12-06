"""
Type annotations for ssm-quicksetup service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_ssm_quicksetup.client import SystemsManagerQuickSetupClient
    from types_boto3_ssm_quicksetup.paginator import (
        ListConfigurationManagersPaginator,
        ListConfigurationsPaginator,
    )

    session = Session()
    client: SystemsManagerQuickSetupClient = session.client("ssm-quicksetup")

    list_configuration_managers_paginator: ListConfigurationManagersPaginator = client.get_paginator("list_configuration_managers")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef,
    ListConfigurationManagersOutputTypeDef,
    ListConfigurationsInputListConfigurationsPaginateTypeDef,
    ListConfigurationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListConfigurationManagersPaginator", "ListConfigurationsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListConfigurationManagersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef],
    ) -> _PageIterator[ListConfigurationManagersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
        """

class ListConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/paginators/#listconfigurationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConfigurationsInputListConfigurationsPaginateTypeDef]
    ) -> _PageIterator[ListConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/paginators/#listconfigurationspaginator)
        """
