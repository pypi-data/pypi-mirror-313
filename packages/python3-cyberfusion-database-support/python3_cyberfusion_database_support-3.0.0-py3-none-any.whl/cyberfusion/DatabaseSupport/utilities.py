"""Generic utilities."""

import os
import secrets
import string
from typing import Any, Callable, Optional, TypeVar, Union, cast

F = TypeVar("F", bound=Callable[..., Any])


def object_exists(f: F) -> Union[bool, F]:
    """Require object to exist, return False otherwise."""

    def wrapper(self: Any, *args: tuple, **kwargs: dict) -> Union[bool, F]:
        if not self.exists:
            return False

        return f(self, *args, **kwargs)

    return cast(F, wrapper)


def object_not_exists(f: F) -> Union[bool, F]:
    """Require object to not exist, return False otherwise."""

    def wrapper(self: Any, *args: tuple, **kwargs: dict) -> Union[bool, F]:
        if self.exists:
            return False

        return f(self, *args, **kwargs)

    return cast(F, wrapper)


def get_host_is_socket(host: str) -> bool:
    """Check if host is socket."""
    return os.path.sep in host


def _generate_mariadb_dsn(
    *,
    username: str,
    host: str,
    password: Optional[str] = None,
    database_name: Optional[str] = None,
) -> str:
    """Generate MariaDB DSN."""
    _host_is_socket = get_host_is_socket(host)

    string = f"mysql+pymysql://{username}"

    if password:
        string += f":{password}"

    if not _host_is_socket:
        string += f"@{host}"
    else:
        string += "@"

    if database_name:
        string += f"/{database_name}"
    else:
        if _host_is_socket:
            string += "/"

    if _host_is_socket:
        string += f"?unix_socket={host}"

    return string


def generate_random_string() -> str:
    """Generate random string."""
    length = 8

    return "".join(secrets.choice(string.ascii_lowercase) for _ in range(length))
