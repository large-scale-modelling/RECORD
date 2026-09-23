## SYNOPSIS

`. record.sh`

## DESCRIPTION

`record.sh` is a Bash library that provides the core provenance-recording
functions for the RECORD workflow system. It is sourced by experiment
scripts rather than executed directly.

When sourced, `record.sh` performs one-time initialisation: it reads user
data from `RECORD_USER_FILE`, registers each person and user account in
the provenance database, creates standard box type entries for Bash, Perl,
R, and ELF executable scripts, and validates that the environment meets
minimum requirements (Bash 4 or later, a reachable database, and the
`create-database.py` helper on `PATH`).

The library uses a guard variable `CONFIG_LOADED` to ensure initialisation
runs only once per shell session even if `record.sh` is sourced multiple
times.

Functions whose names begin with an underscore (`_`) are internal and
should not be called directly from experiment scripts. Functions prefixed
with `record_` form the public API.

## PUBLIC FUNCTIONS

`record_application` *executable* [*--option=value* ...]
: Registers an application in the provenance database. Detects the
  language of *executable* (Bash, Perl, R, or ELF binary), records its
  file metadata (size, hash, modification time), and creates or updates
  the corresponding Application and Box entries. Optional `--model=` and
  `--instance=` parameters associate the application with a model or box
  instance. Returns the application identifier on standard output.

`record_run` *executable* [*--record-argument-ID=value* ...] \
[*--record-input-ID=path* ...] [*--record-output-ID=path* ...] \
[*--record-stdout-ID=path*] [*--record-stderr-ID=path*] \
[*--record-extend-stdout-ID=path*] [*--dependency=executable*] \
[*--cwd=directory*]
: Records provenance for, and synchronously executes, *executable*.
  Creates a Process entry in the database, maps `--record-argument-*`
  flags to ArgumentValue entries, maps `--record-input-*` flags to input
  Box entries, executes the application (optionally in *directory* if
  `--cwd` is given), then maps `--record-output-*`, `--record-stdout-*`,
  `--record-stderr-*`, and `--record-extend-stdout-*` flags to output Box
  entries. Updates the Pipeline chain on completion. Exits with a non-zero
  status if the application fails.

`record_batch` *executable* [*--record-argument-ID=value* ...] \
[*--record-input-ID=path* ...] [*--record-output-ID=path* ...] \
[*--wait_for=pipeline_id*]
: Submits *executable* for asynchronous execution. When `RECORD_SLURM` is
  set the job is submitted via `sbatch` using `RECORD_SLURM_PREFIX` as the
  job-name prefix and `--wait_for` is translated to a Slurm
  `--dependency=afterany:` clause. Without Slurm the function calls
  `record_block` to enforce the `RECORD_MAX_PROCESSES` limit before
  forking `record_run` in the background.

`record_block` [*id_application*]
: Blocks the calling script until the number of running instances of
  *id_application* (or the calling script if omitted) falls below
  `RECORD_MAX_PROCESSES`. Polls at `RECORD_SLEEP`-second intervals.

`record_argument_type` *id_application* *id_argument* [*--option=value* ...]
: Registers a named argument type for *id_application* in the database.
  Subsequent calls to `record_run` can reference arguments by the
  *id_argument* token via `--record-argument-ID`.

`record_input_box_type` *id_application* *box_type_name* *file_pattern* *locator*
: Registers a named input file type for *id_application*. *file_pattern*
  is a regular expression matched against file names. *locator* must
  conform to the pattern `^(stdout|stderr|arg=[0-9]+|argid=.+|opt=.+|env=.+|in_file=.+)$`.
  Creates a Uses relationship in the database. Returns the box type
  identifier on standard output.

`record_output_box_type` *id_application* *box_type_name* *file_pattern* *locator*
: Registers a named output file type for *id_application*. Arguments have
  the same semantics as `record_input_box_type`. Creates a Product
  relationship in the database. Returns the box type identifier on standard
  output.

`record_require_minimum` *id_application* *spec_name* *required_version* *actual_version*
: Asserts that *actual_version* is greater than or equal to *required_version*
  for a named specification of the current computer. Version strings may
  use dotted numeric notation (`major.minor.patch`) or magnitude suffixes
  (`K`, `M`, `G`, `T`). Records Computer, Specification, Requirement, and
  Meets entries in the database. Returns 0 if the requirement is satisfied,
  non-zero otherwise.

`record_require_exact` *id_application* *spec_name* *required_literal* *actual_literal*
: Asserts that *actual_literal* equals *required_literal* exactly. Records
  the same database entries as `record_require_minimum`. Returns 0 on
  match, non-zero otherwise.

## OPTIONS

`record.sh` itself takes no command-line options. It is sourced, not
executed.

