#!/usr/bin/env bash

# This should return the experiment to the state at which it was initialised, so
# after all the preparation scripts have run.

source lib.record.common.sh

if [ -n "$pid_of_record_run" ] && [ -d /proc/${pid_of_record_run} ]
then
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is STILL running.")
    exit -1
fi

rm *.out
rm slurm-outputs/*.out

source lib.record.clean.sh
