## SYNOPSIS

`import record`

## DESCRIPTION

`record.py` (internally known as `ssrepi.py`) is the Python library that
implements the Social Simulation Repository Interface (SSRepI) for the
RECORD workflow system. It provides an object-relational mapping layer
over a provenance database and is the foundational module consumed by
helper scripts such as `update.py`, `exists.py`, `get-value.py`, and
`create-database.py`.

The library models experimental provenance as a graph of entity classes.
Each class corresponds to a table in the relational schema (SQLite 3 or
PostgreSQL) or to a vertex label in a Gremlin-compatible graph database.
All entity classes inherit from the `Table` base class, which provides
common persistence operations (`add`, `update`, `query`, `exists`,
`search`) and common metadata fields (`CREATED`, `CREATOR`, `MODIFIED`,
`MODIFIER`, `DESCRIPTION`, `NAME`, `ABOUT`).

The active database backend is selected at import time via the
`RECORD_DBTYPE` environment variable. Supported backends are `sqlite3`,
`postgres`, and `gremlin` (the default). Connection parameters are read
from additional environment variables described under ENVIRONMENT below.

In addition to the entity classes, `record.py` provides utility functions
for generating provenance graphs using Graphviz and for encoding and
decoding string-based vertex identifiers for use in the Gremlin backend.

## CLASSES

### Table

Base class from which all entity classes inherit. Provides the following
methods:

`add(conn)`
: Inserts a new record into the database. Raises `InvalidEntity` if no
  primary key value is set. Raises `GremlinVertexExists` if the vertex
  already exists in a Gremlin database.

`exists(conn)`
: Returns `True` if a record with the current primary key already exists in
  the database, `False` otherwise.

`query(conn)`
: Populates the instance attributes from the database row matching the
  current primary key. Raises `InvalidEntity` if no primary key is set.

`update(conn)`
: Updates the database row corresponding to the current primary key with
  the current instance attribute values. Records `MODIFIER` and `MODIFIED`
  automatically.

`search(conn, equals)`
: Returns a list of primary key values for rows matching the key-value
  pairs supplied in the *equals* dictionary. Supports SQL `LIKE` wildcards
  (`%`, `_`) and, for the Gremlin backend, edge-based traversal for
  foreign-key columns.

`setValues(values)`
: Sets instance attributes from a dictionary. Raises `InvalidEntity` for
  unrecognised column names.

`validate()`
: Validates common fields. Raises `InvalidEntity` if `ABOUT` is not a
  valid absolute IRI/URI, if `CREATED` is not an ISO 8601 timestamp, or if
  `ID_*` fields do not contain the entity-type token as a substring.

`getDict()`
: Returns the instance attribute dictionary.

`getPrimaryKeys()`
: Returns a SQL `WHERE` clause fragment built from the current primary key
  values, or an empty string if no key is set.

`count(conn)` *(class method)*
: Returns the number of rows in the table.

`getAttributes()` *(class method)*
: Returns the column names defined by the class.

`foreignKeys()` *(class method)*
: Parses the SQL schema string and returns a list of foreign key
  descriptors, each a dictionary with keys `sourceTable`, `sourceColumn`,
  `targetTable`, and `targetColumn`.

`is_relation()` *(class method)*
: Returns `True` if the table is a many-to-many relation (all parts of its
  composite primary key are foreign keys).

`createTable(conn)` *(class method)*
: Executes the class's SQL schema to create the database table if it does
  not already exist.

`dropTable(conn)` *(class method)*
: Drops the table and cascades.

`truncateTable(conn)` *(class method)*
: Truncates the table and cascades.

### Entity Classes

The following classes are defined, each specialising `Table` with its own
schema, primary key definition, and (where applicable) a `validate`
override enforcing domain constraints.

`Application`
: A software application or script. Fields include `ID_APPLICATION`,
  `PURPOSE`, `VERSION`, `LICENCE`, `LANGUAGE`, `ENVS`, `SEPARATOR`,
  `CALLS_APPLICATION`, `CALLS_PIPELINE`, `REVISION`, `MODEL`, and
  `LOCATION` (foreign key to `Box`).

`Argument`
: A formal argument type accepted by an `Application`. Fields include
  `ID_ARGUMENT`, `TYPE` (one of `required`, `option`, or `flag`),
  `ORDER_VALUE`, `ASSIGNMENT_OPERATOR`, `SEPARATOR` (one of `--`, `-`,
  or `/`), `SHORT_NAME`, `SHORT_SEPARATOR`, `ARITY`, `ARGSEP`, `RANGE`,
  `VARIABLE`, and `APPLICATION`.

`ArgumentValue`
: A concrete value supplied for an `Argument` in a particular `Process`.
  Fields include `HAS_VALUE`, `BOX`, `FOR_PROCESS`, and `FOR_ARGUMENT`.

`Assumption`
: A documented assumption associated with an `Application`.

`Assumes`
: Relation linking an `Application` to one or more `Assumption` entities.

