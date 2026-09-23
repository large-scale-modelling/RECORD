## SYNOPSIS

`record-search.py` `--table=`*TableName* [`--`*column_name*`=`*value*...] `--`*column_name*

## DESCRIPTION

`record-search.py` queries the RECORD provenance database for rows
matching a set of column constraints and prints the values of a
specified target column to standard output. It is the search counterpart
to `record-update.py` and `record-get-value.py`.

The script takes a mandatory `--table` argument identifying the entity
class to query, followed by one or more `--column=value` filter
arguments, and a final bare `--column` argument (without a value)
identifying the column whose values should be returned.

Column names are matched case-insensitively against the schema of the
named entity class. For relational backends (SQLite and PostgreSQL),
column existence is verified against the live database schema. For the
Gremlin backend, column existence is verified against the entity
class's instance attributes.

Results are printed one value per line. If no matching rows are found,
an empty line is printed. For the Gremlin backend, the full entry
representation is printed; for relational backends, the value of each
matching column is printed.

## OPTIONS

`--table=`*TableName*
: Required. The entity class to query. *TableName* is case-sensitive
  and must match a class defined in `record.py` exactly (for example
  `Application`, `Box`, `Process`, `Person`, `Pipeline`).

`--`*column_name*`=`*value*
: Constrains the search to rows where *column_name* equals *value*.
  Column names are matched case-insensitively. At least one column
  argument must be supplied.

`--`*column_name*
: The column whose values are to be returned. Specified as a bare flag
  without a value. Must match a column defined on the named entity
  class.

## EXIT STATUS

Returns 0 on success, including when no rows match (an empty line is
printed).

Returns non-zero if:

- the `--table` argument is missing or names an unknown class;
- no valid column arguments are supplied;
- a column name does not exist on the named entity class; or
- a database error occurs during connection or query.

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

Prints matching values to standard output, one per line. Prints an
empty line if no rows match. For Gremlin backends, prints the full
entry representation.

## EXAMPLES

Search for all process IDs associated with a given application:

    record-search.py \
        --table=Process \
        --executable=application_12345 \
        --id_process

Search for all applications written in Python:

    record-search.py \
        --table=Application \
        --language=Python \
        --name

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
module level and cannot be suppressed via the `RECORD_DEBUG` environment
variable.

`basename` is used in debug output but is never imported from `os.path`.
All debug `sys.stderr.write` calls that reference `basename(sys.argv[0])`
will raise a `NameError` at runtime whenever debug mode is active.

The `table_parameter` regex is applied with `.match(arg)` without first
checking whether the result is `None`; any argument that does not match
the `--table=` pattern will cause an `AttributeError` on `.groups()`.
The same issue exists in the column-parsing loop for
`column_parameter.match(arg)`.

The bare `except: raise` in the column validation block swallows the
original exception context, making it harder to diagnose unexpected
database errors.

The `except: raise` in the `search` call similarly loses the original
traceback context.

The `parameters` function verifies column existence by executing a
schema query once per column argument rather than once per table, making
it potentially slow for tables with many columns and many filter
arguments.

The PostgreSQL column existence check uses `information_schema.columns`
without filtering by schema name, which may return false positives if
multiple schemas contain tables with the same name.

The `target` variable is assigned inside the Gremlin branch when
`col_argument is None`, but is never used anywhere in the function,
suggesting incomplete implementation of the target-column selection
logic for the Gremlin backend.

The `__license__` string contains a stray capital `G` in the word
`that` (`"in the hope thaGt it will be useful"`).

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `record-get-value.py`,
`exists.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a command-line
interface for querying the provenance database by column constraints,
supporting all three backends (SQLite, PostgreSQL, and Gremlin).
