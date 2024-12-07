"""Classes for interaction with database engines."""

import os
from typing import TYPE_CHECKING, Dict

import sqlalchemy as sa
from cached_property import cached_property

from cyberfusion.DatabaseSupport.servers import Server
from cyberfusion.DatabaseSupport.utilities import _generate_mariadb_dsn

if TYPE_CHECKING:  # pragma: no cover
    from cyberfusion.DatabaseSupport import DatabaseSupport


class Engines:
    """Abstract representation of database engines."""

    MYSQL_NAME_USER_DEFAULT = "root"
    MYSQL_HOST_DEFAULT = os.path.join(os.path.sep, "run", "mysqld", "mysqld.sock")

    POSTGRESQL_NAME_USER_DEFAULT = "root"
    POSTGRESQL_HOST_DEFAULT = ""

    MYSQL_ENGINE_NAME = "mysql"
    POSTGRESQL_ENGINE_NAME = "postgresql"

    def __init__(
        self,
        *,
        support: "DatabaseSupport",
    ) -> None:
        """Set attributes and call functions to handle engine."""
        self.support = support

    @property
    def _postgresql_url(self) -> str:
        """Get engine URL for PostgreSQL."""
        if not self.support.server_password:
            return f"postgresql+psycopg2://{self.support.postgresql_server_username}@{self.support.postgresql_server_host}/{Server.POSTGRESQL_NAME_DATABASE_POSTGRES}"

        return f"postgresql+psycopg2://{self.support.postgresql_server_username}:{self.support.server_password}@{self.support.postgresql_server_host}/{Server.POSTGRESQL_NAME_DATABASE_POSTGRES}"

    @property
    def _mariadb_url(self) -> str:
        """Get engine URL for MariaDB."""
        return _generate_mariadb_dsn(
            username=self.support.mariadb_server_username,
            host=self.support.mariadb_server_host,
            password=self.support.server_password,
            database_name=None,
        )

    @property
    def urls(self) -> Dict[str, str]:
        """Get engine URLs."""
        urls: Dict[str, str] = {}

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            urls[self.MYSQL_ENGINE_NAME] = self._mariadb_url

        if (
            self.support.POSTGRESQL_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            urls[self.POSTGRESQL_ENGINE_NAME] = self._postgresql_url

        return urls

    @cached_property
    def engines(self) -> Dict[str, sa.engine.base.Engine]:
        """Create engines."""
        engines: Dict[str, sa.engine.base.Engine] = {}

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            engines[self.MYSQL_ENGINE_NAME] = sa.create_engine(
                self.urls[self.MYSQL_ENGINE_NAME]
            )

        if (
            self.support.POSTGRESQL_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            engines[self.POSTGRESQL_ENGINE_NAME] = sa.create_engine(
                self.urls[self.POSTGRESQL_ENGINE_NAME]
            )

        return engines

    @cached_property
    def inspectors(self) -> Dict[str, sa.dialects.postgresql.base.PGInspector]:
        """Get engines inspectors."""
        inspectors: Dict[str, sa.dialects.postgresql.base.PGInspector] = {}

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            inspectors[self.MYSQL_ENGINE_NAME] = sa.inspect(
                self.engines[self.MYSQL_ENGINE_NAME]
            )

        return inspectors
