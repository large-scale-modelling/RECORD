## SYNOPSIS

`record-totals.py`

## DESCRIPTION

`record-totals.py` prints row or entity counts for the RECORD provenance
database. The output format depends on the configured backend:

**Relational backends (SQLite, PostgreSQL):**

Queries every table in the `public` schema and prints the row count for
each table, followed by a grand total. Table names and counts are printed
to standard output as they are retrieved. Any table that cannot be
counted (e.g. due to a permissions error) produces a warning on standard
error and is skipped.

**Gremlin backend:**

Prints a breakdown of vertex counts grouped and sorted by label, then
the total vertex count, followed by the same for edges. The label
breakdown is printed as a side effect of the count queries.

## OPTIONS

This script accepts no options or arguments. The schema name for
relational backends is hard-coded as `public`.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `record` library cannot be imported from `lib/`; or
- a database connection error occurs.

Individual table count failures are non-fatal and produce warnings on
standard error rather than a non-zero exit.

## ENVIRONMENT

The script inherits all database connection environment variables from
the `record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or
  `gremlin`.

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

For relational backends, prints output of the form:

    Found <n> tables in schema 'public'
    <table_name>: <row_count>
    ...
    Grand total rows across all tables in 'public': <total>

For the Gremlin backend, prints output of the form:

    [{'<label>': <count>, ...}]
    There are [<total>] vertices.
    [{'<label>': <count>, ...}]
    There are [<total>] edges.

## EXAMPLES

Print row counts for a PostgreSQL or SQLite database:

    record-totals.py

Print vertex and edge counts for a Gremlin database:

    RECORD_DBTYPE=gremlin record-totals.py

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

The schema name `public` is hard-coded in the `__main__` block and
cannot be overridden without editing the script. The `get_table_names`
and `count_total_rows` functions accept a `schema` parameter but it is
never exposed to the user.

`get_table_names` uses `pg_catalog` and is therefore PostgreSQL-specific.
When `RECORD_DBTYPE` is `sqlite3`, the relational branch will call this
function and it will fail, as SQLite does not have a `pg_catalog` schema.
The SQLite backend is therefore not supported by this script despite
appearing to be.

The `get_vertices` and `get_edges` functions print the label-grouped
breakdown as a side effect via `print(result)` rather than returning it.
This mixes display logic with data retrieval and makes the functions
difficult to reuse.

The `get_nodes_by_label` function is defined but its only call site is
commented out in `__main__`, so it is currently unused.

The Gremlin vertex and edge count queries use a hard-coded evaluation
timeout of 1,200,000 milliseconds (20 minutes) via `g.with(...)`,
which ignores the `RECORD_GREMLIN_TIMEOUT` environment variable.

The `count_rows_in_table` function uses an f-string to construct a
`WITH` cursor block, but `conn.cursor()` as a context manager requires
the database driver to support it; this will fail with drivers that do
not implement `__exit__` on cursors.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-search.py`, `record-documentation.py`,
`record-image-project.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a quick summary
of database population, reporting per-table row counts for relational
backends and per-label vertex and edge counts for the Gremlin backend.
