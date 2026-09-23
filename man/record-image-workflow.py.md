## SYNOPSIS

`record-image-workflow.py`

## DESCRIPTION

`record-image-workflow.py` queries the RECORD provenance database and
produces a Graphviz DOT file visualising the workflow-definition layer
of the provenance graph — applications, pipelines, methods, variables,
and the parameters and arguments that connect them. It sits alongside
`record-image-project.py`, `record-image-services.py`, and
`record-image-provenance.py` as one of several focused views over
different slices of the full provenance model.

The script connects to the database via the `ssrepi` library, calls
`ssrepi.draw_graph` with a fixed set of entity types and their label
fields, and writes the result to `workflow.dot` in the current working
directory.

The graph includes the following entity types, labelled by the specified
field:

| Entity type             | Label field                |
|--------------------------|----------------------------|
| `Applications`          | `name`                     |
| `Pipelines`              | `ID_PIPELINE`              |
| `StatisticalMethods`    | `ID_STATISTICAL_METHOD`    |
| `ContainerTypes`        | `ID_CONTAINER_TYPE`        |
| `StatisticalVariables`  | `ID_STATISTICAL_VARIABLE`  |
| `Variables`             | `ID_VARIABLE`               |
| `VisualisationMethods`  | `ID_VISUALISATION_METHOD`  |
| `Parameters`            | `ID_PARAMETER`              |
| `Arguments`             | `ID_ARGUMENT`               |

The resulting `workflow.dot` file can be rendered to an image using
Graphviz, for example with `dot -Tpng workflow.dot -o workflow.png`.

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

Writes the Graphviz DOT representation of the workflow metadata graph to
`workflow.dot` in the current working directory. Any existing
`workflow.dot` will be overwritten without warning.

## EXAMPLES

Generate the workflow graph and render it to PNG:

    record-image-workflow.py
    dot -Tpng workflow.dot -o workflow.png

## FILES

`lib/ssrepi.py`
: The SSREPI provenance library. Must be importable as `ssrepi`; the
  script appends `lib` to `sys.path` before importing, so `ssrepi.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

`workflow.dot`
: Output Graphviz DOT file written to the current working directory.
  Overwritten on each run without warning.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

This script imports `ssrepi` rather than `record`, consistent with
`record-image-provenance.py` and `record-image-services.py` but
inconsistent with the rest of the RECORD suite (notably
`record-image-project.py`, which uses `record`). This is now the third
"image" script with this inconsistency, reinforcing that it is likely a
legacy artefact from before the library was renamed from SSREPI to
RECORD, rather than three independent oversights.

Unlike `record-image-project.py` and `record-image-services.py`, this
script calls `ssrepi.draw_graph(conn, nodes, "workflow.dot")` with the
output path as a positional argument rather than the keyword argument
`output="workflow.dot"`. If `draw_graph`'s signature does not accept the
output path positionally in that position, this will raise a `TypeError`
or silently bind to the wrong parameter.

The output path `workflow.dot`, the entity types, and the label fields
are all hard-coded and cannot be changed without editing the script.

Any existing `workflow.dot` in the current working directory is
silently overwritten.

The `__credits__` field is empty.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`ssrepi.py`, `record.py`, `record-image-project.py`,
`record-image-services.py`, `record-image-provenance.py`

## HISTORY

Created as part of the RECORD/SSREPI workflow tools to produce a
Graphviz visualisation focused on the workflow-definition layer of the
provenance graph: applications, pipelines, statistical and
visualisation methods, and their parameters and arguments.
