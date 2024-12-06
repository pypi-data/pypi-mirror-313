from __future__ import annotations

from dataclasses import KW_ONLY
from typing import final

from atoti._collections import FrozenMapping, frozendict
from atoti._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from pydantic.dataclasses import dataclass

from ._connection_config import ConnectionConfig


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class UserContentStorageConfig(ConnectionConfig):
    """The config for storing user content in a separate database.

    Example:
        >>> from atoti_jdbc import UserContentStorageConfig
        >>> config = UserContentStorageConfig(
        ...     "mysql://localhost:7777/example?user=username&password=passwd"
        ... )

    """

    _: KW_ONLY

    hibernate_options: FrozenMapping[str, str] = frozendict()
    """Extra options to pass to Hibernate.

    See `AvailableSettings <https://javadoc.io/static/org.hibernate/hibernate-core/5.6.15.Final/org/hibernate/cfg/AvailableSettings.html>`__.
    """
