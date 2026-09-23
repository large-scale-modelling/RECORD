#!/usr/bin/env bash

source lib.record.common.sh

for out in slurm*out
do
    check_for_errors $out
done
