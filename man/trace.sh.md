## SYNOPSIS

`trace.sh` [*options*] *input.dot* *output.dot* *token*

## DESCRIPTION

`trace.sh` filters a Graphviz DOT file produced by the RECORD/SSRepI
provenance tools, tracing a named entity forward through the directed graph
and writing either a filtered subgraph or a coloured version of the full
graph to an output file.

Given a DOT file and a target *token* (a node identifier of the form
`EntityType.id`), `trace.sh` recursively follows all outgoing edges from
that node, collecting the token and all of its descendants. The result can
be written as a new DOT file containing only those nodes and edges, or the
original graph can be re-emitted with the traced nodes and their descendants
highlighted in red.

The set of entity types included in the trace can be narrowed using
`--include` or broadened back from an exclusion list using `--exclude`.
These two options are mutually exclusive.

Recursive traversal is delegated to `trace-recurse.sh`, which must be
present on `PATH`. A temporary file is used to accumulate results from the
recursive calls before final output is produced.

## OPTIONS

`--help`, `-H`
: Print a usage summary and exit with status 0.

`--version`, `-V`
: Print the program name and version number to standard error and exit
  with status 1.

`--colour`, `-C`
: Instead of writing a filtered subgraph, re-emit the full input graph
  with traced nodes and their descendants coloured red (`color = red,
  fontcolor = red`). The output file is built by processing every line of
  the input and adding colour attributes to lines that appear in the
  trace results.

`--affected` *file*, `-a` *file*
: Write the list of affected entity identifiers (one per line, sorted and
  deduplicated) to *file*. Only node lines (not edge lines) from the trace
  results are included. This can be used to enumerate entities downstream
  of a suspect input such as a bad dataset.

`--include` *EntityType*, `-i` *EntityType*
: Restrict the trace to the named entity type. May be repeated to include
  multiple types. The entity type of *token* must always be present in the
  include list. Cannot be used together with `--exclude`.

`--exclude` *EntityType*, `-x` *EntityType*
: Exclude the named entity type from the trace. May be repeated. The
  entity type of *token* cannot be excluded. Cannot be used together with
  `--include`.

## ARGUMENTS

*input.dot*
: Path to the input Graphviz DOT file to be filtered. Must be the first
  positional parameter.

*output.dot*
: Path to the output DOT file to be written. Must be the second positional
  parameter.

*token*
: The node identifier to trace, of the form `EntityType.id` (for example
  `Containers.container_505627104`). Must be the third positional
  parameter.

## EXIT STATUS

Returns 0 on success.

Returns -1 if a required positional argument is missing, if the input file
does not exist, if an `--include` or `--exclude` entity type is not present
in the input graph, if the token's entity type is absent from the include
list, or if the token's entity type appears in the exclude list.

Returns -2 if both `--include` and `--exclude` are specified simultaneously.

Returns 1 if `--version` is requested.

## ENVIRONMENT

No environment variables are used directly. The script depends on
`trace-recurse.sh` being present and executable on `PATH`.

## RETURN VALUE

None.

## EXAMPLES

Trace a container node through the full provenance graph:

    trace.sh provenance.dot trace.dot Containers.container_505627104

Trace the same node, showing only Applications and Containers:

    trace.sh --include Applications --include Containers \
        provenance.dot trace.dot Containers.container_505627104

Colour the affected nodes red in the original graph rather than filtering:

    trace.sh --colour \
        provenance.dot coloured.dot Containers.container_505627104

Write affected entity identifiers to a separate file:

    trace.sh --affected affected.txt \
        provenance.dot trace.dot Containers.container_505627104

Render the output DOT file to a PDF:

    trace.sh provenance.dot trace.dot Containers.container_505627104
    dot -Tpdf trace.dot -o trace.pdf

## FILES

`trace-recurse.sh`
: Helper script that performs the recursive graph traversal. Must be on
  `PATH`. Refuses to run unless called from `trace.sh` or itself.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The check for the input file (`[ -z "$input" ] && [ ! -f $input ]`) uses
`&&` where `||` is intended. As written, the condition can only be true
when `$input` is both empty and does not exist as a file; a non-empty but
invalid path will pass the check and cause subsequent commands to fail with
less informative errors.

The positional parameters are assigned in the order input, output, token
(positions 1, 2, 3), but the usage message describes them in a different
order (input, token, output). This inconsistency is likely to cause
confusion.

The temporary file created by `mktemp` is not removed on exit; the
`rm $temp_output` line at the end of the script is commented out.

The `--colour` mode processes the original input file line by line and
uses `egrep -F -q` to check whether each line appears verbatim in the
temporary trace output. Lines containing special characters may not match
correctly, and the entire input file is re-scanned for every line, making
this mode O(n²) in the number of lines.

The `--version` option exits with status 1 rather than 0, which is
unconventional and will cause callers that check exit codes to treat a
version query as a failure.

Variables `number`, `rest`, and `ws` are set in the default behaviour
comment line but are never used.

## COPYRIGHT

Copyright © 2023 Doug Salt.  License GPLv3+: GNU GPL version 3 or later
<https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`trace-recurse.sh`, `analysis.py`, `dot(1)`

## HISTORY

Created as part of the RECORD/SSRepI workflow tools to allow users to
trace the provenance impact of a particular entity — such as a suspect
dataset — forward through a directed provenance graph, and to visualise
or enumerate the affected downstream entities.
