## SYNOPSIS

`record-status.sh`

## DESCRIPTION

`record-status.sh` reports the status of a running RECORD workflow by
printing a full process listing for every process in the workflow's
process tree. It sources `lib.record.common.sh` and uses `pidtree` to
enumerate all child processes of the recorded PID, then runs `ps -f`
on each one.

If `RECORD_START_PROGRAM` is running (the PID file exists and
`/proc/<pid>` is present), one `ps` output line is printed per process
in the tree, in the format produced by `ps --no-headers -f`.

If the program is not running, a timestamped message is written to
standard error, any stale PID file is removed, and the script exits
with status -1.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables inherited from `lib.record.common.sh`.

## EXIT STATUS

Returns 0 if `RECORD_START_PROGRAM` is running and `ps` output is
produced successfully.

Returns -1 (typically 255) if `RECORD_START_PROGRAM` is not running.

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
  Removed if found stale (program not running).

## EXAMPLES

Check the status of a running workflow:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-status.sh

Use in a polling loop:

    while record-status.sh 2>/dev/null; do
        sleep 30
    done
    echo "Workflow finished."

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file identifying the running workflow process. Removed if the
  recorded process is no longer alive.

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

`$RECORD_PID_FILE` is unquoted in the `rm` call; a path containing
spaces or metacharacters may cause unexpected behaviour.

`pidtree` uses `declare -A` associative arrays, requiring bash 4.0 or
later. It will fail silently on bash 3.x (the default on macOS).

`ps --no-headers` is a GNU `ps` option and is not portable to macOS or
BSD systems, which use `ps -o` with a custom format to suppress
headers.

The stale PID file is silently removed when the program is found not
to be running. This is a side effect of a read-only status query and
may interfere with other tools that check for the PID file's existence,
such as `record-start.sh`'s duplicate-run guard.

If a PID in the tree has already exited between the `pidtree` call and
the `ps` call, `ps` will produce no output for that PID without any
error, so the listing may be incomplete for short-lived child processes.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record-start.sh`, `record-stop.sh`,
`record-edit.sh`, `record-errors.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide a process-level
status view of a running workflow, listing all processes in the workflow
tree using their full `ps -f` details.
