"""Classes for interaction with database user grants."""

import re
from typing import List, Optional

from sqlalchemy.sql import text

from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from cyberfusion.DatabaseSupport.databases import Database
from cyberfusion.DatabaseSupport.exceptions import (
    InvalidInputError,
    ServerNotSupportedError,
)
from cyberfusion.DatabaseSupport.queries import Query
from cyberfusion.DatabaseSupport.tables import Table
from cyberfusion.DatabaseSupport.utilities import object_not_exists, object_exists


class DatabaseUserGrant:
    """Abstract representation of database user grant."""

    LONG_ALL_PRIVILEGES = "ALL PRIVILEGES"
    SHORT_ALL_PRIVILEGES = "ALL"

    CHAR_NAME_TABLE_WILDCARD = "*"
    CHAR_NAME_DATABASE_WILDCARD = "*"

    def __init__(
        self,
        *,
        database: Database,
        database_user: DatabaseUser,
        privilege_names: List[str],
        table: Optional[Table],
    ) -> None:
        """Raise exception if server software not supported, set attributes, and call functions to handle database user grant."""
        self.database = database
        self.database_user = database_user
        self.privilege_names = privilege_names
        self.database_name = self.database.name

        self.table_name: Optional[str] = None  # type: ignore[assignment]

        if table is not None:
            self.table_name = table.name

        # Raise if server software not supported

        if self.database_user.server_software_name not in [
            self.database.support.MARIADB_SERVER_SOFTWARE_NAME
        ]:
            raise ServerNotSupportedError

    @property
    def database_name(self) -> str:
        """Get database name."""
        return self._database_name

    @database_name.setter
    def database_name(self, value: str) -> None:
        """Set database name."""
        if value == self.CHAR_NAME_DATABASE_WILDCARD:
            self._database_name = value

            return

        # Variable must be alphanumeric to prevent SQL injection; DDL statements
        # do not support quoted identifiers

        if not re.match(r"^[a-zA-Z0-9-_%\\]+$", value):
            raise InvalidInputError(value)

        self._database_name = value

    @property
    def privilege_names(self) -> List[str]:
        """Get privilege names."""
        return self._privilege_names

    @privilege_names.setter
    def privilege_names(self, value: List[str]) -> None:
        """Set privilege names."""
        for variable in value:
            # Variable must be alphanumeric to prevent SQL injection; DDL statements
            # do not support quoted identifiers

            if re.match(r"^[a-zA-Z0-9-_ ]+$", variable):
                continue

            raise InvalidInputError(variable)

        self._privilege_names = value

    @property
    def table_name(self) -> str:
        """Get table name."""
        return self._table_name

    @table_name.setter
    def table_name(self, value: Optional[str]) -> None:
        """Set table name."""

        # If table name is not set, it covers all tables ('*')

        if value is None:
            self._table_name = self.CHAR_NAME_TABLE_WILDCARD

            return

        self._table_name = value

    @property
    def exists(self) -> bool:
        """Get database user grant exists locally."""
        for database_user_grant in self.database_user.server.database_user_grants:
            if database_user_grant.table_name != self.table_name:
                continue

            if database_user_grant.privilege_names != self.privilege_names:
                continue

            if database_user_grant.database_user.name != self.database_user.name:
                continue

            if database_user_grant.database_user.host != self.database_user.host:
                continue

            if database_user_grant.database.name != self.database_name:
                continue

            return True

        return False

    @property
    def text_table_name(self) -> str:
        """Get table name for use in query.

        If table name is not wildcard, it should be quoted.
        """
        if self.table_name == self.CHAR_NAME_TABLE_WILDCARD:
            return self.table_name

        return "`" + self.table_name + "`"

    @property
    def text_privilege_names(self) -> str:
        """Get privilege names for use in query."""
        return ", ".join(self.privilege_names)

    @object_not_exists
    def grant(self) -> bool:
        """Create database user grant."""
        Query(
            engine=self.database_user.server.support.engines.engines[
                self.database.support.engines.MYSQL_ENGINE_NAME
            ],
            query=text(
                f"GRANT {self.text_privilege_names} ON `{self.database_name}`.{self.text_table_name} TO :database_user_name@:database_user_host;"
            ).bindparams(
                database_user_name=self.database_user.name,
                database_user_host=self.database_user.host,
            ),
        )

        return True

    @object_exists
    def revoke(self) -> bool:
        """Delete database user grant."""
        Query(
            engine=self.database_user.server.support.engines.engines[
                self.database.support.engines.MYSQL_ENGINE_NAME
            ],
            query=text(
                f"REVOKE {self.text_privilege_names} ON `{self.database_name}`.{self.text_table_name} FROM :database_user_name@:database_user_host;"
            ).bindparams(
                database_user_name=self.database_user.name,
                database_user_host=self.database_user.host,
            ),
        )

        return True
