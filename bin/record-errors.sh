#!/usr/bin/env bash

source lib.record.common.sh

if [ -f "$RECORD_PID_FILE" ] && [ -f $(get_stderr $(head -1 "$RECORD_PID_FILE")) ]
then
    check_for_errors $(get_stderr $(head -1 "$RECORD_PID_FILE"))
else
    for file in *out
    do
#        if [ -f "$file" ]
#        then
#            read -p "Do you wish to inspect this out file, $file? (Y/N/Q)" ynq
#            case $ynq in
#                [Yy]* ) check_for_errors "$file";;
#                [Qq]* ) exit;;
#                [Nn]* ) :;;
#                * ) echo "Please answer yes or quit.";;
#            esac
#        fi
        check_for_errors "$file"
    done
fi

for file in slurm-outputs/*.out
do
    check_for_errors "$file"
done
