# figure 5
# ========

PROG=$(record_application "treehist3.pl" \
    --description="Some documentation here, please." \
) || exit -1

source lib.treehist3.pl.requirements.software.sh
source lib.treehist3.pl.requirements.hardware.sh
FOR=treehist3.pl source lib.treehist3.pl.input-types.sh
source lib.treehist3.pl.output-types.sh
source lib.treehist3.pl.argument-types.sh

# Metadata
# --------

record_contributor $PROG $gary_polhill_id Developer
record_contributor $PROG $gary_polhill_id Author

#source lib.treehist3.pl.finegrain.sh
