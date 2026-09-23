#!/usr/bin/env bash

source lib.record.common.sh

if [ -n "$pid_of_record_run" ] && [ -d /proc/${pid_of_record_run} ]
then
   (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is already running.")
   exit -1
fi

nohup \
    $RECORD_START_PROGRAM > \
    $RECORD_START_PROGRAM.$(date '+%Y-%m-%d').out \
    2>&1 &
echo $! > $RECORD_PID_FILE

(>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM Started!")

