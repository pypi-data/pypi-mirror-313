"""Classes for interaction with database users."""

import re
from typing import TYPE_CHECKING, Optional

from sqlalchemy.sql import text

from cyberfusion.DatabaseSupport.exceptions import (
    InvalidInputError,
    PasswordMissingError,
)
from cyberfusion.DatabaseSupport.queries import Query
from cyberfusion.DatabaseSupport.utilities import (
    object_exists,
    object_not_exists,
)

if TYPE_CHECKING:  # pragma: no cover
    from cyberfusion.DatabaseSupport.servers import Server


class DatabaseUser:
    """Abstract representation of database user."""

    def __init__(
        self,
        *,
        server: "Server",
        name: str,
        server_software_name: str,
        password: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        """Set attributes and call functions to handle database user."""
        self.server = server
        self.name = name
        self.server_software_name = server_software_name
        self.password = password
        self._host = host

    def _get_password(self) -> str:
        """Get password of database user on server."""
        if (
            self.server_software_name
            == self.server.support.MARIADB_SERVER_SOFTWARE_NAME
        ):
            return Query(
                engine=self.server.support.engines.engines[
                    self.server.support.engines.MYSQL_ENGINE_NAME
                ],
                query=text(
                    "SELECT Password from mysql.user WHERE User=:name AND Host=:host;"
                ).bindparams(name=self.name, host=self.host),
            ).result.first()[0]

        return Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query=text(
                "SELECT rolpassword FROM pg_authid WHERE rolname=:rolname;"
            ).bindparams(rolname=self.name),
        ).result.first()[0]

    @property
    def name(self) -> str:
        """Get name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set name."""

        # Variable must be alphanumeric to prevent SQL injection; DDL statements
        # do not support quoted identifiers

        if not re.match(r"^[a-zA-Z0-9-_]+$", value):
            raise InvalidInputError(value)

        self._name = value

    @property
    def host(self) -> Optional[str]:
        """Get host."""
        if (
            self.server_software_name
            != self.server.support.POSTGRESQL_SERVER_SOFTWARE_NAME
        ):
            return self._host

        return None

    @property
    def exists(self) -> bool:
        """Get database user exists locally."""
        for database_user in self.server.database_users:
            if database_user.name != self.name:
                continue

            if database_user.host != self.host:
                continue

            return True

        return False

    def _create_mariadb(self) -> None:
        """Create database user for MariaDB."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.MYSQL_ENGINE_NAME
            ],
            query=text(
                "CREATE USER :name@:host IDENTIFIED BY PASSWORD :password;"
            ).bindparams(name=self.name, host=self.host, password=self.password),
        )

    def _create_postgresql(self) -> None:
        """Create database user for PostgreSQL."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query=text(f"CREATE USER {self.name} WITH PASSWORD :password;").bindparams(
                password=self.password
            ),
        )

    @object_not_exists
    def create(self) -> bool:
        """Create database user."""
        if not self.password:
            raise PasswordMissingError

        if (
            self.server_software_name
            == self.server.support.MARIADB_SERVER_SOFTWARE_NAME
        ):
            self._create_mariadb()

            return True

        self._create_postgresql()

        return True

    def _drop_mariadb(self) -> None:
        """Delete database user for MariaDB."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.MYSQL_ENGINE_NAME
            ],
            query=text("DROP USER :name@:host;").bindparams(
                name=self.name, host=self.host
            ),
        )

    def _drop_postgresql(self) -> None:
        """Delete database user for PostgreSQL."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query=text(f"DROP USER {self.name};").bindparams(),
        )

    @object_exists
    def drop(self) -> bool:
        """Delete database user."""

        # Delete database user

        if (
            self.server_software_name
            == self.server.support.MARIADB_SERVER_SOFTWARE_NAME
        ):
            self._drop_mariadb()

            return True

        self._drop_postgresql()

        return True

    def _edit_mariadb(self) -> None:
        """Edit database user password for MariaDB."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.MYSQL_ENGINE_NAME
            ],
            query=text(
                "ALTER USER :name@:host IDENTIFIED BY PASSWORD :password;"
            ).bindparams(
                name=self.name,
                host=self.host,
                password=self.password,
            ),
        )

    def _edit_postgresql(self) -> None:
        """Edit database user password for PostgreSQL."""
        Query(
            engine=self.server.support.engines.engines[
                self.server.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query=text(f"ALTER USER {self.name} WITH PASSWORD :password;").bindparams(
                password=self.password
            ),
        )

    def edit(self) -> bool:
        """Edit database user."""
        if not self.password:
            raise PasswordMissingError

        if self._get_password() == self.password:
            return False

        if (
            self.server_software_name
            == self.server.support.MARIADB_SERVER_SOFTWARE_NAME
        ):
            self._edit_mariadb()

            return True

        self._edit_postgresql()

        return True
