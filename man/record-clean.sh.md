## SYNOPSIS

`record-clean.sh`

## DESCRIPTION

`record-clean.sh` restores a RECORD experiment directory to a clean state
after execution.

The command removes generated output files and invokes additional cleanup
logic provided by the RECORD workflow library.

Before performing any cleanup, the script checks whether the RECORD run
process is still active using the `pid_of_record_run` variable. If the
process is still running, the script reports the condition and exits
without making changes.

If no active run process is detected, the script removes all files in the
current directory matching the pattern `*.out`. It then executes the
cleanup procedures defined in `lib.record.clean.sh`.

This command is typically used to reset the experiment directory to the
state it was in immediately after initialisation.

## OPTIONS

This command takes no command-line options.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if a RECORD run process is still active or if cleanup
operations fail.

## ENVIRONMENT

The script depends on variables and functions defined in the following
RECORD workflow libraries:

`lib.record.common.sh`
: provides shared configuration variables including
  `pid_of_record_run` and `RECORD_START_PROGRAM`.

`lib.record.clean.sh`
: provides additional cleanup logic for removing generated
  files and restoring the experiment directory state.

## RETURN VALUE

None.

## EXAMPLES

Clean the experiment directory after a run:

    record-clean.sh

Typical workflow:

    record-start.sh
    record-stop.sh
    record-clean.sh
    (do something)
    record-start.sh

## FILES

`lib.record.common.sh`
: shared shell utilities and environment configuration.

`lib.record.clean.sh`
: additional cleanup procedures for RECORD experiments.

## AUTHORS

Doug Salt, Lorenzo Milazzo, Gary Polhill

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The script assumes that the `pid_of_record_run` variable correctly
identifies the active RECORD process.

Only files matching `*.out` in the current directory are removed
explicitly; additional cleanup depends on `lib.record.clean.sh`.

## SEE ALSO

+ `record-start.sh`(

## COPYRIGHT

Copyright © 2022 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record-run.sh`, `record-start.sh`

## HISTORY

Created as part of the RECORD workflow scripts to provide a consistent
mechanism for resetting experiment directories after execution.
