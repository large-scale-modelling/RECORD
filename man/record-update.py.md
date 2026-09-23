## SYNOPSIS

`record-update.py --table=`*TableName* `--`*column_name*`=`*value* [...]

## DESCRIPTION

`record-update.py` inserts or updates a single record in the RECORD provenance
database from the command line. It is the primary write helper used by
`record.sh` to record provenance entities such as applications, processes,
boxes, persons, and pipelines.

The script takes a mandatory `--table` argument identifying the entity
class to operate on, followed by one or more `--column=value` arguments
supplying field values. Column names are matched case-insensitively against
the attributes of the named entity class.

`record-update.py` first attempts to insert the record by calling `add`. If the
record already exists (detected via a backend-appropriate uniqueness
exception — `GremlinVertexExists`, `sqlite3.IntegrityError`, or
`psycopg2.errors.UniqueViolation`) it falls back to calling `update` on
the same object instead. Any other exception is reported to standard error
and the script exits with a non-zero status.

On success the primary key value of the inserted or updated record is
printed to standard output. If the primary key is composite, the component
values are printed as a comma-separated list. This output is captured by
`record.sh` to chain identifiers between successive `record-update.py` calls.

## OPTIONS

`--table=`*TableName*
: Required. The entity class to insert or update. *TableName* is
  case-sensitive and must match a class defined in `record.py` exactly
  (for example `Application`, `Box`, `Process`, `Person`, `Pipeline`).

`--`*column_name*`=`*value*
: Sets the field *column_name* to *value*. Column names are matched
  case-insensitively. At least one column argument must be supplied. Any
  argument that does not match a column defined on the entity class raises
  an `IllegalArgumentError` and the script exits without writing to the
  database.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `--table` argument is missing or names an unknown class;
- no valid column arguments are supplied;
- a column name does not exist on the named entity class;
- a database error other than a uniqueness violation occurs during `add`;
  or
- the fallback `update` call raises an exception.

## ENVIRONMENT

The script inherits all database connection environment variables from the
`record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or `gremlin`.
  The appropriate uniqueness exception type is selected at import time
  based on this variable.

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

Prints the primary key value of the affected record to standard output on
success. For composite primary keys the component values are printed as a
comma-separated list, with quoting and the SQL `AND` clauses stripped.

## EXAMPLES

Register a computer node:

    record-update.py \
        --table=Computer \
        --id_computer=computer_myhost \
        --name=myhost \
        --ip_address=192.168.1.1

Register or update an application, capturing its ID:

    id_app=$(record-update.py \
        --table=Application \
        --id_application=application_12345 \
        --name=my_sim \
        --language=Python)

Register a process start, then update it with an end time:

    id_process=$(record-update.py \
        --table=Process \
        --id_process=process_abc \
        --executable="$id_app" \
        --start_time=20240101T120000)

    record-update.py \
        --table=Process \
        --id_process=process_abc \
        --executable="$id_app" \
        --end_time=20240101T130000

## FILES

`lib/record.py`
: The RECORD provenance library. Must be importable as `record`; the
  script appends no path prefix, so `record.py` must be on `sys.path` or
  in the same directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `table_parameter` regex will raise an `AttributeError` rather than
skipping gracefully if any argument in `sys.argv` does not match the
`--table=` pattern, because `re.match` returns `None` for non-matching
strings and `None.groups()` is called unconditionally. The same issue
affects `column_parameter.match(arg)` in the column-parsing loop.

Debug output is unconditionally enabled by the line `record.debug = True`
at module level and cannot be suppressed via the `RECORD_DEBUG` environment
variable.

The variable declared as `colums` (a typo for `columns`) on line 89 is
unused; the actual `columns` dictionary is assigned by `parameters` on the
next line.

The primary key output is derived by applying three successive regex
substitutions to the SQL `WHERE` clause fragment returned by
`getPrimaryKeys`. This approach is fragile: primary key values that contain
the literal string ` AND ` or a leading `= ` may be mangled in the output.

The bare `except: raise` in the `update` fallback swallows the original
exception context, making it harder to diagnose failures that occur during
the update path.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `exists.py`, `get-value.py`, `search.py`,
`create-database.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a single
command-line interface for upsert operations against the provenance
database, supporting all three backends (SQLite, PostgreSQL, and Gremlin)
used by the RECORD workflow system.