`Box`
: A file or directory artefact. Fields include `ID_BOX`, `LOCATION_VALUE`,
  `LOCATION_TYPE` (e.g. `local`), `INSTANCE` (foreign key to `BoxType`),
  `ENCODING`, `SIZE`, `MODIFICATION_TIME`, `UPDATE_TIME`, `HASH`,
  `OUTPUT_OF` (foreign key to `Process`), and `LOCATION_APPLICATION`.

`BoxType`
: A category of `Box`, identified by a MIME type (`FORMAT`) and a
  matching expression (`IDENTIFIER`). The identifier may be prefixed with
  `magic:` for libmagic pattern matching or `name:` for file-name pattern
  matching.

`Computer`
: A compute node. Fields include `ID_COMPUTER`, `HOST_ID`, `IP_ADDRESS`,
  and `MAC_ADDRESS`.

`Dependency`
: A dependency relationship between two `Application` entities.  Fields
  include `DEPENDANT`, `DEPENDENCY`, and `OPTIONALITY`.

`Documentation`
: A documentation artefact associated with an entity.

`Entailment`
: A logical entailment linking two entities.

`Implements`
: Relation linking an `Application` to a `Model`.

`Involvement`
: Relation linking a `Person` to a `Project` or `Study`.

`Meets`
: Records that a `Computer` satisfies a hardware or software
  `Requirement`. Fields include `COMPUTER_SPECIFICATION` and
  `REQUIREMENT_SPECIFICATION`.

`Model`
: A computational model described or implemented by one or more
  `Application` entities.

`Parameter`
: A parameter associated with a `Model` or `Application`.

`Person`
: A contributor. Fields include `ID_PERSON`, `NAME`, and `EMAIL`.

`PersonalData`
: Sensitive personal data fields extending `Person`.

`Pipeline`
: A sequential ordering of `Application` executions. Fields include
  `ID_PIPELINE`, `FIRST` (foreign key to `Application`), and `NEXT`
  (foreign key to `Pipeline`).

`Process`
: A single execution of an `Application`. Fields include `ID_PROCESS`,
  `SOME_USER`, `WORKING_DIR`, `HOST`, `EXECUTABLE`, `START_TIME`, and
  `END_TIME`.

`Product`
: Declares that an `Application` produces outputs of a given `BoxType`.
  Fields include `APPLICATION`, `BOX_TYPE`, `LOCATOR`, and `OPTIONALITY`.

`Project`
: A research project grouping one or more `Study` entities.

`Requirement`
: A hardware or software requirement for an `Application`. Fields include
  `APPLICATION`, `MINIMUM`, and `EXACT` (foreign keys to `Specification`).

`Specification`
: A measured characteristic of a `Computer`. Fields include
  `ID_SPECIFICATION`, `SPECIFICATION_OF`, and `VALUE`.

`StatisticalInput`, `StatisticalMethod`, `StatisticalVariable`, `Statistics`
: Classes supporting the recording of statistical analyses associated with
  simulation outputs.

`Study`
: A research study within a `Project`.

`Tag`, `TagMap`
: Free-text tagging of entities via a folksonomy.

`Use`
: Declares that an `Application` consumes inputs of a given `BoxType`.
  Fields include `APPLICATION`, `BOX_TYPE`, `LOCATOR`, and `OPTIONALITY`.

`User`
: A system account associated with a `Person`. Fields include `ID_USER`,
  `HOME_DIR`, and `ACCOUNT_OF`.

`Value`
: A discrete allowed value for an `Argument`.

`Variable`
: A named variable used by a `Model` or `Argument`.

`Visualisation`, `VisualisationMethod`, `VisualisationValue`
: Classes supporting the recording of visualisation outputs produced by
  simulation runs.

### Exceptions

`InvalidEntity`
: Raised when field validation fails or when a required primary key is
  absent.

`GremlinDBError`
: Raised when a Gremlin query cannot be constructed (for example, because
  no vertex identifier could be derived).

`GremlinVertexExists`
: Raised by `add` when the vertex already exists in the Gremlin database.

## MODULE-LEVEL FUNCTIONS

`is_path(s)` → `bool`
: Returns `True` if *s* is a path to an existing file or directory.

`is_iri(s)` → `bool`
: Returns `True` if *s* parses as a valid IRI according to RFC 3987.

`dict_factory(cursor, row)` → `dict`
: SQLite row factory that returns rows as dictionaries keyed by column name.

`draw_graph(conn, nodes, output)`
: Queries the database for the supplied node set, resolves edges between
  them, removes orphaned nodes, and writes the resulting Graphviz DOT
  representation to *output* (or to standard output if *output* is `None`).

`get_nodes(conn, nodes, labels)` → `dict`
: Fetches node data for the specified node specification and label mapping
  from the database, adds them to a Graphviz `Digraph`, and returns the
  active node dictionary.

`get_edges(conn, edges, activeNodes)` → `dict`
: Fetches edges linking the supplied active nodes from the database and
  returns them as a dictionary mapping `((sourceTable, id), (targetTable,
  id))` pairs to edge labels.

