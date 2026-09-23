## SYNOPSIS

`trace-recurse.sh` *input.dot* *token* *output* *filter* *history*

## DESCRIPTION

`trace-recurse.sh` is the recursive traversal helper for `trace.sh`. It
scans a Graphviz DOT file for all edges and nodes involving a given *token*,
appends matching lines to an accumulator file, and calls itself recursively
for each newly discovered downstream node.

For each line in *input.dot* that mentions *token*, the script distinguishes
three cases. If the line is an edge (`->`) and *token* is the source, the
target node is extracted and, provided it has not been visited before (as
recorded in *history*) and both the source and target entity types appear
in *filter*, the edge is appended to *output* and the script recurses with
the target as the new token. If the line is a node declaration for *token*
and the token's entity type appears in *filter*, the node line is appended
to *output*. Edge lines in which *token* is the target rather than the
source are silently ignored, confining the traversal to forward (downstream)
edges only.

The script enforces a caller restriction: it inspects its parent process
name and refuses to run unless it was invoked by `trace.sh` or by another
instance of itself. This prevents accidental direct invocation.

This script is not intended to be called directly. Use `trace.sh` instead.

## ARGUMENTS

*input.dot*
: Path to the Graphviz DOT file being traversed. Passed unchanged through
  each level of recursion.

*token*
: The node identifier currently being traced, of the form `EntityType.id`.
  At the top level this is the original search token supplied to `trace.sh`;
  at deeper levels it is a downstream node discovered during traversal.

*output*
: Path to the accumulator file to which matching node and edge lines are
  appended. Shared across all recursive calls.

*filter*
: A space-separated list of entity type names. Only nodes and edges whose
  source and target types both appear in this list are written to *output*.

*history*
: A string recording the node identifiers that have already been visited
  during the current traversal, used to detect cycles and prevent infinite
  recursion. Each visited node identifier is concatenated onto this string
  before the next recursive call.

## OPTIONS

This command takes no option flags. All arguments are positional and
mandatory.

## EXIT STATUS

Returns 0 on success.

Returns -1 if the script is not called from `trace.sh` or
`trace-recurse.sh`.

## ENVIRONMENT

No environment variables are used.

## RETURN VALUE

None. Results are written to the *output* accumulator file.

## EXAMPLES

This script is not intended to be invoked directly. It is called
automatically by `trace.sh`. A representative internal call takes the
form:

    trace-recurse.sh provenance.dot Containers.container_505627104 \
        /tmp/tmp.abc123 "Applications Containers" \
        Containers.container_505627104

## FILES

`trace.sh`
: The parent script that performs argument parsing, option handling, and
  final output assembly. `trace-recurse.sh` must be called from `trace.sh`
  or from itself.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The caller restriction is implemented by checking the parent process name
via `ps $PPID`. This check can fail in environments where `ps` output
formatting differs from the expected column layout, or where the parent
process name is truncated. It will also fail if `trace.sh` or
`trace-recurse.sh` are invoked via a wrapper or a shell that alters the
process name.

The cycle detection mechanism concatenates visited node identifiers into a
single string and uses a glob match (`[[ "$hist" != *$target* ]]`) to
detect revisits. This will produce false positives if one node identifier
is a substring of another, potentially suppressing legitimate traversal
paths.

The edge-line regex used to extract the source node
(`sed 's/^.*"\(.*\)".*\-\>.*".*".*$/\1/'`) and target node
(`sed 's/^.*".*".*\-\>.*"\(.*\)".*\[.*$/\1/'`) relies on a fixed quoting
and bracket structure. DOT lines that deviate from this structure (for
example those lacking a trailing `[label=...]` attribute) will not be
parsed correctly, and the extracted source or target may be empty or
malformed.

Duplicate-edge detection (`egrep -q "$source.*\-\>.*$target" "$output"`)
uses an unanchored regex against the accumulated output file, which may
produce false positives if the source or target strings contain regex
metacharacters or appear as substrings of other identifiers.

The script reads from *input.dot* twice: once via `egrep "$token" "$input"`
piped into the `while read` loop, and again by redirecting the same file
into the loop with `done < "$input"`. The redirect at the end of the loop
overrides the pipe, so the pipe's output is discarded and the loop actually
iterates over the raw *input.dot* rather than the pre-filtered grep output.
This means every line of the file is examined regardless of whether it
mentions *token*, making the grep redundant and the loop less efficient
than intended.

## COPYRIGHT

Copyright © 2023 Doug Salt.  License GPLv3+: GNU GPL version 3 or later
<https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`trace.sh`, `analysis.py`, `dot(1)`

## HISTORY

Created as a companion to `trace.sh` to work around the limitation that
Bash functions cannot be called recursively with a consistent process
space. By externalising the recursion into a separate script, each
recursive step runs in its own process, allowing the traversal to descend
to arbitrary depth without corrupting shared shell state.
