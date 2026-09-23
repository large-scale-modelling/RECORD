## SYNOPSIS

`record-get-value.py --table=`*TableName* `--`*column_name*`=`*value* [...] `--`*target_column*

## DESCRIPTION

`record-get-value.py` retrieves a single field value from a record in the RECORD
provenance database. It is used by `record.sh` to look up stored attributes
of entities — such as the location of a registered application or the
separator character for a named argument — so that those values can be used
to construct subsequent commands.

The script takes a mandatory `--table` argument, one or more
`--column=value` arguments that identify the record to retrieve (acting as
lookup keys), and a final bare `--column` argument (without a value) that
names the field whose content is to be returned. The identified record is
fetched from the database via the `query` method of the corresponding
entity class, and the value of the target field is printed to standard
output.

Column validation is performed differently depending on the backend: for
Gremlin the column name is checked against the entity class's in-memory
attribute dictionary; for SQLite and PostgreSQL the column name is verified
by querying the live database schema via `PRAGMA TABLE_INFO` or
`information_schema.columns` respectively.

## OPTIONS

`--table=`*TableName*
: Required. The entity class to query. *TableName* is case-sensitive and
  must match a class defined in `record.py` exactly (for example
  `Application`, `Box`, `Argument`, `Process`).

`--`*column_name*`=`*value*
: Supplies a field value used to identify the record. Multiple such
  arguments may be given; together they must provide enough information to
  populate the primary key so that `query` can locate a unique row. Column
  names are matched case-insensitively.

`--`*target_column*
: Required. A bare flag (no `=value` part) naming the field whose value is
  to be printed. Must appear after all `--column=value` arguments. Only
  one target column may be specified per invocation; if more than one bare
  column flag is supplied, only the last one encountered is used as the
  target.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `--table` argument is missing or names an unknown class;
- no `--column=value` lookup arguments are supplied;
- a column name is not valid for the named entity class;
- the database query fails; or
- an unexpected error occurs during column name validation.

## ENVIRONMENT

The script inherits all database connection environment variables from the
`record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or `gremlin`.
  Controls how column names are validated.

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

Prints the value of the target field to standard output. If the field
value is `None` the string `None` is printed.

## EXAMPLES

Retrieve the `location` field of a registered application:

    id_box=$(record-get-value.py \
        --table=Application \
        --id_application=application_12345 \
        --location)

Retrieve the `location_value` field of a box:

    executable=$(record-get-value.py \
        --table=Box \
        --id_box="$id_box" \
        --location_value)

Retrieve the `separator` for a named argument:

    sep=$(record-get-value.py \
        --table=Argument \
        --application=application_12345 \
        --id_argument=argument_input_file \
        --separator)

## FILES

`lib/record.py`
: The RECORD provenance library. Must be present in a `lib` subdirectory
  relative to the working directory, or otherwise on the Python path.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `table_parameter` regex will raise an `AttributeError` rather than
skipping gracefully if any argument in `sys.argv` does not match the
`--table=` pattern, because `re.match` returns `None` for non-matching
strings and `None.groups()` is called unconditionally.

The error message for a missing `--table` argument reads `"No --class
argument supplied"` rather than `"No --table argument supplied"`, which is
misleading.

The `target` variable is assigned inside the argument-parsing loop but is
referenced unconditionally in the return statement. If no bare column
argument is supplied, `target` will be undefined and the script will raise
a `NameError` rather than a descriptive `IllegalArgumentError`.

The bare `except: raise` in `__main__` discards exception context and
offers no additional diagnostic information beyond what the original
exception already provides.

The broad `except: raise IllegalArgumentError(...)` in the relational
column-validation branch will mask any underlying database error (such as
a connection failure or a malformed query) with the generic message
`"Unexpected error for querying column"`, making diagnosis difficult.

`sqlite3` is imported unconditionally at the top of the script regardless
of the value of `RECORD_DBTYPE`, which will cause an import error on
systems where the `sqlite3` module is unavailable even when the backend is
configured as `postgres` or `gremlin`.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `update.py`, `exists.py`, `search.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a command-line
interface for reading individual field values out of the provenance
database, supporting the argument-resolution and file-tracking operations
performed by `record.sh`.
