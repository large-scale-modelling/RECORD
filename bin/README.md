# PURPOSE

Contains all the Python and Bash scripts to utilise RECORD.

# MANIFEST

+ `lib.record.common.sh` - Bash source script, contains commonalities for the control scripts
+ `README.md` - this file
+ `record-check-slurm-journals.sh` - control script - looks for errors in the slurm journals found in `slurm-outputs`.
+ `record-clean.sh` - control script - tidies up minimally for a new run.
+ `record-create-database.py` - used by Bash programs to create the database. The empty database ssrepi must be present for this to work in postgres and sqlite
+ `record-create-edge.py` - legacy program for gremlin based databases - creates an edge between two nodes and any remaining parameter pairs are treated as edge properties.
+ `record-delete-database.py` - control script - completely wipes out a database - USE WITH CARE.
+ `record-documentation.py` - control script - produces the schamata in markdown table form. Done this way because the word document kept getting out of date, so this framework is now officially self-documenting.
+ `record-edit.sh` - control script - edits the current main out file if a run is going.
+ `record-errors.sh` - control script - displays any errors found in the standard log files - takes no arguments.
+ `record-exists.py` - checks whether a give row in a table or node in a graph database exists.
+ `record-export-database.py` - exports the database to JSON if a Tinkerpop graph database. 
+ `record-get-arguments.jl` - preprocessor to generate some of the source files needed.This is a pre-version of `record-preprocess.jl` which is a superset of this program.
+ `record-get-folksonomy-table.sh` - control script - lists out the defined tags.
+ `record-get-value.py` - used by Bash scripts to return a single value from the database given the primary key.
+ `record-image-analysis.py` - takes the SQL database and draws the anlaysis sub graph for Graphviz.
+ `record-image-finegrain.py` - converted - uses the SQL database to construct the fine\_grain graph for Graphviz.
+ `record-image-folksonomy.py` - converted - utilises SQL database to produce the folksonomy sub-graph for Graphviz.
+ `record-image-project.py` - uses the SQL database to produce the project sub-graph for Graphviz.
+ `record-image-provenance.py` - used the database to produce the provenance sub-graph for Graphviz.
+ `record-image-services.py` - used to create the services sub-graph from the SQL database for Graphviz.
+ `record-image-tbox.py` - used to create all the types, i.e. the schemata - this is used for the documentation - my plan is to do it in mermaid.
+ `record-image-workflow.py` - converted - This is an adhoc prgram to produce the workflow graph from the SQL database for Graphviz.
+ `record-import-database.py` - control script - import a JSON database. Only works for Tinkerpop at the moment - I wish to make it universal.
+ `record-look-for-errors.sh` - control script - this looks for errors in a named file (first argument).
+ `record-mr-proper.sh` - control script - wipes out everything back to a clean state before running - USE WITH CARE.
+ `record-preprocess.jl` - will (eventually) produce all the shell scripts for the a program or script. This will be run once to create the shell-scripts.
+ `record-run.sh` - used by `record.sh` to launch a batch process - this should never be called directly.
+ `record-search.py` - given values returns a node(s) or table(s) that match the inputs.
+ `record-start.sh` - control script - starts everything off.
+ `record-status.sh` - control script - tells you if the system is currently running.
+ `record-stop.sh` - control script - kills the current run.
+ `record-tail.sh` - control script - tails of the default log for this run - good for checking stuff is working, kinda.
+ `record-totals.py`  control script -- counts the number of rows in the SSREPI database.
+ `record-trace.py` - 
+ `record-truncate-database.py` - empties a database - this is not applicable to Tinkerpop databases - USE WITH CARE.
+ `record-update.py` - used by the Bash scripts to insert/update a database record.
+ `trace-recurse.sh` -
+ `trace.sh` - Follows a query through a set 
