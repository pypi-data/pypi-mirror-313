"""Classes for importing databases."""

from cached_property import cached_property

from cyberfusion.Common import hash_string_mariadb
from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant
from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from cyberfusion.DatabaseSupport.databases import Database
from cyberfusion.DatabaseSupport.exceptions import ServerNotSupportedError
from cyberfusion.DatabaseSupport.servers import Server
from cyberfusion.DatabaseSupport.utilities import generate_random_string


class DatabaseImportation:
    """Abstraction of database importation process.

    Restores dump from file to given database.

    This class differs from the Database.load method. As a convenience, among
    others, this class creates a user for importing the database (as doing it
    as root is not optimal from a security standpoint).

    A database user will be created, as well as a grant for the specified database.
    The created user will be able to access the specified database only. Use this
    user to import the database. This is safer than importing the database as the
    default (usually root) user.

    The class contains unprivileged and privileged attributes. These are used
    for creating the objects, as unprivileged users cannot do this. Unprivileged
    attributes are used to import the database.
    """

    NAME_ACCESS_HOST = "localhost"

    def __init__(
        self,
        *,
        privileged_support: DatabaseSupport,
        server_software_name: str,
        database_name: str,
        source_path: str,
    ) -> None:
        """Set attributes."""
        self.privileged_support = privileged_support
        self.server_software_name = server_software_name
        self.database_name = database_name
        self.source_path = source_path

        # Raise if server software not supported

        if self.server_software_name not in [
            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
        ]:
            raise ServerNotSupportedError

    @cached_property
    def unprivileged_support(self) -> DatabaseSupport:
        """Get support."""
        return DatabaseSupport(
            server_software_names=[self.server_software_name],
            server_password=self.unhashed_password,
            mariadb_server_username=self.username,
            mariadb_server_host=self.privileged_support.mariadb_server_host,
        )

    @cached_property
    def privileged_server(self) -> Server:
        """Get server."""
        return Server(support=self.privileged_support)

    @cached_property
    def privileged_database(self) -> Database:
        """Get database."""
        return Database(
            support=self.privileged_support,
            name=self.database_name,
            server_software_name=self.server_software_name,
        )

    @cached_property
    def unprivileged_database(self) -> Database:
        """Get database."""
        return Database(
            support=self.unprivileged_support,
            name=self.database_name,
            server_software_name=self.server_software_name,
        )

    @cached_property
    def database_user(self) -> DatabaseUser:
        """Get temporary database user."""
        return DatabaseUser(
            server=self.privileged_server,
            name=self.username,
            server_software_name=self.server_software_name,
            password=self.hashed_password,
            # Database user has localhost as host, as remote access is not
            # required (the import will run locally).
            host=self.NAME_ACCESS_HOST,
        )

    @cached_property
    def database_user_grant(self) -> DatabaseUserGrant:
        """Get temporary database user grant."""
        return DatabaseUserGrant(
            database=self.privileged_database,
            database_user=self.database_user,
            privilege_names=[DatabaseUserGrant.SHORT_ALL_PRIVILEGES],
            table=None,
        )

    @cached_property
    def username(self) -> str:
        """Username for temporary database user."""
        return f"restore-{generate_random_string().lower()}"

    @cached_property
    def unhashed_password(self) -> str:
        """Get unhashed password for temporary database user."""
        return generate_random_string()

    @cached_property
    def hashed_password(self) -> str:
        """Get hashed password for temporary database user."""
        return hash_string_mariadb(string=self.unhashed_password)

    def _create_objects(self) -> None:
        """Create temporary objects."""
        self.database_user.create()
        self.database_user_grant.grant()

    def _delete_objects(self) -> None:
        """Delete temporary objects."""
        self.database_user.drop()  # Cascading delete for database user grants

    def load(self) -> None:
        """Load (import) database."""
        self._create_objects()

        with open(self.source_path, "r") as f:
            self.unprivileged_database.load(dump_file=f)

        self._delete_objects()
