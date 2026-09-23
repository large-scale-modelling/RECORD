## SYNOPSIS

`record-run.sh` *command* [*arg*...]

## DESCRIPTION

`record-run.sh` is a wrapper that executes a command through the RECORD
workflow environment. It sources `lib/record.sh` and delegates execution
to the `record_run` function defined there, passing all arguments
through unchanged.

This wrapper is typically used to launch commands that should be tracked
as part of a RECORD experiment workflow. It may be invoked directly or
submitted as the executable in a Slurm batch job or other batch system,
ensuring that commands run within the provenance-recording environment
regardless of execution context.

If `DEBUG` is set, entry and exit messages including the full argument
list are written to standard error.

## OPTIONS

This script accepts no options of its own. All positional arguments are
passed directly to `record_run`. Refer to the documentation of
`lib/record.sh` for the arguments and behaviour of `record_run`.

## EXIT STATUS

Returns the exit status of `record_run`. Returns non-zero if
`lib/record.sh` cannot be sourced.

## ENVIRONMENT

`DEBUG`
: When set (to any value), enables entry and exit messages on standard
  error showing the script name and arguments.

All environment variables required by `lib/record.sh` and `record_run`
are inherited from the calling environment. Refer to `lib/record.sh`
for the full list.

## EXAMPLES

Run a command under RECORD provenance tracking:

    record-run.sh my_sim --config=conf.yaml input.dat

Submit as a Slurm batch job:

    sbatch --wrap="record-run.sh my_sim --config=conf.yaml input.dat"

Use from a Slurm job script:

    #!/usr/bin/env bash
    #SBATCH --job-name=my_sim
    record-run.sh my_sim --config=conf.yaml input.dat

## FILES

`lib/record.sh`
: The RECORD workflow library. Sourced at startup using `.` (dot
  source). Must be present at `lib/record.sh` relative to the working
  directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `DEBUG` check `[ -n $DEBUG ]` is unquoted; when `DEBUG` is unset
the expression becomes `[ -n ]`, which evaluates to true in bash
(since the single token `-n` is treated as a non-empty string). As a
result the entry and exit messages are always printed to standard error
regardless of whether `DEBUG` is set. The correct form is
`[ -n "$DEBUG" ]`.

`lib/record.sh` is sourced with a path relative to the working
directory rather than relative to the script's own location. If
`record-run.sh` is invoked from a directory other than the RECORD
project root, sourcing will fail.

The script sources `lib/record.sh` rather than `lib.record.common.sh`
used by the other RECORD wrapper scripts, which is an inconsistency in
the library path convention across the suite.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`lib/record.sh`, `record-start.sh`, `record-stop.sh`,
`record-preprocess.jl`, `record.sh`

## HISTORY

Created as part of the RECORD workflow tools to provide a minimal
executable wrapper around `record_run`, suitable for direct invocation
or submission to Slurm and other batch systems.
