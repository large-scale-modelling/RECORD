## SYNOPSIS

`record-image-finegrain.py`

## DESCRIPTION

`record-image-finegrain.py` generates a Graphviz DOT file representing a fine-grained
provenance graph stored in the RECORD database. It queries a broader set
of entity types than `analysis.py`, adding container, container type,
content, and context entities to the node specification, and writes the
resulting graph to the file `finegrain.dot` in the current working
directory.

The script connects to the database using the connection helper provided
by the `ssrepi` library, calls `ssrepi.draw_graph` with the node
specification, and then disconnects cleanly. The node specification
controls which fields are rendered in bold within each node's label when
the corresponding field value is present in the database.

This script is intended to be run after one or more simulation runs have
been recorded in the provenance database, to produce a detailed visual
summary that includes the data containers and their contents alongside the
analytical pipeline entities captured by `analysis.py`.

## OPTIONS

This command takes no command-line options.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if the database connection fails or if `ssrepi.draw_graph`
encounters an error.

## ENVIRONMENT

The script depends on environment variables consumed by the `ssrepi`
library to establish a database connection. Refer to the `ssrepi` (i.e.
`record.py`) documentation for the full list, including `RECORD_DBTYPE`,
`RECORD_DBFILE`, `RECORD_DBUSER`, `RECORD_DBNAME`, `RECORD_POSTGRES_HOST`,
`RECORD_POSTGRES_PORT`, `RECORD_POSTGRES_PASSWORD`, `RECORD_GREMLIN_HOST`,
and `RECORD_GREMLIN_TIMEOUT`.

## RETURN VALUE

None.

## EXAMPLES

Generate the fine-grained provenance graph:

    record-image-finegrain.py

Render the resulting DOT file to a PDF:

    record-image-finegrain.py
    dot -Tpdf finegrain.dot -o finegrain.pdf

## OUTPUT FILES

`finegrain.dot`
: Graphviz DOT representation of the fine-grained provenance graph, written
  to the current working directory. Nodes correspond to entity instances
  from the database; edges represent relationships between them. Orphaned
  nodes (those with no edges) are omitted.

## NODE TYPES

The following entity types are included in the graph. For each type, the
fields listed in parentheses are rendered in bold when present:

`Applications` (`name`)
: Software applications registered in the provenance database.

`Containers` (`ID_CONTAINERS`)
: Data containers (files or directories) associated with simulation runs.

`ContainerTypes` (`ID_CONTAINER_TYPE`)
: Categories of data container, identified by type and format.

`Contents` (`ID_CONTENT`)
: Records of the content held within a container.

`StatisticalMethods` (`ID_STATISTICAL_METHOD`)
: Statistical methods used to analyse simulation outputs.

`StatisticalVariables` (`ID_STATISTICAL_VARIABLE`)
: Variables consumed or produced by statistical analyses.

`VisualisationMethods` (`ID_VISUALISATION_METHOD`)
: Methods used to produce visualisation outputs.

`Parameters` (`ID_PARAMETERS`)
: Parameters associated with models or applications.

`Persons` (`ID_PERSON`)
: Contributors recorded in the provenance database.

`Visualisations` (`ID_VISULISATION`)
: Specific visualisation artefacts produced during a run.

`Assumptions` (`assumption`, `variable`, `person`, `statistics`, `visualisation`)
: Documented assumptions, with multiple fields emboldened when present.

`Statistics` (`ID_STATISTICS`)
: Statistical results recorded during a run.

`Variables` (`ID_VARIABLE`)
: Named variables used by models or arguments.

`Contexts` (`ID_CONTEXT`)
: Contextual metadata associated with simulation runs or entities.

`Value` (`ID_VALUE`)
: Discrete allowed values associated with arguments or variables.

## FILES

`lib/ssrepi.py`
: The SSRepI library providing `connect_db`, `disconnect_db`, and
  `draw_graph`. Must be present in a `lib` subdirectory relative to the
  working directory, or otherwise on the Python path.

`finegrain.dot`
: Output file written to the current working directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The output filename `finegrain.dot` is hard-coded and cannot be overridden
without modifying the script.

The node specification is also hard-coded; adding or removing entity types
requires editing the script directly.

The bold field identifier for `Visualisations` is spelled `ID_VISULISATION`
(missing a letter), which will cause the field to fail silently to embolden
if the actual attribute name in the database is `ID_VISUALISATION`.

The bold field identifier for `Parameters` is `ID_PARAMETERS` (plural),
which may not match the actual attribute name `ID_PARAMETER` (singular)
defined in `record.py`, potentially causing the field to fail silently to
embolden.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`analysis.py`, `record.py`, `record.sh`, `record-run.sh`, `dot(1)`

## HISTORY

Created as part of the RECORD workflow tools to provide a more detailed
graphical overview of provenance than `analysis.py`, by additionally
including data container, container type, content, and context entities
captured during social simulation experiments.
