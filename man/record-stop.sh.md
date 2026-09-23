## SYNOPSIS

`record-stop.sh`

## DESCRIPTION

`record-stop.sh` terminates a running RECORD workflow, optionally
including any associated Slurm jobs. It sources `lib.record.common.sh`
and operates in two phases:

**Phase 1 — Slurm cancellation (optional):**

If `RECORD_SLURM` is set, the script queries the Slurm queue with
`squeue` and cancels all jobs whose names match the prefix
`RECORD_SLURM_PREFIX.*` using `scancel`.

**Phase 2 — Process termination:**

- **If `RECORD_START_PROGRAM` is running** (the PID file exists and
  `/proc/<pid>` is present), the script uses `pidtree` to enumerate the
  full process subtree rooted at the recorded PID and sends `SIGKILL`
  (`kill -9`) to every process in the tree. The PID file is then
  removed.

- **If `RECORD_START_PROGRAM` is not running** (the PID file is absent
  or the process no longer exists), a timestamped message is written to
  standard error and the script exits with status -1.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables.

## EXIT STATUS

Returns 0 if the process tree was successfully killed and the PID file
removed.

Returns -1 (typically 255) if:

- the PID file does not exist; or
- the process recorded in the PID file is no longer running.

Returns non-zero if `lib.record.common.sh` validation fails at source
time (see `lib.record.common.sh` documentation).

## ENVIRONMENT

`RECORD_START_PROGRAM`
: The name of the workflow program to stop. Set and validated by
  `lib.record.common.sh` at source time.

`RECORD_DBTYPE`
: Used by `lib.record.common.sh` to construct the PID file path.

`RECORD_PID_FILE`
: Path to the PID file, exported by `lib.record.common.sh` as
  `/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid`.

`RECORD_SLURM`
: When set (to any non-empty value), enables Slurm job cancellation in
  phase 1. If unset or empty, the Slurm phase is skipped.

`RECORD_SLURM_PREFIX`
: The job name prefix used to identify Slurm jobs belonging to this
  workflow. All jobs returned by `squeue` whose names match
  `RECORD_SLURM_PREFIX.*` will be cancelled. Only used when
  `RECORD_SLURM` is set.

## EXAMPLES

Stop a running workflow:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-stop.sh

Stop a workflow and cancel its associated Slurm jobs:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    export RECORD_SLURM=1
    export RECORD_SLURM_PREFIX=my_sim
    record-stop.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file written by the workflow run. Read to identify the process
  tree to kill, then removed on success.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

`kill -9` (`SIGKILL`) is sent to every process in the tree without
first attempting a graceful shutdown with `SIGTERM`. This prevents
the workflow from performing any cleanup (flushing buffers, releasing
locks, writing final provenance records) before termination.

`exit -1` is used for error exits. POSIX does not guarantee the
behaviour of negative exit codes; most shells interpret `-1` as 255,
but this is not portable.

The `LOGIN_PID=` assignment inside the running branch is empty and
unused, suggesting incomplete logic that was never finished.

`pidtree` uses `declare -A` associative arrays, requiring bash 4.0 or
later. It will fail silently on bash 3.x (the default on macOS).

The `/proc/<pid>` check used to determine whether the process is
running is Linux-specific and will not work on macOS or other
non-Linux systems.

`$RECORD_PID_FILE` and `$RECORD_SLURM_PREFIX` are unquoted in several
places; values containing spaces or shell metacharacters may cause
unexpected behaviour.

The Slurm `grep` pattern `$RECORD_SLURM_PREFIX'.*'` concatenates a
shell variable with a literal `.*`, which is a basic regular expression
passed to `grep`. If `RECORD_SLURM_PREFIX` is unset, all jobs in the
queue will be matched and cancelled.

If any `kill -9` call fails (e.g. due to a permissions error or a PID
that has already exited), the error is silently ignored and the loop
continues. The PID file is still removed regardless of whether all
kills succeeded.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record.sh`, `record-edit.sh`,
`record-errors.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide a single
command for halting a running workflow and optionally cancelling
its associated Slurm batch jobs.
