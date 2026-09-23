#!/usr/bin/env bash

source lib.record.common.sh

if [ -n "$RECORD_SLURM" ]
then
    squeue -h -o "%A %j" | grep $RECORD_SLURM_PREFIX'.*' | awk '{print $1}' | xargs scancel
fi

if [ ! -f "$RECORD_PID_FILE" ]
then
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is not running.")
    exit -1
elif [ -n "$pid_of_record_run" ] && [ -d /proc/${pid_of_record_run} ]
then
    LOGIN_PID=
    for pid in $(pidtree $(cat $RECORD_PID_FILE))
    do
        kill -9 "$pid"
    done
    rm $RECORD_PID_FILE
else
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is not running.")
    exit -1
fi

