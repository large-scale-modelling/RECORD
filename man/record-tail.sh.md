## SYNOPSIS

`record-tail.sh`

## DESCRIPTION

`record-tail.sh` streams the live stderr output of a running RECORD
workflow using `tail -f`. It sources `lib.record.common.sh`, resolves
the stderr file descriptor of the running process via `get_stderr`, and
follows it continuously until interrupted.

If `RECORD_START_PROGRAM` is running (the PID file exists and
`/proc/<pid>` is present), the script calls `get_stderr` with the
recorded PID and passes the resolved path to `tail -f`, allowing live
monitoring of the workflow's output.

If the program is not running — either because the PID file is absent
or the recorded process no longer exists — a timestamped error is
written to standard error and the script exits with status -1.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables inherited from `lib.record.common.sh`.

## EXIT STATUS

Returns 0 when `tail -f` is interrupted (e.g. by Ctrl-C).

Returns -1 (typically 255) if:

- the PID file does not exist; or
- the process recorded in the PID file is no longer running.

Returns non-zero if `lib.record.common.sh` validation fails at source
time (see `lib.record.common.sh` documentation).

## ENVIRONMENT

`RECORD_START_PROGRAM`
: The name of the workflow program being monitored. Set and validated
  by `lib.record.common.sh` at source time.

`RECORD_DBTYPE`
: Used by `lib.record.common.sh` to construct the PID file path.

`RECORD_PID_FILE`
: Path to the PID file, exported by `lib.record.common.sh` as
  `/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid`.

## EXAMPLES

Follow the live output of a running workflow:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-tail.sh

Use with `record-errors.sh` to check for errors after tailing:

    record-tail.sh
    record-errors.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file identifying the running workflow process. Read to obtain
  the PID passed to `get_stderr`.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

`exit -1` is used for error exits. POSIX does not guarantee the
behaviour of negative exit codes; most shells interpret `-1` as 255,
but this is not portable.

The `/proc/<pid>` liveness check is Linux-specific and will not work
on macOS or other non-Linux systems.

`get_stderr` relies on `/proc/<pid>/fd/2`, which is also Linux-specific.

The two error branches (PID file absent and process not running)
produce identical messages and exit codes, making it impossible to
distinguish between a workflow that was never started and one that has
already finished.

The result of `get_stderr` is unquoted in the `tail -f` call; if the
resolved stderr path contains spaces, the command will fail or behave
unexpectedly.

If the workflow process exits while `tail -f` is running, `tail -f`
will continue to block rather than exit, as it is following a file
rather than a pipe. The user must interrupt it manually with Ctrl-C.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record-edit.sh`, `record-errors.sh`,
`record-start.sh`, `record-stop.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide live streaming
of workflow output, analogous to `tail -f` on a log file but resolving
the correct output file automatically from the running process state.
