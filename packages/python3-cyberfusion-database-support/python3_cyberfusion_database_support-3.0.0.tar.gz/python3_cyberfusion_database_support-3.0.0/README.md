# python3-cyberfusion-database-support

Library for MariaDB and PostgreSQL.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-database-support

Next, install PostgreSQL according to the [documentation](https://www.postgresql.org/download/macosx/) (provides `pg_config`, required by `psycopg2`).

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

See code.
