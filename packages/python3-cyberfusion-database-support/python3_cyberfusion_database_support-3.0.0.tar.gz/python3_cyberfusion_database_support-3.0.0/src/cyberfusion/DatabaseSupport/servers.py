"""Classes for interaction with database servers."""

import re
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:  # pragma: no cover
    from cyberfusion.DatabaseSupport import DatabaseSupport

from sqlalchemy.sql import text

from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant
from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from cyberfusion.DatabaseSupport.databases import Database
from cyberfusion.DatabaseSupport.queries import Query
from cyberfusion.DatabaseSupport.tables import Table


class Server:
    """Abstract representation of database server."""

    MYSQL_NAME_DATABASE_INFORMATION_SCHEMA = "information_schema"
    MYSQL_NAME_DATABASE_PERFORMANCE_SCHEMA = "performance_schema"
    MYSQL_NAME_DATABASE_MYSQL = "mysql"
    MYSQL_NAME_DATABASE_SYS = "sys"

    POSTGRESQL_NAME_DATABASE_TEMPLATE0 = "template0"
    POSTGRESQL_NAME_DATABASE_TEMPLATE1 = "template1"
    POSTGRESQL_NAME_DATABASE_POSTGRES = "postgres"

    MYSQL_NAME_USER_MONITORING = "monitoring"
    MYSQL_NAME_USER_DEBIAN_SYS_MAINT = "debian-sys-maint"
    MYSQL_NAME_USER_MARIADB_SYS = "mariadb.sys"
    MYSQL_NAME_USER_MYSQL = "mysql"

    POSTGRESQL_NAME_USER_ADMIN = "admin"
    POSTGRESQL_NAME_USER_POSTGRES = "postgres"
    POSTGRESQL_PREFIX_SYSTEM_USER = "pg_"

    def __init__(self, *, support: "DatabaseSupport") -> None:
        """Set attributes and call functions to handle server."""
        self.support = support

    @property
    def _databases_mariadb(self) -> List[Database]:
        """Get MariaDB databases."""
        databases: List[Database] = []

        for database_name in self.support.engines.inspectors[
            self.support.engines.MYSQL_ENGINE_NAME
        ].get_schema_names():
            if database_name in [
                self.MYSQL_NAME_DATABASE_MYSQL,
                self.MYSQL_NAME_DATABASE_PERFORMANCE_SCHEMA,
                self.MYSQL_NAME_DATABASE_INFORMATION_SCHEMA,
                self.MYSQL_NAME_DATABASE_SYS,
            ]:
                continue

            databases.append(
                Database(
                    support=self.support,
                    name=database_name,
                    server_software_name=self.support.MARIADB_SERVER_SOFTWARE_NAME,
                )
            )

        return databases

    @property
    def _databases_postgresql(self) -> List[Database]:
        """Get PostgreSQL databases."""
        databases: List[Database] = []

        for database_name in Query(
            engine=self.support.engines.engines[
                self.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query="SELECT datname FROM pg_database;",
        ).result:
            database_name = database_name[0]

            if database_name in [
                self.POSTGRESQL_NAME_DATABASE_TEMPLATE0,
                self.POSTGRESQL_NAME_DATABASE_TEMPLATE1,
                self.POSTGRESQL_NAME_DATABASE_POSTGRES,
            ]:
                continue

            databases.append(
                Database(
                    support=self.support,
                    name=database_name,
                    server_software_name=self.support.POSTGRESQL_SERVER_SOFTWARE_NAME,
                )
            )

        return databases

    @property
    def databases(self) -> List[Database]:
        """Get databases."""
        databases: List[Database] = []

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            databases.extend(self._databases_mariadb)

        if (
            self.support.POSTGRESQL_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            databases.extend(self._databases_postgresql)

        return databases

    @property
    def _mariadb_database_user_grants(self) -> List[DatabaseUserGrant]:
        """Get MariaDB database user grants."""
        database_user_grants: List[DatabaseUserGrant] = []

        for database_user in self.database_users:
            for grant in Query(
                engine=self.support.engines.engines[
                    self.support.engines.MYSQL_ENGINE_NAME
                ],
                query=text("SHOW GRANTS FOR :username@:host;").bindparams(
                    username=database_user.name, host=database_user.host
                ),
            ).result:
                # Parse grant

                parsed_grant = re.match(
                    """GRANT (.+) ON (.+) TO (['`"]).*\\3@(['`"]).*\\4( IDENTIFIED BY PASSWORD (['`"]).+\\6)? ?(.*)""",
                    grant[0],
                )

                if not parsed_grant:
                    raise RuntimeError

                if (
                    parsed_grant.group(1) == "PROXY"
                ):  # PROXY grants have a syntax that we don't support
                    continue

                parsed_part = re.fullmatch(
                    r"[`]?(.+?)[`]?\.[`]?(.+?)[`]?", parsed_grant.group(2)
                )

                if not parsed_part:
                    raise RuntimeError

                database_name = parsed_part.group(1)
                table_name = parsed_part.group(2)
                privilege_names = [x.strip() for x in parsed_grant.group(1).split(",")]

                # Use short version of 'ALL PRIVILEGES'

                for index, privilege_name in enumerate(privilege_names):
                    if privilege_name != DatabaseUserGrant.LONG_ALL_PRIVILEGES:
                        continue

                    privilege_names[index] = DatabaseUserGrant.SHORT_ALL_PRIVILEGES

                # Get database object

                database = Database(
                    support=self.support,
                    name=database_name,
                    server_software_name=database_user.server_software_name,
                )

                # Get table object

                table = None

                if table_name != DatabaseUserGrant.CHAR_NAME_TABLE_WILDCARD:
                    table = Table(
                        database=database,
                        name=table_name,
                    )

                database_user_grants.append(
                    DatabaseUserGrant(
                        database=database,
                        database_user=database_user,
                        privilege_names=privilege_names,
                        table=table,
                    )
                )

        return database_user_grants

    @property
    def database_user_grants(self) -> List[DatabaseUserGrant]:
        """Get database user grants."""
        database_user_grants: List[DatabaseUserGrant] = []

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            database_user_grants.extend(self._mariadb_database_user_grants)

        return database_user_grants

    @property
    def _mariadb_database_users(self) -> List[DatabaseUser]:
        """Get MariaDB database users."""
        database_users: List[DatabaseUser] = []

        for database_user in Query(
            engine=self.support.engines.engines[self.support.engines.MYSQL_ENGINE_NAME],
            query=text("SELECT User,Host,Password from mysql.user;"),
        ).result:
            database_user_name = database_user[0]
            database_user_host = database_user[1]
            database_user_password = database_user[2]

            if database_user_name in [
                self.MYSQL_NAME_USER_MONITORING,
                self.MYSQL_NAME_USER_DEBIAN_SYS_MAINT,
                self.MYSQL_NAME_USER_MARIADB_SYS,
                self.MYSQL_NAME_USER_MYSQL,
            ]:
                continue

            database_users.append(
                DatabaseUser(
                    server=self,
                    name=database_user_name,
                    server_software_name=self.support.MARIADB_SERVER_SOFTWARE_NAME,
                    password=database_user_password,
                    host=database_user_host,
                )
            )

        return database_users

    @property
    def _postgresql_database_users(self) -> List[DatabaseUser]:
        """Get PostgreSQL database users."""
        database_users: List[DatabaseUser] = []

        for database_user in Query(
            engine=self.support.engines.engines[
                self.support.engines.POSTGRESQL_ENGINE_NAME
            ],
            query=text("SELECT rolname FROM pg_catalog.pg_roles;"),
        ).result:
            database_user_name = database_user[0]

            if database_user_name in [
                self.POSTGRESQL_NAME_USER_ADMIN,
                self.POSTGRESQL_NAME_USER_POSTGRES,
            ]:
                continue

            if database_user_name.startswith(self.POSTGRESQL_PREFIX_SYSTEM_USER):
                continue

            password = Query(
                engine=self.support.engines.engines[
                    self.support.engines.POSTGRESQL_ENGINE_NAME
                ],
                query=text(
                    "SELECT rolpassword FROM pg_authid WHERE rolname=:rolname;"
                ).bindparams(rolname=database_user_name),
            ).result.first()[0]

            database_users.append(
                DatabaseUser(
                    server=self,
                    name=database_user_name,
                    server_software_name=self.support.POSTGRESQL_SERVER_SOFTWARE_NAME,
                    password=password,
                    host=None,
                )
            )

        return database_users

    @property
    def database_users(self) -> List[DatabaseUser]:
        """Get database users."""
        database_users: List[DatabaseUser] = []

        if (
            self.support.MARIADB_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            database_users.extend(self._mariadb_database_users)

        if (
            self.support.POSTGRESQL_SERVER_SOFTWARE_NAME
            in self.support.server_software_names
        ):
            database_users.extend(self._postgresql_database_users)

        return database_users