## EXIT STATUS

Individual functions exit the calling shell with `-1` (non-zero) on
database errors, missing executables, failed requirement checks, or when
`record_run` reports a non-zero exit status from the wrapped application.

The initialisation block exits the calling shell immediately if
`RECORD_USER_FILE` does not exist, if Bash is older than version 4, if
`create-database.py` is not on `PATH`, or (when `RECORD_SLURM` is set) if
`squeue` is not available.

## ENVIRONMENT

`RECORD_USER_FILE`
: Path to a CSV file listing project contributors. Required. Each row
  contains fields `record_user_id`, `name`, `email`, `user`, and
  `homedir`.

`RECORD_DBTYPE`
: Database backend. One of `sqlite3`, `postgres`, or `gremlin` (default:
  `gremlin`).

`RECORD_DBFILE`
: Path to the SQLite database file (default: `ssrepi.db`). Used when
  `RECORD_DBTYPE` is `sqlite3`.

`RECORD_DBUSER`
: PostgreSQL username (default: `ds42723`). Used when `RECORD_DBTYPE` is
  `postgres`.

`RECORD_DBNAME`
: PostgreSQL database name (default: `ssrepi`).

`RECORD_POSTGRES_HOST`
: PostgreSQL host (default: `localhost`).

`RECORD_POSTGRES_PORT`
: PostgreSQL port (default: `5432`).

`RECORD_POSTGRES_PASSWORD`
: PostgreSQL password. Required when `RECORD_DBTYPE` is `postgres`.

`RECORD_GREMLIN_HOST`
: Gremlin server WebSocket URL (default: `ws://127.0.0.1:8182/gremlin`).

`RECORD_GREMLIN_TIMEOUT`
: Gremlin query timeout in milliseconds (default: `1200000`).

`RECORD_MAX_PROCESSES`
: Maximum number of concurrent background processes enforced by
  `record_block` and `record_batch` (default: `4`).

`RECORD_SLEEP`
: Poll interval in seconds used by `record_block` (default: `30`).

`RECORD_SLURM`
: When set, `record_batch` submits jobs to Slurm via `sbatch`.

`RECORD_SLURM_PREFIX`
: Prefix applied to Slurm job names (default: `record`).

`RECORD_DEBUG`
: When set, enables verbose diagnostic output to standard error.

`CONFIG_LOADED`
: Set by `record.sh` after initialisation to prevent re-execution on
  subsequent source calls.

## RETURN VALUE

None. `record.sh` is a library; its functions communicate results through
standard output and exit codes.

## EXAMPLES

Source the library and register the calling script:

    source record.sh
    id_app=$(record_me)

Register an argument type and run an application with provenance:

    id_arg=$(record_argument_type "$id_app" argument_input_file \
        --name=input --separator=-- --assignment_operator=equal)

    record_run my_analysis.sh \
        --record-argument-argument_input_file=data.csv \
        --record-output-result_box_type=output.csv

Submit a job to run in the background (or via Slurm if configured):

    record_batch my_analysis.sh \
        --record-argument-argument_input_file=data.csv \
        --record-stdout-log_box_type=run.log

Assert a minimum version requirement:

    record_require_minimum "$id_app" python3 3.9 $(python3 --version | awk '{print $2}')

## FILES

`lib.folksonomy.sh`
: Tag and folksonomy utilities sourced by `record.sh` at initialisation.

`update.py`
: Python helper used by library functions to insert or update database
  records.

`exists.py`
: Python helper used to check whether a record already exists in the
  database.

`get-value.py`
: Python helper used to retrieve individual field values from the database.

`create-database.py`
: Python helper invoked at initialisation to ensure the database schema
  exists.

`create-edge.py`
: Python helper used by some functions when `RECORD_DBTYPE` is `gremlin`
  to create graph edges directly.

## AUTHORS

Doug Salt, Lorenzo Milazzo, Gary Polhill

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The library uses `eval` to execute wrapped applications, which may cause
unexpected word splitting if arguments contain unusual characters.

Version comparison in `record_require_minimum` is only performed when both
the required and actual values match the dotted-numeric or magnitude-suffix
patterns; non-matching strings cause the function to return non-zero via
the regex fall-through path.

The `RECORD_PIPELINE` file is written to `/tmp` using a name derived from
`$USER`, `$$`, and `$(basename $0)`, which may cause collisions in unusual
execution environments.

## COPYRIGHT

Copyright © 2022 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record-run.sh`, `record-clean.sh`, `record-start.sh`, `record.py`

## HISTORY

Developed as part of the RECORD workflow system to provide provenance
capture for social simulation experiments, based on the SSRepI data model
described in Polhill et al. "Towards metadata standards for social
simulation outputs".
