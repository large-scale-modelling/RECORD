## SYNOPSIS

`record-import-database.py`

## DESCRIPTION

`record-import-database.py` restores a Gremlin graph database from a
JSON export file, loading all vertices first and then all edges. It is
the import counterpart to a graph export utility and is intended for use
with the Gremlin backend of the RECORD provenance system.

The script uses `ijson` to stream the input file in two passes — one for
the `vertices` array and one for the `edges` array — so arbitrarily large
exports can be imported without loading the entire file into memory.

Progress is reported to standard output every 1,000 successfully loaded
vertices or edges. Failures for individual vertices or edges are reported
to standard error with the affected `T.id`, and processing continues
rather than aborting. A summary of loaded and failed counts, together
with the live vertex and edge counts returned by the graph, is printed at
the end.

The script exits with status 2 if any vertex or edge failed to load,
allowing calling scripts to detect a partial import.

## OPTIONS

This script accepts no command-line options. All configuration is
supplied via environment variables.

## EXIT STATUS

Returns 0 if all vertices and edges were loaded successfully.

Returns 1 if the input JSON file does not exist.

Returns 2 if one or more vertices or edges failed to load.

Returns non-zero if an unhandled exception occurs during connection or
traversal setup.

## ENVIRONMENT

`SSREPI_GREMLIN_HOST`
: WebSocket URL of the Gremlin server. Defaults to
  `ws://localhost:8182/gremlin` if not set.

`GRAPH_JSON`
: Path to the JSON file to import. Defaults to `graph.json` if not set.
  The file must contain a top-level `vertices` array and a top-level
  `edges` array. The script exits with status 1 if the file does not
  exist.

`TRAVERSAL_SOURCE`
: Named traversal source to use when connecting to the Gremlin server.
  Defaults to `g` if not set.

## RETURN VALUE

On completion a restore summary is printed to standard output:

    === RESTORE SUMMARY ===
    V loaded <n> fail <n>   graph V(): <n>
    E loaded <n> fail <n>   graph E(): <n>

Progress lines are also printed to standard output every 1,000
successfully loaded vertices or edges:

    [V] 1000 loaded (fail 0)
    [E] 2000 loaded (fail 1)

Individual failures are reported to standard error:

    [V] FAIL <T.id>: <exception message>
    [E] FAIL <T.id>: <exception message>

## EXAMPLES

Import using all defaults (localhost Gremlin server, `graph.json`):

    record-import-database.py

Import from a specific file against a remote server:

    SSREPI_GREMLIN_HOST=ws://gremlin.example.com:8182/gremlin \
    GRAPH_JSON=/backups/provenance-2024.json \
    record-import-database.py

Check for partial failures in a pipeline:

    record-import-database.py || echo "Import completed with errors"

## INPUT FORMAT

The JSON file must be structured as:

```json
{
  "vertices": [
    { "T.id": "...", "T.label": "...", "<property>": "<value>", ... },
    ...
  ],
  "edges": [
    {
      "T.id": "...",
      "T.label": "...",
      "Direction.OUT": { "T.id": "..." },
      "Direction.IN":  { "T.id": "..." },
      "<property>": "<value>",
      ...
    },
    ...
  ]
}
```

`T.id` and `T.label` are reserved keys. All other keys on a vertex or
edge object are treated as properties. `Direction.OUT` and `Direction.IN`
are required on every edge and must each contain a `T.id` key identifying
the source and target vertices respectively.

## FILES

`graph.json`
: Default input file. Overridden by `GRAPH_JSON`.

## AUTHORS

Doug Salt

## CREDITS

Gary Polhill, Lorenzo Milazzo

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The environment variable for the Gremlin host is named
`SSREPI_GREMLIN_HOST` rather than `RECORD_GREMLIN_HOST` as used by the
rest of the RECORD toolchain, which may cause confusion.

The script accepts no `--help` or `--version` flags, unlike the other
RECORD utilities.

Edge failures do not increment `e_fail` before printing the failure
message; the counter is only incremented in the `except` block, so the
progress line `[E] FAIL ...` is printed correctly but the count reported
in the summary may undercount failures if an exception is raised before
the counter increment is reached.

The bare `except: pass` in the `finally` block silently suppresses any
error raised by `conn.close()`, making connection cleanup failures
invisible.

Property values are passed to Gremlin without type coercion. If the JSON
source contains numeric or boolean values serialised as strings, they
will be stored as strings rather than their native types.

The script makes no attempt to detect or skip vertices or edges that
already exist in the graph, so re-running against a non-empty graph will
produce duplicate-ID errors counted as failures rather than being handled
as upserts.

## COPYRIGHT

Copyright © 2016 The James Hutton Institute. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.py`, `record.sh`, `record-update.py`, `record-truncate-database.py`,
`delete-database.py`, `create-database.py`

## HISTORY

Created as part of the RECORD workflow tools to provide a streaming
import path for restoring Gremlin graph databases from JSON exports
produced by the RECORD workflow system.
