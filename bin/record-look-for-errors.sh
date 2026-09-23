#!/usr/bin/env bash

grep --color -n -H ": line" $@ && exit
grep --color -n -H "line " $@ | grep -v "Pipeline = " && exit
grep --color -n -H -i "error" $@ | grep -v -- '--error=' && exit
grep --color -n -H "Trace" $@ && exit
grep --color -n -H "does not exist" $@ && exit
