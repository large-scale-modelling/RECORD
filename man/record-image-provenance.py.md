## SYNOPSIS

`record-image-provenance.py`

## DESCRIPTION

`record-image-provenance.py` queries the RECORD provenance database and
produces a Graphviz DOT file visualising the full provenance graph. It
is the more comprehensive counterpart to `record-image-project.py`,
covering the complete set of entity types that make up an SSREPI
provenance record rather than just the project-level metadata.

The script connects to the database via the `ssrepi` library, calls
`ssrepi.draw_graph` with a fixed set of entity types and their label
fields, and writes the result to `provenance.dot` in the current working
directory.

The graph includes the following entity types, labelled by the specified
field:

| Entity type              | Label field                |
|--------------------------|----------------------------|
| `Persons`                | `ID_PERSON`                |
| `Users`                  | `ID_USER`                  |
| `Computers`              | `ID_COMPUTER`              |
| `Applications`           | `name`                     |
| `Processes`              | `ID_PROCESS`               |
| `Arguments`              | `ID_ARGUMENT`              |
| `Specifications`         | `ID_SPECIFICATION`         |
| `ArgumentValues`         | `ID_ARGUMENT_VALUE`        |
| `Studies`                | `ID_STUDY`                 |
| `Containers`             | `ID_CONTAINER`             |
| `VisualisationMethods`   | `ID_VISUALISATION_METHOD`  |
| `StatisticalMethods`     | `ID_STATISTICAL_METHOD`    |
| `Visualisations`         | `ID_VISUALISATION`         |
| `Statistics`             | `ID_STATISTIC`             |
| `Parameters`             | `ID_PARAMETER`             |
| `StatisticalVariables`   | `ID_STATISTICAL_VARIABLE`  |
| `Value`                  | `ID_VALUE`                 |

The resulting `provenance.dot` file can be rendered to an image using
Graphviz, for example with `dot -Tpng provenance.dot -o provenance.png`.
For large provenance graphs, `neato` or `sfdp` may produce more legible
layouts than `dot`.

## OPTIONS

This script accepts no options or arguments. The entity types, label
fields, and output path are all hard-coded.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `ssrepi` library cannot be imported from `lib/`; or
- a database connection or query error occurs.

## ENVIRONMENT

The script inherits all database connection environment variables from
the `ssrepi` library. Refer to `ssrepi.py` for the full list.

## RETURN VALUE

Writes the Graphviz DOT representation of the full provenance graph to
`provenance.dot` in the current working directory. Any existing
`provenance.dot` will be overwritten without warning.

## EXAMPLES

Generate the provenance graph and render it to PNG:

    record-image-provenance.py
    dot -Tpng provenance.dot -o provenance.png

Generate and render using a force-directed layout for large graphs:

    record-image-provenance.py
    sfdp -Tsvg provenance.dot -o provenance.svg

## FILES

`lib/ssrepi.py`
: The SSREPI provenance library. Must be importable as `ssrepi`; the
  script appends `lib` to `sys.path` before importing, so `ssrepi.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

`provenance.dot`
: Output Graphviz DOT file written to the current working directory.
  Overwritten on each run without warning.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

This script imports `ssrepi` rather than `record`, unlike every other
script in the RECORD suite. It is unclear whether this is intentional
(the script predates the renaming of the library from SSREPI to RECORD)
or an oversight. If `ssrepi` is simply an alias or earlier version of
`record`, the script should be updated to import `record` for
consistency.

The output path `provenance.dot`, the entity types, and the label
fields are all hard-coded and cannot be changed without editing the
script.

Any existing `provenance.dot` in the current working directory is
silently overwritten.

The `__credits__` field is empty.

The `Value` entity type uses a singular name while all other entity
types use plurals, which may indicate a naming inconsistency in the
underlying schema.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`ssrepi.py`, `record.py`, `record.sh`, `record-image-project.py`,
`record-trace.py`, `record-documentation.py`

## HISTORY

Created as part of the RECORD/SSREPI workflow tools to produce a
Graphviz visualisation of the complete provenance graph, covering all
entity types tracked by the SSREPI provenance system.
