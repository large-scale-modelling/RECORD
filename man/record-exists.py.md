## SYNOPSIS

`record-exists.py --table=`*TableName* `--`*column_name*`=`*value* [...]

## DESCRIPTION

`record-exists.py` checks whether a record matching the supplied field values
exists in the RECORD provenance database and prints the result to standard
output. It is used by `record.sh` to guard against duplicate insertions and
to test for the presence of registered entities such as applications and
boxes before acting on them.

The script takes a mandatory `--table` argument identifying the entity
class to query, followed by one or more `--column=value` arguments
supplying the field values that identify the record. These values are used
to populate an instance of the named entity class, whose `exists` method is
then called against the database connection.

On success the string `True` or `False` is printed to standard output. If
the `exists` call raises an exception the script prints `False`, disconnects
from the database, and exits with status 0 rather than propagating the
error.

Column validation follows the same backend-specific logic as `get-value.py`:
for the Gremlin backend column names are checked against the entity class's
in-memory attribute dictionary; for SQLite and PostgreSQL they are verified
by querying the live database schema via `PRAGMA TABLE_INFO` or
`information_schema.columns` respectively.

## OPTIONS

`--table=`*TableName*
: Required. The entity class to query. *TableName* is case-sensitive and
  must match a class defined in `record.py` exactly (for example
  `Application`, `Box`, `Process`, `Person`).

`--`*column_name*`=`*value*
: Supplies a field value used to identify the record to check. Multiple
  such arguments may be given. Column names are matched case-insensitively.
  At least one column argument must be supplied.

## EXIT STATUS

Returns 0 in all cases, including when the record does not exist and when
the `exists` call raises an exception.

Returns non-zero only if argument parsing fails due to a missing `--table`
argument, an unknown table name, an invalid column name, or no column
arguments being supplied.

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
: When set, enables verbose diagnostic output to standard error via
  `record.debug`. Note that the module-level `debug` variable in
  `record-exists.py` itself is unconditionally set to `True` and is used
  independently of `record.debug` within the `parameters` function.

## RETURN VALUE

Prints `True` to standard output if the record exists, `False` otherwise.

## EXAMPLES

Check whether an application is already registered:

    record-exists.py --table=Application --id_application=application_12345

Use the result in a shell conditional:

    if [[ $(record-exists.py --table=Application --id_application="$id_app") == "True" ]]
    then
        id_application="$id_app"
    fi

Check whether a box exists before registering it:

    record-exists.py --table=Box --id_box=box_987654

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

The script defines its own module-level `debug` variable and sets it to
`True` unconditionally. This variable is used within `parameters` for
diagnostic output but is entirely independent of `record.debug`, which is
used in `__main__`. The two flags can therefore be in different states,
leading to inconsistent diagnostic behaviour.

The broad `except: raise IllegalArgumentError(...)` in the relational
column-validation branch masks any underlying database error with the
generic message `"Unexpected error for querying column"`, making diagnosis
of connection or query failures difficult.

The bare `except: print(False)` in `__main__` silently suppresses all
exceptions raised by `row.exists`, including unexpected errors unrelated
to the record's absence, and always exits with status 0. Callers cannot
distinguish a genuine `False` result from a failure.

The `__copyright__` field records 2022 while `__modified__` records
2017-04-20, suggesting one of the two dates is incorrect.

The `os` and `getopt` modules are imported but never used.

The TODO comment for `ArgumentValue`-specific validation is present but
the body is a bare `pass`, so no validation is performed.

## COPYRIGHT

Copyright © 2022 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `update.py`, `get-value.py`, `search.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a command-line
existence check against the provenance database, used by `record.sh` to
determine whether entities such as applications and boxes have already been
registered before attempting to insert or retrieve them.
