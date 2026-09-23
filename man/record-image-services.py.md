## SYNOPSIS

`record-image-services.py`

## DESCRIPTION

`record-image-services.py` queries the RECORD provenance database and
produces a Graphviz DOT file visualising service-level metadata —
applications, the computers they run on, and the specifications that
define them. It is a narrower counterpart to `record-image-project.py`
and `record-image-provenance.py`, focused specifically on the
infrastructure and software side of the provenance graph rather than
people, studies, or statistical entities.

The script connects to the database via the `ssrepi` library, calls
`ssrepi.draw_graph` with a fixed set of entity types and their label
fields, and writes the result to `services.dot` in the current working
directory.

The graph includes the following entity types, labelled by the specified
field:

| Entity type       | Label field         |
|--------------------|---------------------|
| `Applications`     | `name`              |
| `Computers`        | `ID_COMPUTER`       |
| `Specifications`   | `ID_SPECIFICATION`  |

The resulting `services.dot` file can be rendered to an image using
Graphviz, for example with `dot -Tpng services.dot -o services.png`.

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

Writes the Graphviz DOT representation of the services metadata graph to
`services.dot` in the current working directory. Any existing
`services.dot` will be overwritten without warning.

## EXAMPLES

Generate the services graph and render it to PNG:

    record-image-services.py
    dot -Tpng services.dot -o services.png

## FILES

`lib/ssrepi.py`
: The SSREPI provenance library. Must be importable as `ssrepi`; the
  script appends `lib` to `sys.path` before importing, so `ssrepi.py`
  must be present in a `lib/` subdirectory relative to the working
  directory.

`services.dot`
: Output Graphviz DOT file written to the current working directory.
  Overwritten on each run without warning.

## AUTHORS

Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

This script imports `ssrepi` rather than `record`, unlike most other
scripts in the RECORD suite (with the exception of
`record-image-provenance.py`, which has the same inconsistency). It is
unclear whether this is intentional (the script predates the renaming
of the library from SSREPI to RECORD) or an oversight.

The output path `services.dot`, the entity types, and the label fields
are all hard-coded and cannot be changed without editing the script.

Any existing `services.dot` in the current working directory is
silently overwritten.

The `__credits__` field is empty.

The graph as configured contains no edges between `Applications`,
`Computers`, and `Specifications` unless `ssrepi.draw_graph` derives
relationships automatically from foreign keys; the script itself
supplies no explicit relationship information.

The word "services" in the module comment is misspelled as "serivces".

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`ssrepi.py`, `record.py`, `record-image-project.py`,
`record-image-provenance.py`, `record-documentation.py`

## HISTORY

Created as part of the RECORD/SSREPI workflow tools to produce a
Graphviz visualisation focused on service-level metadata: the
applications, computers, and specifications that make up the
infrastructure side of a provenance record.
