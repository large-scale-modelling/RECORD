PROG=$(record_application figure2-3s.R \
    --description="""
    Need some stuff here.
    Produces a sunflow plot for the paper
""" \
) || exit -1

source lib.figure2-3s.R.requirements.software.sh
source lib.figure2-3s.R.requirements.hardware.sh
FOR=figure2-3s.R source lib.figure2-3s.R.input-types.sh
source lib.figure2-3s.R.output-types.sh
source lib.figure2-3s.R.argument-types.sh

# Metadata
# --------

record_contributor $PROG $gary_polhill_id Developer
record_contributor $PROG $gary_polhill_id Author

record_tag $figure_for_a_paper_id --application=$PROG
record_tag $figure_four_id --application=$PROG

#source lib.figure2-3s.R.finegrain.sh

