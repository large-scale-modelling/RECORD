
#!/usr/bin/env bash

source lib.record.common.sh

if [ ! -f "$RECORD_PID_FILE" ]
then
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is not running.")
    exit -1
elif [ -n "$pid_of_record_run" ] && [ -d /proc/${pid_of_record_run} ]
then
    tail -f $(get_stderr $(head -1 "$RECORD_PID_FILE"))
else
    (>&2 echo $BASH_SOURCE": "$(date)": $RECORD_START_PROGRAM is not running.")
    exit -1
fi
