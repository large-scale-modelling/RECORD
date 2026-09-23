## SYNOPSIS

`record-preprocess.jl` [*options*] `--` *command* [*arg*...]

## DESCRIPTION

`record-preprocess.jl` parses a command invocation and generates the
provenance boilerplate needed to record it in the RECORD workflow system.
It is intended to wrap an existing command call: everything before `--` is
interpreted as options to the preprocessor itself; everything after `--`
is the target command and its arguments.

The script produces two kinds of output:

1. **Standard output** — a shell fragment assigning `$ARGS` with
   `--record-argument-*` and `--record-stdout-*` / `--record-stderr-*`
   lines, one per argument or redirection, for direct inclusion in the
   provenance-recording call.

2. **Argument-types library file** (`lib.<PROG>.argument-types.sh` by
   default) — a shell script that registers each argument type with
   `record_argument_type`, with placeholder descriptions and ranges
   derived from the observed values.

3. **Output-types library file** (`lib.<PROG>.output-types.sh` by
   default) — a shell script that registers each redirected output with
   `record_output_box_type`.

The first token after `--` must be a resolvable executable (`Sys.which`
is used to verify this); it becomes `$PROG` and is used to namespace all
generated identifiers.

Argument parsing of the passthrough section handles the three major
command-line conventions automatically:

- **\*NIX long options** (`--flag`, `--option=value`, `--option value`)
- **\*NIX short options** (`-f`, `-o value`, `-o=value`; with `-U`,
  single-hyphen strings are split into individual letter flags)
- **Windows/MSDOS switches** (`/S`, `/S:value`)

Shell redirections (`>`, `>>`, `2>`, `2>>`, `2>&1`) are recognised
in-line and recorded as output types rather than arguments.

Ambiguities (e.g. whether a bare token following a flag is its value or
an independent positional argument) are resolved heuristically by
read-ahead: if the next token starts with `-`, `/`, or `>` it is treated
as a new argument and the current token is classified as a flag. Use
`--suppress-alternatives` to silence the reporting of such ambiguities.

If `--run` is supplied the target command is also executed under
`strace`, and the files it reads and writes are reported to standard
output.

## OPTIONS

Options must appear **before** `--`. Any positional argument before `--`
is an error.

`-a` *val*, `-a=`*val*, `--assignment-operator` *val*, `--assignment-operator=`*val*
: Override the character used as the assignment operator when splitting
  option names from values in the passthrough section. By default the
  operator is inferred from context (`=` for long options, `:` for
  Windows switches, space otherwise).

`-D`, `--debug`
: Enable debug logging to standard error via Julia's `Logging` module.

`-H`, `--help`
: Print a usage summary including annotated output examples, then exit 0.

`-l` *val*, `-l=`*val*, `--argument-types-library` *val*, `--argument-types-library=`*val*
: Write the argument-types shell fragment to *val* instead of the default
  path `lib.<PROG>.argument-types.sh`.

`-o` *val*, `-o=`*val*, `--output-types-library` *val*, `--output-types-library=`*val*
: Write the output-types shell fragment to *val* instead of the default
  path `lib.<PROG>.output-types.sh`.

`-R`, `--run`
: Execute the passthrough command under `strace` after generating the
  provenance fragments, and print the sets of files read and written.

`-S`, `--suppress-alternatives`
: Do not report ambiguous argument assignments; silently accept the
  default interpretation.

`-U`, `--unix-flags`
: Treat single-hyphen options as compact flag strings (e.g. `-ABC` is
  three flags `-A`, `-B`, `-C`). Also sets `=` as the assignment
  operator for long options.

`-V`, `--version`
: Print the version string and exit 0.

## EXIT STATUS

Returns 0 on success.

Returns 2 (via `die`) if:

- a required value is missing for a recognised option;
- an unrecognised option appears before `--`;
- a positional argument appears before `--`;
- the first passthrough token is not a resolvable executable; or
- any other fatal error is detected during argument processing.

## ENVIRONMENT

`record-preprocess.jl` does not read any environment variables directly.
If `--run` is used, the child process inherits the full environment.

## RETURN VALUE

On success the script writes to three destinations:

- **stdout**: the `$ARGS` shell fragment.
- **`lib.<PROG>.argument-types.sh`** (or the path given by `-l`): the
  argument-type registration script, opened in append mode.
- **`lib.<PROG>.output-types.sh`** (or the path given by `-o`): the
  output-type registration script, opened in append mode.

## EXAMPLES

Generate provenance fragments for a Python script invocation:

    record-preprocess.jl -- prog.py \
        --out-file=dougs.file \
        -on-flag \
        -A \
        -i input_path.dat \
        "pickling times are fun times" \
        2>&1 \
        > dougs.out

Generate fragments using Unix flag mode and a custom argument-types path:

    record-preprocess.jl \
        -U \
        -l lib.my_tool.args.sh \
        -- my_tool -Dvf input.dat > output.dat

Generate fragments and also run the command, tracing file I/O:

    record-preprocess.jl -R -- my_tool --config=conf.yaml input.dat

## FILES

`lib.<PROG>.argument-types.sh`
: Shell script registering each argument type via `record_argument_type`.
  Created or appended to in the current working directory unless
  overridden with `-l`.

`lib.<PROG>.output-types.sh`
: Shell script registering each output type via `record_output_box_type`.
  Created or appended to in the current working directory unless
  overridden with `-o`.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `parse_before_double_dash` function calls `split(a, "=", limit=2)`
unconditionally when `--assignment-operator` or `--argument-types-library`
is detected, but then tests the variable `val` (undefined) rather than
`value`, meaning the `=`-form of these options will always raise an
`UndefVarError` at runtime.

Similarly, in the `-a=` and `-l=` short-option handlers, the parsed
value is assigned to `val` (undefined) rather than `assignment_operator`
or `arguments_path`.

The `--unix-flags` handler sets `assignment_operator = "="` at module
level but `parse_before_double_dash` also returns a local
`unix_flags`/`assignment_operator`; the interaction between the global
and local variables may produce unexpected behaviour.

In the main passthrough loop, the variable `assingment` (a typo for
`assignment`) is written in several branches but the correctly-spelled
`assignment` is what is passed to `preprocessor`, so the space-separated
assignment operator is silently discarded.

The `>` redirection handler contains a bare `name =` with no right-hand
side (line 800), which is a syntax error that will prevent the script
from loading.

The `trace_file_io` function contains two debugging `println` calls
(`"pickle"` and `"pockle"`) that are unconditionally written to standard
output and will corrupt the `$ARGS` fragment when `--run` is used.

The output-types library file is opened in append mode; re-running the
script for the same `$PROG` will duplicate entries rather than replacing
them.

Multi-arity argument handling is not yet implemented; the relevant
`--arity` and `--separator` lines in `preprocessor` are commented out
with a `TODO` note.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `record-get-io.jl`,
`exists.py`, `get-value.py`, `search.py`, `create-database.py`

## HISTORY

Created as part of the RECORD workflow tools to automate generation of
provenance-recording boilerplate for arbitrary command invocations,
supporting \*NIX, Windows, and PowerShell argument conventions.
