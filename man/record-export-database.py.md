## SYNOPSIS

`record-export-database.py` `output_file`

## DESCRIPTION

`record-export-database.py` exports the configured RECORD database to the
named output file.

If the configured database type is Gremlin, the command connects to the
graph database, retrieves all vertices and edges, converts map keys to
strings where needed, and writes the result as formatted JSON.

If the configured database type is not Gremlin, the command invokes
`pg_dump` to create a PostgreSQL custom-format backup in the named output
file.

## OPTIONS

`output_file`
: path to the file to create

## EXIT STATUS

Returns 0 on success.

Returns non-zero if the database export fails, if the database connection
cannot be made, or if `pg_dump` exits with an error.

## ENVIRONMENT

The command uses the RECORD database configuration provided by the local
Python `record` module.

## RETURN VALUE

None.

## EXAMPLES

Export a Gremlin database or PostgreSQL backup to the named file:

    record-export-database.py export.json

Create a PostgreSQL custom-format dump:

    record-export-database.py backup.dump

## FILES

`lib/record.py`
: provides database configuration and connection handling

## AUTHORS

Doug Salt, Lorenzo Milazzo, Gary Polhill

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

For PostgreSQL exports the database name is currently fixed by the script.

## COPYRIGHT

Copyright © 2022 The James Hutton Institute.  License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`pg_dump`(1)

## HISTORY

Originally written to export Gremlin graph data as JSON. Later extended to
support PostgreSQL export through `pg_dump` and to accept the output file
name as a command-line parameter.
