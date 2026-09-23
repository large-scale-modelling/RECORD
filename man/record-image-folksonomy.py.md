## SYNOPSIS

`folksonomy.py`

## DESCRIPTION

`folksonomy.py` generates a Graphviz DOT file representing the folksonomy
metadata graph stored in the RECORD database. It queries the subset of
entity types concerned with tagging and classification — tags, applications,
container types, studies, documentation, statistical methods, and
visualisation methods — and writes the resulting graph to the file
`folksonomy.dot` in the current working directory.

The script connects to the database using the connection helper provided
by the `ssrepi` library, calls `ssrepi.draw_graph` with the node
specification, and then disconnects cleanly. The node specification
controls which fields are rendered in bold within each node's label when
the corresponding field value is present in the database.

This script is intended to be run after one or more simulation runs have
been recorded in the provenance database, to produce a visual summary of
how tags have been applied across applications, container types, studies,
documentation, and analytical method entities.

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

Generate the folksonomy metadata graph:

    folksonomy.py

Render the resulting DOT file to a PDF:

    folksonomy.py
    dot -Tpdf folksonomy.dot -o folksonomy.pdf

## OUTPUT FILES

`folksonomy.dot`
: Graphviz DOT representation of the folksonomy metadata graph, written
  to the current working directory. Nodes correspond to entity instances
  from the database; edges represent relationships between them. Orphaned
  nodes (those with no edges) are omitted.

## NODE TYPES

The following entity types are included in the graph. For each type, the
fields listed in parentheses are rendered in bold when present:

`Tags` (`ID_TAG`)
: Free-text tags applied to entities via the folksonomy system.

`Applications` (`name`)
: Software applications registered in the provenance database.

`ContainerTypes` (`ID_CONTAINER_TYPE`)
: Categories of data container, identified by type and format.

`Studies` (`ID_STUDY`)
: Research studies within a project, associated with tagged entities.

`Documentation` (`ID_DOCUMENTATION`)
: Documentation artefacts linked to applications or other entities.

`StatisticalMethods` (`ID_STATISTICAL_METHOD`)
: Statistical methods used to analyse simulation outputs.

`VisualisationMethods` (`ID_VISUALISATION_METHOD`)
: Methods used to produce visualisation outputs.

## FILES

`lib/ssrepi.py`
: The SSRepI library providing `connect_db`, `disconnect_db`, and
  `draw_graph`. Must be present in a `lib` subdirectory relative to the
  working directory, or otherwise on the Python path.

`folksonomy.dot`
: Output file written to the current working directory.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The output filename `folksonomy.dot` is hard-coded and cannot be overridden
without modifying the script.

The node specification is also hard-coded; adding or removing entity types
requires editing the script directly.

The `os` module is imported but never used.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`analysis.py`, `finegrain.py`, `record.py`, `record.sh`, `dot(1)`

## HISTORY

Created as part of the RECORD workflow tools to provide a graphical
overview of the folksonomy metadata captured during social simulation
experiments, showing how tags relate to applications, container types,
studies, documentation, and analytical methods.
