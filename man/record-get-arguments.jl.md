## SYNOPSIS

`record-get-arguments.jl` [*options*] `--` *command* [*args*...]

## DESCRIPTION

`record-get-arguments.jl` is a Julia pre-processor that inspects a command
invocation and generates the RECORD provenance boilerplate needed to record
it in a workflow script. Given a command and its arguments after the `--`
separator, it produces two types of output:

To **standard output**, it emits a shell fragment of `--record-argument-*`,
`--record-stdout-*`, `--record-stderr-*`, and related flags that can be
assigned to a `$ARGS` variable and passed to `record_run` in a RECORD
workflow script.

To two **library files**, it writes the `record_argument_type` and
`record_output_box_type` shell function calls that must be sourced once to
register the argument and output types for the command in the provenance
database. By default these files are named `lib.`*command*`.argument-types.sh`
and `lib.`*command*`.output-types.sh` in the current working directory;
alternative paths can be supplied via `--argument-types-library` and
`--output-types-library`.

The script parses the passthrough command arguments heuristically, handling
Unix long options (`--flag`, `--option=value`, `--option value`), Unix
short options (`-f`, `-o value`), MSDOS-style switches (`/S`, `/S:value`),
and shell redirections (`>`, `>>`, `2>`, `2>>`, `2>&1`). Positional
arguments are detected by read-ahead: if a token does not start with a
recognised prefix and the preceding argument could take a value, the token
is treated as the option's value; otherwise it is classified as a
positional (required) argument.

When ambiguity exists — for example when `-i input.dat` could be either an
option with a value or a flag followed by a positional — the script notes
the ambiguity and, unless `--suppress-alternatives` is set, both
interpretations are presented.

All argument classification takes place before any provenance output is
written. The first token after `--` is treated as the executable name
(*command*) and must be findable on `PATH`; the script aborts if it is not.

## OPTIONS

Options must appear **before** the `--` separator. Everything after `--`
is treated as the command to be analysed.

`--help`, `-H`
: Print a usage summary and exit with status 0.

`--version`, `-V`
: Print the version number and exit with status 0.

`--debug`, `-D`
: Enable debug logging to standard error.

`--assignment-operator` *value*, `--assignment-operator=`*value*, `-a` *value*, `-a=`*value*
: Override the assignment operator used to split option names from their
  values in the passthrough arguments. Useful when the target command uses
  a non-standard separator such as `:`.

`--unix-flags`, `-U`
: Treat single-hyphen options as a run of single-letter flags (Unix style).
  When set, `-ABC` is interpreted as three flags `-A`, `-B`, `-C`, and the
  assignment operator is assumed to be `=`.

`--suppress-alternatives`, `-S`
: Suppress the display of alternative interpretations when argument
  classification is ambiguous. The default interpretation is used silently.

`--argument-types-library` *file*, `--argument-types-library=`*file*, `-l` *file*, `-l=`*file*
: Write the `record_argument_type` stubs to *file* instead of the default
  `lib.`*command*`.argument-types.sh`.

`--output-types-library` *file*, `--output-types-library=`*file*, `-o` *file*, `-o=`*file*
: Write the `record_output_box_type` stubs to *file* instead of the default
  `lib.`*command*`.output-types.sh`.

`--run`, `-R`
: After generating the provenance boilerplate, actually execute the
  passthrough command.

## EXIT STATUS

Returns 0 on success.

Returns 2 (via `die`) if a required option value is missing, if an unknown
option is encountered before `--`, if a positional argument appears before
`--`, or if the *command* after `--` is not found on `PATH`.

## ENVIRONMENT

No environment variables are used directly.

## RETURN VALUE

None. Results are written to standard output and to the two library files.

## EXAMPLES

Generate provenance boilerplate for a simple Python script invocation:

    record-get-arguments.jl -- prog.py \
        --out-file=dougs.file \
        -on-flag \
        -A \
        -i input_path.dat \
        "pickling times are fun times" \
        2>&1 > dougs.out

This produces on standard output:

    $ARGS="""$ARGS
    --record-argument-${a_prog.py_i_id}=input_path.dat
    --record-argument-${a_prog.py_out-file_id}=dougs.file
    --record-argument-${a_prog.py_A_id}
    --record-argument-${a_prog.py_on_flag_id}
    --record-stdout-${o_prog.py_stdout_id}=dougs.out
    """

And writes `record_argument_type` and `record_output_box_type` stubs to
`lib.prog.py.argument-types.sh` and `lib.prog.py.output-types.sh`
respectively.

Use a custom assignment operator for a command that uses `:` as a
separator:

    record-get-arguments.jl --assignment-operator=: -- mycommand /S:value

Treat single-hyphen options as individual flags:

    record-get-arguments.jl --unix-flags -- prog -ABC --option=val

## OUTPUT FILES

`lib.`*command*`.argument-types.sh`
: Shell script fragment containing `record_argument_type` calls for each
  argument detected in the passthrough command. Written to the current
  working directory unless overridden by `--argument-types-library`. Each
  call includes a placeholder description, the inferred type (`option`,
  `flag`, or `required`), the argument name, and where applicable the
  assignment operator, range regex, arity, and order value. Descriptions
  must be filled in manually before use.

`lib.`*command*`.output-types.sh`
: Shell script fragment containing `record_output_box_type` calls for each
  redirection detected in the passthrough command. Written to the current
  working directory unless overridden by `--output-types-library`.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `--assignment-operator` and `--argument-types-library` option parsers
call `split(a, "=", limit=2)` unconditionally before checking whether `=`
is present, then reference the undefined local variable `val` (instead of
`value`) when testing for `nothing`. This will raise an `UndefVarError` at
runtime whenever these options are used.

The same `val` vs `value` bug affects the `-a=`, `-l=`, and `-o=` short
option handlers.

The `--run` / `-R` flag is recognised and sets `execute = true` in
`parse_before_double_dash`, but the return tuple from that function omits
`execute`, so `main` never receives it and the flag has no effect.

The `parse_before_double_dash` return statement when `--` is not found
returns `assignment_operator` and `suppress` in swapped positions compared
to the return statement when `--` is found, meaning the caller will
silently assign the wrong values to these variables when `--` is absent.

In the passthrough parser, the `>` (stdout redirect) branch contains a
syntax error: `name =` appears on a line by itself with no right-hand side,
which will cause a parse error at load time.

In several branches the local variable `assingment` (a typo of
`assignment`) is assigned rather than `assignment`, silently discarding the
space assignment operator for these cases.

The `identifier` variable is referenced in the `required` argument output
inside `preprocessor` but is never assigned a value in `main`, so it will
always be `nothing` in the generated output.

The `--suppress-alternatives` option is spelled `--suppress-alterantives`
(transposed letters) in the help text, which does not match the
`--suppress-alternatives` spelling used in the parser.

The library files are opened in append mode (`"a"`), meaning repeated
invocations accumulate duplicate entries rather than overwriting the
previous output.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.sh`, `record_argument_type`, `record_output_box_type`,
`record-get-io.jl`

## HISTORY

Created as part of the RECORD workflow tools to reduce the manual effort
of writing provenance boilerplate for existing commands, by automatically
inferring argument types and redirection outputs from a representative
command invocation and generating the corresponding `record_argument_type`
and `record_output_box_type` registration stubs.
