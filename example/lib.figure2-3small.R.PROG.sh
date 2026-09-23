PROG=$(record_application "figure2-3small.R" \
    --description="Some words of wisdom about this script."
) || exit -1

source lib.figure2-3small.R.requirements.hardware.sh
source lib.figure2-3small.R.requirements.software.sh
FOR=figure2-3small.R source lib.figure2-3small.R.input-types.sh
source lib.figure2-3small.R.output-types.sh
source lib.figure2-3small.R.argument-types.sh

record_contributor $PROG $gary_polhill_id author

record_tag $appendix_id --application=$PROG
