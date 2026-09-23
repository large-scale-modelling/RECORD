## SYNOPSIS

`record-documentation.py`

## DESCRIPTION

`record-documentation.py` prints the schema specification of the RECORD
provenance database to standard output. It is a diagnostic and reference
utility that exposes the data model defined by the `record` library in
human-readable form.

The script takes no arguments. It imports the `record` library, calls
`record.specification()`, and writes the result directly to standard
output. If debug mode is active, entry and exit messages are written to
standard error.

## OPTIONS

This script accepts no options or arguments.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `record` library cannot be imported from `lib/`; or
- `record.specification()` raises an unhandled exception.

## ENVIRONMENT

The script inherits all database connection environment variables from the
`record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or `gremlin`.

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

`RECORD_GREMLIN_HOST`
: WebSocket URL of the Gremlin server.

`RECORD_GREMLIN_TIMEOUT`
: Per-query evaluation timeout in milliseconds.

`RECORD_DEBUG`
: When set, enables verbose diagnostic output to standard error.

## RETURN VALUE

Prints the output of `record.specification()` to standard output. The
format of this output is determined by the `record` library.

## EXAMPLES

Print the database schema specification:

    record-documentation.py

Capture the specification to a file:

    record-documentation.py > schema.txt

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

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `exists.py`,
`get-value.py`, `search.py`, `create-database.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a command-line
interface for inspecting the provenance database schema, supporting all
three backends (SQLite, PostgreSQL, and Gremlin) used by the RECORD
workflow system.
