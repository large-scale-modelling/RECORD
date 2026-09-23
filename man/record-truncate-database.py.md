## SYNOPSIS

`record-truncate-database.py` `--force`

## DESCRIPTION

`record-truncate-database.py` removes all rows from every table in the
RECORD provenance database without dropping the schema. It is a
destructive maintenance utility and requires explicit confirmation via
`--force` before any write is performed.

The script is only meaningful for relational backends. If
`RECORD_DBTYPE` is `gremlin`, the script exits with an advisory message
directing the user to `delete-database.py` instead, as truncation is not
a applicable concept for a graph database.

## OPTIONS

`--force`
: Required. Instructs the script to proceed with truncation. Without
  this flag the script prints a refusal message to standard error and
  exits with status 1.

## EXIT STATUS

Returns 0 on success.

Returns 1 if:

- `--force` is not supplied; or
- `RECORD_DBTYPE` is `gremlin` (advisory exit, no truncation attempted).

Returns non-zero if:

- the `record` library cannot be imported from `lib/`; or
- a database error occurs during `empty_tables`, `connect_db`, or
  `disconnect_db`.

## ENVIRONMENT

The script inherits all database connection environment variables from the
`record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or
  `gremlin`. If set to `gremlin`, truncation is skipped and an advisory
  message is printed.

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

This script produces no output on success. Diagnostic messages are
written to standard error when debug mode is active or when truncation
is refused.

## EXAMPLES

Truncate all tables in the database:

    record-truncate-database.py --force

Attempt truncation without confirmation (will be refused):

    record-truncate-database.py

## FILES

`lib/record.py`
: The RECORD provenance library. Must be importable as `record`; the
  script appends `lib` to `sys.path` before importing, so `record.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

## AUTHORS

Doug Salt

## CREDITS

Gary Polhill, Lorenzo Milazzo

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

Debug output is unconditionally enabled by `record.debug = True` at
module level in `record.py` and cannot be suppressed via the
`RECORD_DEBUG` environment variable.

When `RECORD_DBTYPE` is `gremlin` the script writes the advisory message
to standard error but exits with status 0 rather than a non-zero status,
making it indistinguishable from a successful truncation in automated
pipelines.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `record-documentation.py`,
`delete-database.py`, `create-database.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a safe,
confirmation-gated command-line interface for clearing all provenance
data from the relational backends (SQLite and PostgreSQL) used by the
RECORD workflow system.
