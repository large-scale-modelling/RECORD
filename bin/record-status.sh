#!/usr/bin/env bash

source lib.record.common.sh

if [ -n "$pid_of_record_run" ] && [ -d /proc/${pid_of_record_run} ]
then
    for pid in $(pidtree  $(head -1 $RECORD_PID_FILE))
    do 
        ps --no-headers -f $pid
    done
else
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is not running.")
    [ -f $RECORD_PID_FILE ] && rm $RECORD_PID_FILE
    exit -1
fi

