#!/bin/bash
#
# gen-readme.sh - Generate a README.md MANIFEST section from a file listing.
#
# Usage:
#   ./gen-readme.sh $(ls -1) > README.md
#   ./gen-readme.sh *
#
# Each argument becomes one manifest entry. The line for README.md itself
# is auto-annotated as "this file". All other entries are left blank for
# you to fill in.

set -euo pipefail

readme_name="README.md"

echo """# PURPOSE

The purpose of this directory is

# MANIFEST
""" >> $readme_name

for f in "$@"
do
    if [ "$f" = "$readme_name" ]
    then
        echo "+ \`${f}\` - this file." >> $readme_name
    else
        echo "+ \`${f}\` - " >> $readme_name
    fi
done
