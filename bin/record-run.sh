#!/usr/bin/env bash

# A simple wrapper to allow the running of a slurm or batched job.

. lib/record.sh

[ -n "$DEBUG" ] && (>&2 echo "BASH: RUNNING: record-run.sh $@: Entering...")

record_run "$@"
if [ $? -ne 0 ]
then
    (>&2 echo "BASH: $FUNCNAME $@: SBATCH just failed.")
    exit -1
fi

[ -n "$DEBUG" ] && (>&2 echo "BASH: RUNNING: record-run.sh $@:...exited.")
return 0


