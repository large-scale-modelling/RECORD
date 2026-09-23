## SYNOPSIS

`record-start.sh`

## DESCRIPTION

`record-start.sh` launches `RECORD_START_PROGRAM` as a detached
background process and records its PID for use by other RECORD workflow
tools. It sources `lib.record.common.sh`, which validates the environment
and checks the PID file before any action is taken.

If `RECORD_START_PROGRAM` is already running (determined by the presence
of a valid PID in the PID file and a live `/proc/<pid>` entry), the
script writes a timestamped error to standard error and exits with
status -1 without starting a second instance.

Otherwise the script launches `RECORD_START_PROGRAM` under `nohup`,
redirecting both stdout and stderr to a datestamped output file named
`$RECORD_START_PROGRAM.<YYYY-MM-DD>.out` in the current working
directory. The PID of the background process is written to
`RECORD_PID_FILE`, and a confirmation message is written to standard
error.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables.

## EXIT STATUS

Returns 0 if `RECORD_START_PROGRAM` is launched successfully.

Returns -1 (typically 255) if `RECORD_START_PROGRAM` is already
running.

Returns non-zero if `lib.record.common.sh` validation fails at source
time (see `lib.record.common.sh` documentation).

## ENVIRONMENT

`RECORD_START_PROGRAM`
: The program to launch. Must be set and resolve to an executable on
  `PATH`. Validated by `lib.record.common.sh` at source time.

`RECORD_DBTYPE`
: Used by `lib.record.common.sh` to construct the PID file path.

`RECORD_PID_FILE`
: Path to the PID file, exported by `lib.record.common.sh` as
  `/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid`.
  Written with the PID of the launched process on success.

## EXAMPLES

Start a workflow program:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-start.sh

Start and then monitor for errors:

    record-start.sh
    sleep 60
    record-errors.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file written with the PID of the launched process. Used by
  `record-stop.sh`, `record-edit.sh`, and `record-errors.sh` to locate
  the running process.

`$RECORD_START_PROGRAM.<YYYY-MM-DD>.out`
: Datestamped output file written in the current working directory,
  capturing both stdout and stderr of the launched process.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

`exit -1` is used for error exits. POSIX does not guarantee the
behaviour of negative exit codes; most shells interpret `-1` as 255,
but this is not portable.

The `/proc/<pid>` check is Linux-specific and will not work on macOS
or other non-Linux systems.

`$RECORD_START_PROGRAM` and `$RECORD_PID_FILE` are unquoted throughout;
values containing spaces or shell metacharacters may cause unexpected
behaviour.

If two instances of `record-start.sh` are invoked simultaneously and
the PID file does not yet exist, both may pass the running check and
launch duplicate instances of `RECORD_START_PROGRAM`, with the second
`echo $! > $RECORD_PID_FILE` silently overwriting the first.

If `RECORD_START_PROGRAM` is run multiple times on the same date, each
run appends to the same datestamped `.out` file rather than creating a
new one, as `>` is used but stdout and stderr from successive runs will
be interleaved without any separator.

The PID file is written after `nohup` returns the background PID, but
there is no check that `RECORD_START_PROGRAM` actually started
successfully. If it exits immediately, the PID file will contain a
stale PID and subsequent tools will behave as if the program is still
running until the PID is recycled by the OS.

The confirmation message is written to standard error rather than
standard output, which is consistent with the rest of the RECORD tools
but means it will be suppressed if stderr is redirected.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record-stop.sh`, `record-edit.sh`,
`record-errors.sh`, `record.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide a standardised
launch wrapper for workflow programs, capturing output to a datestamped
file and registering the process PID for use by other tools in the
RECORD suite.
