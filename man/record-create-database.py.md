## SYNOPSIS

`record-create-database.py`

## DESCRIPTION

`record-create-database.py` initialises the relational database schema for the
RECORD provenance system. It connects to the configured database, creates
all entity tables defined by the `record` library if they do not already
exist, and then disconnects.

The script is a no-op when the database backend is Gremlin (`RECORD_DBTYPE=gremlin`),
since schema creation is meaningless for a graph database. In that case a
diagnostic message is written to standard error and the script exits
without making any changes.

`record-create-database.py` is called automatically by `record.sh` during its
initialisation sequence to ensure the schema is in place before any
provenance recording begins. It may also be invoked directly to set up a
fresh database outside of a workflow run.

## OPTIONS

This command takes no command-line options.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if the database connection fails or if table creation
raises an unhandled exception.

## ENVIRONMENT

The script inherits all database connection environment variables from the
`record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3` or `postgres`. If set to
  `gremlin` the script exits without creating any tables.

`RECORD_DBFILE`
: Path to the SQLite database file. Used when `RECORD_DBTYPE` is `sqlite3`.

`RECORD_DBUSER`
: PostgreSQL username. Used when `RECORD_DBTYPE` is `postgres`.

`RECORD_DBNAME`
: PostgreSQL database name. Used when `RECORD_DBTYPE` is `postgres`.

`RECORD_POSTGRES_HOST`
: PostgreSQL hostname.

`RECORD_POSTGRES_PORT`
: PostgreSQL port number.

`RECORD_POSTGRES_PASSWORD`
: PostgreSQL password. Required when `RECORD_DBTYPE` is `postgres`.

`RECORD_DEBUG`
: When set, enables verbose diagnostic output to standard error.

## RETURN VALUE

None.

## EXAMPLES

Initialise a SQLite database in the current directory:

    RECORD_DBTYPE=sqlite3 RECORD_DBFILE=ssrepi.db record-create-database.py

Initialise a PostgreSQL database:

    RECORD_DBTYPE=postgres \
    RECORD_DBUSER=myuser \
    RECORD_DBNAME=ssrepi \
    RECORD_POSTGRES_PASSWORD=secret \
    record-create-database.py

Typical workflow usage (called automatically by `record.sh`):

    source record.sh
    # record-create-database.py has already been called at this point

## FILES

`lib/record.py`
: The RECORD provenance library providing `connect_db`, `create_tables`,
  and `disconnect_db`. Must be present in a `lib` subdirectory relative to
  the working directory, or otherwise on the Python path.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

Debug output is controlled by the `record.debug` flag, which is
unconditionally set to `True` inside `record.py` regardless of the
`RECORD_DEBUG` environment variable. As a result diagnostic messages are
always written to standard error.

The script takes no action and produces no error when `RECORD_DBTYPE` is
`gremlin`, but it still exits with status 0 rather than a non-zero status
that would indicate to the caller that no initialisation was performed.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-run.sh`, `record-clean.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide a single-command
means of initialising the provenance database schema prior to running
social simulation experiments.
