#!/usr/bin/env bash

source lib.record.common.sh

echo "Are you really sure you want to do this? This will stop everything and clear the provenance database. Delete any initialisation and output files"

read -p  "Type uppercase 'YES' if you really want to do this. " ANSWER


if ! [[ "$ANSWER" == "YES" ]]
then
    exit -1
fi

record-stop.sh
record-clean.sh
record-delete-database.py --force

source lib.record.mrproper.sh



