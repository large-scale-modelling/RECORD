## SYNOPSIS

`record-errors.sh`

## DESCRIPTION

`record-errors.sh` scans workflow output files for error indicators
using the `check_for_errors` function from `lib.record.common.sh`. It
sources `lib.record.common.sh` and operates in two phases:

**Phase 1 — current or recent output:**

- **If `RECORD_START_PROGRAM` is running** (the PID file exists and its
  stderr file descriptor resolves to a regular file), `check_for_errors`
  is run non-interactively against the live stderr file.

- **If `RECORD_START_PROGRAM` is not running**, the script iterates over
  all `*.out` files in the current working directory and prompts the
  user interactively for each one:
  - `Y` — run `check_for_errors` on the file.
  - `N` — skip the file.
  - `Q` — exit the script immediately.

**Phase 2 — Slurm output:**

Unconditionally runs `check_for_errors` on every `*.out` file found
under `slurm-outputs/`, regardless of the outcome of phase 1.

## OPTIONS

This script accepts no options or arguments. All configuration is
supplied via environment variables inherited from `lib.record.common.sh`.

## EXIT STATUS

Returns 0 on normal completion.

Returns 0 if the user enters `Q` during interactive prompting.

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

Scan the current workflow run or recent output files:

    export RECORD_START_PROGRAM=my_sim
    export RECORD_DBTYPE=sqlite3
    record-errors.sh

## FILES

`lib.record.common.sh`
: Common library sourced at startup. Must be present in the working
  directory or on `PATH`.

`/tmp/record.<USER>.<RECORD_DBTYPE>.<RECORD_START_PROGRAM>.pid`
: PID file written by the workflow run. Read to determine whether
  `RECORD_START_PROGRAM` is currently running.

`*.out`
: Output files in the current working directory, inspected
  interactively when the program is not running.

`slurm-outputs/*.out`
: Slurm job output files, always scanned non-interactively in phase 2.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The condition `[ -f $(get_stderr ...) ]` is unquoted; if the path
returned by `get_stderr` contains spaces, the test will fail or behave
unexpectedly.

`get_stderr` relies on `/proc/<pid>/fd/2`, which is Linux-specific and
will not work on macOS or other non-Linux systems.

The glob `*out` in the interactive phase matches any file ending in
`out`, not just files with the `.out` extension — for example,
`stderr_output` would also be matched. The Slurm phase uses `*.out`
(with a dot), so the two phases are inconsistent.

If `slurm-outputs/` does not exist or contains no `*.out` files, the
`for` loop in phase 2 will iterate once with the literal string
`slurm-outputs/*.out` as `$file`, and `check_for_errors` will be called
with that unexpanded glob as its argument, likely producing a `grep`
error.

Phase 2 always runs unconditionally after phase 1 completes normally.
There is no way to suppress the Slurm scan, even in environments where
`slurm-outputs/` is not relevant.

The interactive prompt does not have a newline after it, so on some
terminals the user's input appears on the same line as the prompt.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib.record.common.sh`, `record-look-for-errors.sh`, `record-edit.sh`,
`record.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide interactive and
automated scanning of workflow output files for error indicators,
including support for Slurm batch job outputs.
