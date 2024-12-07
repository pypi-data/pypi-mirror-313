"""Helper classes for scripts for clusters of database type."""

from typing import List, Optional

from cyberfusion.DatabaseSupport.engines import Engines


class DatabaseSupport:
    """Helper class for local support modules."""

    MARIADB_SERVER_SOFTWARE_NAME = "MariaDB"
    POSTGRESQL_SERVER_SOFTWARE_NAME = "PostgreSQL"

    EXTENSION_FILE_SQL = "sql"

    def __init__(
        self,
        *,
        server_software_names: List[str],
        server_password: Optional[str] = None,
        mariadb_server_host: str = Engines.MYSQL_HOST_DEFAULT,
        postgresql_server_host: str = Engines.POSTGRESQL_HOST_DEFAULT,
        mariadb_server_username: str = Engines.MYSQL_NAME_USER_DEFAULT,
        postgresql_server_username: str = Engines.POSTGRESQL_NAME_USER_DEFAULT,
    ) -> None:
        """Set information."""
        self.server_software_names = server_software_names
        self.server_password = server_password
        self.mariadb_server_host = mariadb_server_host
        self.postgresql_server_host = postgresql_server_host
        self.mariadb_server_username = mariadb_server_username
        self.postgresql_server_username = postgresql_server_username

        self.engines = Engines(support=self)
