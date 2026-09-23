## SYNOPSIS

`record-edit.sh`

## DESCRIPTION

`record-edit.sh` opens the current or most recent output of
`RECORD_START_PROGRAM` in `vi` for inspection or editing. It sources
`lib.record.common.sh` and uses the PID file and process state to
determine which file to open:

- **If `RECORD_START_PROGRAM` is running** (the PID file exists and
  `/proc/<pid>` is present), the script resolves the program's current
  standard error file descriptor via `get_stderr` and opens it in `vi`.
  This allows live inspection of a running workflow's stderr output.

- **If `RECORD_START_PROGRAM` is not running** (the PID file is absent
  or the process is no longer alive), the script opens the most recent
  output file matching the glob
  `$RECORD_START_PROGRAM.????-??-??.out` in `vi`. A message is written
  to standard error noting that the program is not running.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables inherited from `lib.record.common.sh`.

## EXIT STATUS

Returns 0 if the program is running and `vi` exits successfully.

Returns -1 (typically 255) if:

- the PID file does not exist; or
- the process is no longer running.

Note that in both failure cases `vi` is still launched before the
script exits, so the exit status reflects the state *after* `vi` closes.

## ENVIRONMENT

`RECORD_START_PROGRAM`
: The name of the workflow program being monitored. Used to locate the
  PID file and to glob for output files. Set and validated by
  `lib.record.common.sh` at source time.

`RECORD_DBTYPE`
: Used by `lib.record.common.sh` to construct the PID file path.

`RECORD_PID_FILE`
: Path to the PID file, exported by `lib.record.common.sh` as
  `/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid`.

## EXAMPLES

Open the stderr of a currently running workflow:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-edit.sh

Open the most recent output file of a completed workflow:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-edit.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file written by the workflow run. Read to determine whether
  `RECORD_START_PROGRAM` is currently running.

`$RECORD_START_PROGRAM.????-??-??.out`
: Glob pattern used to find output files when the program is not
  running. Matched in the current working directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

`exit -1` is used for error exits. POSIX does not guarantee the
behaviour of negative exit codes; most shells interpret `-1` as 255,
but this is not portable.

In both non-running branches, `vi` is launched before `exit -1` is
reached. This means the script always opens an editor regardless of
error state, which may be surprising in automated or non-interactive
contexts.

The glob `$RECORD_START_PROGRAM.????-??-??.out` is unquoted and may
expand to nothing (or cause an error with `nullglob` unset) if no
matching files exist in the current directory. `vi` will then be invoked
with a literal unexpanded glob string as its argument.

If the glob matches more than one file, `vi` will open all of them as a
buffer list, which may or may not be the intended behaviour.

`get_stderr` relies on `/proc/<pid>/fd/2`, which is Linux-specific and
will not work on macOS or other non-Linux systems.

The script checks for the existence of `/proc/<pid>` as a proxy for
whether the process is running, which is Linux-specific. On systems
without `/proc`, the live-process branch will never be taken.

The `pid_of_record_run` variable is populated by `lib.record.common.sh`
only when the PID file already exists at source time. If the PID file
was created after sourcing the library, `pid_of_record_run` will be
empty and the script will fall through to the not-running branch even
if the process is live.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record.sh`, `record-look-for-errors.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide convenient
interactive access to the output of a running or recently completed
workflow program.
