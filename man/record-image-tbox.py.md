## SYNOPSIS

`record-image-tbox.py` `>` *output.owl*

## DESCRIPTION

`record-image-tbox.py` generates an OWL ontology, in OWL Functional-Style
Syntax, describing the structure (TBOX) of the RECORD/SSREPI database
schema itself — tables, columns, primary keys, foreign keys, and the
relationships between tables — rather than the data contained within it.
This is distinct from the other `record-image-*.py` scripts, which
visualise the *data* graph; this script documents the *schema*.

The script writes the generated ontology directly to standard output, in
three phases:

1. A fixed ontology header declaring core classes (`Column`,
   `ForeignKey`, `PrimaryKey`, `Table`, `Key`) and object properties
   (`hasForeignKey`, `hasPart`, `hasPrimaryKey`, `manyToMany`, `partOf`,
   `relation`), along with their domains, ranges, and labels.

2. For each relationship returned by `ssrepi.derive_edges()`, declarations
   of the source and target table classes, their primary or foreign key
   classes, and an object property linking them — classified as either
   `manyToMany` (if the edge has a `join`) or `relation` otherwise.

3. For each table and column set returned by `ssrepi.labels()`,
   declarations of the table class and each of its column classes,
   asserting that each column is part of its table.

The output is closed with a final `)"` to complete the `Ontology(...)`
declaration opened in the header.

## OPTIONS

This script accepts no options or arguments.

## EXIT STATUS

Returns 0 on success.

Returns non-zero (with a `SyntaxError`) under Python 3, since the script
is written using Python 2 print-statement syntax (see BUGS).

## ENVIRONMENT

The script inherits all database connection environment variables from
the `ssrepi` library. Refer to `ssrepi.py` for the full list. No database
connection is opened directly in this script; schema information is
obtained via `ssrepi.derive_edges()` and `ssrepi.labels()`.

## RETURN VALUE

Writes a complete OWL ontology in Functional-Style Syntax to standard
output. Redirect to a file to capture it:

    record-image-tbox.py > schema-tbox.owl

## EXAMPLES

Generate the schema TBOX and save it to a file:

    record-image-tbox.py > schema-tbox.owl

Generate the TBOX and validate it with an OWL tool (e.g. ROBOT):

    record-image-tbox.py > schema-tbox.owl
    robot validate --input schema-tbox.owl

## FILES

`lib/ssrepi.py`
: The SSREPI provenance library. Must be importable as `ssrepi`; the
  script appends `lib` to `sys.path` before importing, so `ssrepi.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

**This script is written in Python 2 and will not run under Python 3.**
Every `print` statement uses the bare Python 2 form (`print "..."`)
rather than the Python 3 function call form (`print("...")`). This will
raise a `SyntaxError` immediately on any Python 3 interpreter, which is
what the shebang (`#!/usr/bin/env python3`) requests. The shebang and
the script body are therefore mutually inconsistent.

This script imports `ssrepi` rather than `record`, consistent with the
other "image" scripts but inconsistent with `record-image-project.py`.

The module-level imports include `graphviz`, `os`, `re`, `random`, and
`string`, none of which are used anywhere in the script body.

The variable `sourceForeignKey` is computed twice: once unconditionally
near the top of the loop body, and again inside the `else` branch when
`"join" not in edgeValue.keys()`. The first computation is dead code.

Variable names `sourceClass`, `targetClass`, `sourceKey`, `targetKey`,
`targetPrimaryKey`, and `sourceForeignKey` are all assigned the *string*
result of `getattr(...)()` or string concatenation, but are named as if
they held class objects. This is a naming inconsistency that makes the
logic difficult to follow (the author's own inline comment — "you need
to tidy this up, because it is virtually impossible to read" — confirms
this).

The indentation inside the multi-line string literals for `sourcePrimaryKey`
and `sourceForeignKey` blocks contains inconsistent leading whitespace
(some `SubClassOf` lines are indented with extra spaces relative to
their siblings), which does not affect the generated OWL syntax but
suggests the string templates were edited carelessly.

The script assumes `ssrepi.derive_edges()` and `ssrepi.labels()` succeed
and return well-formed dictionaries; there is no error handling if the
schema cannot be introspected or if `source`/`target` strings do not
contain the expected `ClassName(key)` format, in which case
`.index("(")` will raise a `ValueError`.

No `ssrepi.connect_db()` / `disconnect_db()` calls are present, unlike
the other `record-image-*.py` scripts, suggesting `derive_edges()` and
`labels()` operate on static schema metadata rather than a live
connection — this should be confirmed and documented in `ssrepi.py`.

## COPYRIGHT

Copyright © 2017 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`ssrepi.py`, `record.py`, `record-image-project.py`,
`record-image-services.py`, `record-image-workflow.py`,
`record-image-provenance.py`

## HISTORY

Created as part of the RECORD/SSREPI workflow tools to generate a formal
OWL ontology describing the structure of the underlying database schema,
complementing the data-level Graphviz visualisations produced by the
other `record-image-*.py` scripts.