`save_dot(nodes, edges, output=None)`
: Renders a node and edge dictionary to Graphviz DOT format and writes the
  result to *output* or to standard output.

`remove_orphans(nodes, edges)` → `dict`
: Filters *nodes* to retain only those that appear in at least one edge in
  *edges*.

`remove_edges(nodes, edges)` → `dict`
: Filters *edges* to retain only those whose source and target nodes both
  appear in *nodes*.

`encodeIndex(stringIndex)` → `int`
: Encodes a string as an integer by treating each character as a base-256
  digit. Used to produce numeric vertex identifiers for the Gremlin
  backend.

`decodeIndex(numericIndex)` → `str`
: Reverses the encoding performed by `encodeIndex`.

`gremlin_safe_string(s)` → `str`
: Escapes backslashes and newline characters in *s* to produce a string
  safe for embedding in a Gremlin query.

## ENVIRONMENT

`RECORD_DBTYPE`
: Selects the database backend. One of `sqlite3`, `postgres`, or `gremlin`
  (default: `gremlin`).

`RECORD_DBFILE`
: Path to the SQLite database file (default: `ssrepi.db` in the current
  working directory). Used when `RECORD_DBTYPE` is `sqlite3`.

`RECORD_DBUSER`
: PostgreSQL username (default: `ds42723`). Used when `RECORD_DBTYPE` is
  `postgres`.

`RECORD_DBNAME`
: PostgreSQL database name (default: `ssrepi`). Used when `RECORD_DBTYPE`
  is `postgres`.

`RECORD_POSTGRES_HOST`
: PostgreSQL hostname (default: `localhost`).

`RECORD_POSTGRES_PORT`
: PostgreSQL port number (default: `5432`).

`RECORD_POSTGRES_PASSWORD`
: PostgreSQL password. Required when `RECORD_DBTYPE` is `postgres`.

`RECORD_GREMLIN_HOST`
: WebSocket URL of the Gremlin server (default:
  `ws://localhost:8182/gremlin`). Used when `RECORD_DBTYPE` is `gremlin`.

`RECORD_GREMLIN_TIMEOUT`
: Per-query evaluation timeout for Gremlin in milliseconds (default:
  `30000`).

`RECORD_DEBUG`
: When set, enables verbose diagnostic output to standard error.

## RETURN VALUE

Not applicable. `record.py` is a library module.

## EXAMPLES

Connecting to a SQLite database and recording an application:

    import os, record
    os.environ['RECORD_DBTYPE'] = 'sqlite3'
    os.environ['RECORD_DBFILE'] = '/path/to/ssrepi.db'

    import sqlite3
    conn = sqlite3.connect(os.environ['RECORD_DBFILE'])
    conn.row_factory = record.dict_factory

    app = record.Application({'ID_APPLICATION': 'application_my_sim',
                              'NAME': 'my_sim',
                              'LANGUAGE': 'Python'})
    try:
        app.add(conn)
    except record.GremlinVertexExists:
        app.update(conn)
    conn.commit()

Querying an existing process record:

    proc = record.Process({'ID_PROCESS': 'process_abc123'})
    proc.query(conn)
    print(proc.START_TIME, proc.END_TIME)

Checking whether a box exists:

    box = record.Box({'ID_BOX': 'box_987654'})
    if not box.exists(conn):
        box.LOCATION_VALUE = '/data/output.csv'
        box.LOCATION_TYPE  = 'local'
        box.add(conn)

## FILES

`ssrepi.db`
: Default SQLite database file, created in the current working directory
  when `RECORD_DBTYPE` is `sqlite3`.

## AUTHORS

Lorenzo Milazzo, J. Gary Polhill, Doug Salt

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The `debug` flag is hard-coded to `True` at module level, overriding the
`RECORD_DEBUG` environment variable check immediately above it.

The `search` method contains a partially commented-out alternative
implementation. The active implementation may not correctly handle
foreign-key column searches under all Gremlin configurations.

`encodeIndex` and `decodeIndex` use a byte-by-byte base-256 encoding that
may produce large integers for long strings; the authors note this may not
be the best approach.

The `update` method for the Gremlin backend attempts to drop existing edges
by edge identifier, but the deletion query uses the foreign-key value as
the edge identifier rather than the actual edge ID, which may not behave as
intended in all Gremlin server configurations.

## COPYRIGHT

Copyright © 2015, 2022 The James Hutton Institute.  License GPLv3+: GNU
GPL version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`record.sh`, `record-clean.sh`, `record-run.sh`, `update.py`,
`exists.py`, `get-value.py`, `create-database.py`

## HISTORY

Originally developed as `ssrepi.py` for the Social Simulation Repository
Interface project (Polhill et al. "Towards metadata standards for social
simulation outputs"), then extended and incorporated into the RECORD
workflow system to provide multi-backend provenance capture for simulation
experiments.
