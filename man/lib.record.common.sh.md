## SYNOPSIS

`. lib.record.common.sh`

## DESCRIPTION

`lib.record.common.sh` is a shell library sourced by RECORD workflow
scripts. It must not be executed directly. When sourced it defines two
utility functions (`check_for_errors` and `pidtree`  and `get_stderr`)
and performs startup validation of the environment required by the RECORD
workflow system.

**Startup validation** runs unconditionally at source time and performs
the following checks in order:

1. `RECORD_START_PROGRAM` is set. If not, a timestamped error is written
   to standard error and the sourcing shell exits with status -1.
2. `RECORD_START_PROGRAM` names an executable on `PATH`. If not, a
   timestamped error is written to standard error and the sourcing shell
   exits with status -1.
3. If the PID file (`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`)
   exists, its first line is read and validated as a non-empty integer.
   If the PID file is present but malformed, a timestamped error is
   written to standard error and the sourcing shell exits with status -1.

The PID file path is also exported as `RECORD_PID_FILE` for use by the
sourcing script.

## FUNCTIONS

**`check_for_errors`** *file*

Scans *file* for common error indicators and prints matching lines to
standard output with colour highlighting, line numbers, and the
filename. The following patterns are checked (all patterns are always
run, unlike `record-look-for-errors.sh`):

- Lines containing `: line`
- Lines containing `line ` that do not match `pipeline` (case-insensitive)
- Lines containing `error` (case-insensitive) that do not contain `--error`
- Lines containing `Trace`
- Lines containing `does not exist`
- Lines containing `No such file or directory`

Returns the exit status of the final `grep`. Takes exactly one argument;
behaviour is undefined if called with zero or more than one argument.

**`pidtree`** [*pid*...]

Prints the full process subtree rooted at each given *pid*, one PID per
line. Works by reading the full process table from `ps` and walking the
parent-child relationships recursively. Compatible with both `bash` and
`zsh` (sets `shwordsplit` when running under `zsh`).

**`get_stderr`** *pid*

Resolves and prints the path to the standard error file descriptor of
the process with the given *pid* by reading
`/proc/<pid>/fd/2` via `readlink -f`. Prints a usage message and exits
with status -1 if no PID is supplied, or if the process is not found or
has no stderr file descriptor.

## ENVIRONMENT

The following variables are read at source time:

`RECORD_START_PROGRAM`
: The name of the top-level program being recorded. Must be set and must
  resolve to an executable on `PATH`. Required; the sourcing shell exits
  if this variable is unset.

`RECORD_DBTYPE`
: Database backend type. Used to construct the PID file path. Should be
  one of `sqlite3`, `postgres`, or `gremlin`.

`USER`
: The current username. Used to construct the PID file path. Normally
  set automatically by the shell.

The following variable is set and exported by this library:

`RECORD_PID_FILE`
: Path to the PID file for this invocation, constructed as
  `/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid`.

## EXIT STATUS

This library causes the sourcing shell to exit with status -1 if any of
the startup validation checks fail. Under most shells `-1` is interpreted
as 255.

Individual functions return the exit status of the last command executed
within them; `get_stderr` explicitly exits with -1 on error.

## EXAMPLES

Source the library at the top of a RECORD workflow script:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    . lib.record.common.sh

Check a log file for errors after a run:

    check_for_errors run.log

Print all child PIDs of a running process:

    pidtree $PPID

Find where a process is writing its stderr:

    get_stderr 12345

## FILES

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file for the current workflow run, exported as `RECORD_PID_FILE`.
  Read (but not written) by this library at source time if it already
  exists.

## AUTHORS

Doug Salt

## CREDITS

The `pidtree` function is adapted from a solution at
https://superuser.com/questions/363169/ps-how-can-i-recursively-get-all-child-process-for-a-given-pid

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The startup validation block runs unconditionally when the file is
sourced. This means `RECORD_START_PROGRAM` and `RECORD_DBTYPE` must be
exported before sourcing even in contexts where the PID-file logic is
not needed.

`exit -1` is used throughout for error exits. POSIX does not guarantee
the behaviour of negative exit codes; most shells interpret `-1` as 255,
but this is not portable.

`check_for_errors` takes a single unquoted filename argument. Filenames
containing spaces or shell metacharacters must be quoted by the caller,
and passing multiple files is not supported (unlike
`record-look-for-errors.sh` which accepts `$@`).

`get_stderr` relies on `/proc/<pid>/fd/2`, which is Linux-specific and
will not work on macOS or other non-Linux systems.

`pidtree` uses a `declare -A` associative array, which requires bash 4.0
or later (or zsh). It will fail silently on bash 3.x (the default on
macOS).

The PID file validation reads the file but takes no action if the PID
is valid — it neither checks whether a process with that PID is actually
running, nor prevents a second instance of the workflow from starting.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.sh`, `record-update.py`, `record-look-for-errors.sh`,
`record-truncate-database.py`, `record-preprocess.jl`

## HISTORY

Created as part of the RECORD workflow tools to provide shared utility
functions and startup validation for shell scripts in the RECORD
provenance system.
