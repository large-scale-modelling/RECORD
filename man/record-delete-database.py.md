## SYNOPSIS

`record-delete-database.py --force`

## DESCRIPTION

`record-delete-database.py` deletes all tables from the RECORD provenance
database.

The command connects to the configured RECORD database, removes all
tables, and then closes the database connection.

Because this operation permanently deletes all stored provenance data,
the command requires the `--force` option before performing the deletion.

If `--force` is not supplied the program exits without modifying the
database.

## OPTIONS

`--force`
: perform the database deletion

## FILES

`lib/record.py`
: RECORD database interface library

## EXIT STATUS

0
: success

1
: deletion refused because `--force` was not specified

non-zero
: database connection or deletion failure

## ENVIRONMENT

Database connection parameters are determined by the RECORD configuration
used by the `record` Python module.

## SEE ALSO

`record-export-database(1)`,
`record-clean(1)`,
`record-mr-proper(1)`
