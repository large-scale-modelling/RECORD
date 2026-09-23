## SYNOPSIS

`record-mr-proper.sh`

## DESCRIPTION

`record-mr-proper.sh` performs a full reset of the RECORD workflow
environment. It is the RECORD equivalent of `make mrproper` in the
Linux kernel build system: a destructive, non-recoverable operation that
returns the environment to a clean state.

The script prompts the user to type `YES` (uppercase) to confirm intent
before proceeding. Any other input causes the script to exit without
taking any action.

On confirmation the script runs the following steps in order:

1. **`record-stop.sh`** — terminates any running instance of
   `RECORD_START_PROGRAM` and removes the PID file.
2. **`record-clean.sh`** — removes initialisation and output files.
3. **`reccord-delete-database.py`** — deletes the provenance database.
4. **`. lib.record.mrproper.sh`** — sources any additional project-specific
   cleanup defined in `lib.record.mrproper.sh`.

## OPTIONS

This script accepts no options or arguments.

## EXIT STATUS

Returns 0 on successful completion of all steps.

Returns -1 (typically 255) if the user does not confirm with `YES`.

Returns non-zero if `lib.record.common.sh` validation fails at source
time, or if any of the invoked scripts exit with a non-zero status.

## ENVIRONMENT

All environment variables required by `lib.record.common.sh`,
`record-stop.sh`, and `reccord-delete-database.py` are inherited from
the calling environment. Refer to those scripts for the full list.

## EXAMPLES

Perform a full reset of the RECORD environment:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-mr-proper.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`lib.record.mrproper.sh`
: Project-specific cleanup library sourced as the final step. Must be
  present in the working directory if any project-specific teardown is
  required.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

`reccord-delete-database.py` is a typo (double `c`) and will fail with
a command-not-found error, silently skipping the database deletion
unless `set -e` is active. The correct name is likely
`record-delete-database.py`.

The script does not use `set -e`, so if `record-stop.sh` or
`record-clean.sh` fails, execution continues to the database deletion
and mrproper steps regardless.

`exit -1` is used for the confirmation refusal exit. POSIX does not
guarantee the behaviour of negative exit codes; most shells interpret
`-1` as 255, but this is not portable.

The warning message is printed with `echo` rather than directed to
standard error, so it will be swallowed if stdout is redirected.

`lib.record.mrproper.sh` is sourced unconditionally as the final step
but there is no check that it exists; if the file is absent, the source
command will fail with an error, making the success of an otherwise
complete reset appear as a failure.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `lib.record.mrproper.sh`, `record-stop.sh`,
`record-clean.sh`, `record-delete-database.py`, `record-start.sh`

## HISTORY

Created as part of the RECORD workflow tools as a full environment
reset command, inspired by the `make mrproper` target in the Linux
kernel build system which removes all generated files and returns the
source tree to a pristine state.
