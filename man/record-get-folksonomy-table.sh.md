## SYNOPSIS

`record-get-folksonomy-table.sh`

## DESCRIPTION

`record-get-folksonomy-table.sh` extracts the list of tag variable names
from the folksonomy library at `example/lib.folksonomy.sh`. It finds all
lines invoking `record_make_tag`, strips everything from the `=` sign
onwards, and prints the resulting variable names to standard output —
one per line.

The path to `example/lib.folksonomy.sh` is hard-coded; the script must
be run from the root of the RECORD project directory.

## OPTIONS

This script accepts no options or arguments.

## EXIT STATUS

Returns 0 on success, or if no matches are found.

Returns non-zero if `example/lib.folksonomy.sh` does not exist or
cannot be read.

## EXAMPLES

List all folksonomy tag variable names:

    record-get-folksonomy-table.sh

Use the output to drive further processing:

    record-get-folksonomy-table.sh | while read tag; do
        echo "Processing $tag"
    done

## FILES

`example/lib.folksonomy.sh`
: The folksonomy library file. Path is hard-coded relative to the
  working directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The path `example/lib.folksonomy.sh` is hard-coded, so the script will
silently produce no output or fail with a `grep` error if run from any
directory other than the RECORD project root.

The script accepts no `--help` or `--version` flags, unlike other RECORD
utilities.

If `grep` finds no matches it exits with status 1, which will propagate
as a non-zero exit from the script and may be misinterpreted as an error
by calling scripts using `set -e`.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.sh`, `record-update.py`, `example/lib.folksonomy.sh`

## HISTORY

Created as part of the RECORD workflow tools to extract the set of
folksonomy tag identifiers defined in the example folksonomy library.
