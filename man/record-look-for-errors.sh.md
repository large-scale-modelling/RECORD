## SYNOPSIS

`record-look-for-errors.sh` *file* [*file*...]

## DESCRIPTION

`record-look-for-errors.sh` scans one or more log files for common error
indicators produced by the RECORD workflow system and prints any matching
lines to standard output with colour highlighting, line numbers, and
filenames.

The script applies five successive `grep` patterns in priority order.
Each pattern is tried in turn; if any match is found the script exits
immediately after that pattern, so only the first matching category of
error is reported per invocation:

1. Lines containing `: line` — typically shell error messages of the
   form `script.sh: line 42: ...`.
2. Lines containing `line ` that do not also contain `Pipeline = ` —
   catches further line-reference messages while suppressing false
   positives from pipeline progress output.
3. Lines containing `error` (case-insensitive) that do not contain
   `--error=` — catches error messages while suppressing lines that
   merely reference an `--error=` option.
4. Lines containing `Trace` — catches stack traces and traceback headers.
5. Lines containing `does not exist` — catches missing-file or
   missing-entity messages.

If none of the five patterns match any file, the script exits without
output and returns the exit status of the final `grep`.

## OPTIONS

This script accepts no options of its own. All arguments are passed
directly to `grep` as file paths via `$@`. Standard `grep` options are
not supported and will be treated as filenames.

## EXIT STATUS

Returns 0 if any pattern matches at least one line in the supplied files
(i.e. an error indicator was found).

Returns 1 if no pattern matches any file (i.e. no error indicators were
found).

The exit status reflects the last `grep` executed; intermediate `grep`
invocations that match cause an immediate exit with status 0.

## EXAMPLES

Scan a single log file:

    record-look-for-errors.sh run.log

Scan all log files in a directory:

    record-look-for-errors.sh logs/*.log

Use in a pipeline to fail a build if errors are detected:

    record-look-for-errors.sh run.log && echo "Errors found" && exit 1

## FILES

No files are created or modified by this script. The files named on the
command line are opened read-only by `grep`.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

Because each `grep` exits the script on a match, only the first
matching error category is reported. If a log file contains both a
`: line` message and a `Trace`, only the `: line` match will be shown.

The `--color` flag is always passed to `grep`, which may produce escape
codes that corrupt output when the script is used in a non-interactive
pipeline or when the terminal does not support colour.

The script accepts no `--help` or `--version` flags, unlike the other
RECORD utilities.

`$@` is unquoted in every `grep` invocation, so filenames containing
spaces or shell metacharacters will be split or expanded incorrectly.

The case-insensitive `error` match (pattern 3) will produce false
positives on lines such as `stderr`, `error_count=0`, or any log line
that happens to contain the substring `error` in a non-error context.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.sh`, `record-update.py`, `record-preprocess.jl`

## HISTORY

Created as part of the RECORD workflow tools to provide a quick
diagnostic scan of workflow log files for common error patterns produced
by the RECORD provenance system.
