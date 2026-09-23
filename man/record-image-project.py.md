## SYNOPSIS

`record-image-project.py`

## DESCRIPTION

`record-image-project.py` queries the RECORD provenance database and
produces a Graphviz DOT file visualising the project-level metadata
graph. It connects to the database via the `record` library, calls
`record.draw_graph` with a fixed set of entity types and their label
fields, and writes the result to `project.dot` in the current working
directory.

The graph includes the following entity types, labelled by the specified
field:

| Entity type     | Label field        |
|-----------------|--------------------|
| `Persons`       | `ID_PERSON`        |
| `Projects`      | `ID_PROJECT`       |
| `Applications`  | `name`             |
| `Documentation` | `ID_DOCUMENTATION` |
| `Boxes`         | `ID_BOX`           |

The resulting `project.dot` file can be rendered to an image using
Graphviz, for example with `dot -Tpng project.dot -o project.png`.

## OPTIONS

This script accepts no options or arguments. The entity types, label
fields, and output path are all hard-coded.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if:

- the `record` library cannot be imported from `lib/`; or
- a database connection or query error occurs.

## ENVIRONMENT

The script inherits all database connection environment variables from
the `record` library. Refer to `record.py` for the full list, including:

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or
  `gremlin`.

`RECORD_DBFILE`
: Path to the SQLite database file. Used when `RECORD_DBTYPE` is `sqlite3`.

`RECORD_DBUSER`
: PostgreSQL username. Used when `RECORD_DBTYPE` is `postgres`.

`RECORD_DBNAME`
: PostgreSQL database name. Used when `RECORD_DBTYPE` is `postgres`.

`RECORD_POSTGRES_HOST`
: PostgreSQL hostname.

`RECORD_POSTGRES_PORT`
: PostgreSQL port number.

`RECORD_POSTGRES_PASSWORD`
: PostgreSQL password. Required when `RECORD_DBTYPE` is `postgres`.

`RECORD_GREMLIN_HOST`
: WebSocket URL of the Gremlin server.

`RECORD_GREMLIN_TIMEOUT`
: Per-query evaluation timeout in milliseconds.

`RECORD_DEBUG`
: When set, enables verbose diagnostic output to standard error.

## RETURN VALUE

Writes the Graphviz DOT representation of the project metadata graph to
`project.dot` in the current working directory. Any existing `project.dot`
file will be overwritten without warning.

## EXAMPLES

Generate the project graph and render it to PNG:

    record-image-project.py
    dot -Tpng project.dot -o project.png

Generate and render to SVG for use in documentation:

    record-image-project.py
    dot -Tsvg project.dot -o project.svg

## FILES

`lib/record.py`
: The RECORD provenance library. Must be importable as `record`; the
  script appends `lib` to `sys.path` before importing, so `record.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

`project.dot`
: Output Graphviz DOT file written to the current working directory.
  Overwritten on each run without warning.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The output path `project.dot`, the entity types, and the label fields
are all hard-coded and cannot be changed without editing the script.

Any existing `project.dot` in the current working directory is silently
overwritten.

Debug output is unconditionally enabled by `record.debug = True` at
module level in `record.py` and cannot be suppressed via the
`RECORD_DEBUG` environment variable.

The `__credits__` field is empty.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `record-trace.py`,
`record-documentation.py`

## HISTORY

Created as part of the RECORD workflow tools to produce a Graphviz
visualisation of project-level provenance metadata, covering persons,
projects, applications, documentation, and data boxes.
EOF
