PROG=$(record_application figure2-3part.R \
    --description="""
    Produces 6 graphs for figure 3 for the paper.  The
    configurations to select this graphs are kept in a
    configuration file, unlike other code this does not take these
    scenarios from the commmand line
""" \
) || exit -1

source lib.figure2-3part.R.requirements.software.sh
source lib.figure2-3part.R.requirements.hardware.sh
FOR=figure2-3part.R source lib.figure2-3part.R.input-types.sh
source lib.figure2-3part.R.output-types.sh
source lib.figure2-3part.R.argument-types.sh

#source lib.figure2-3part.R.finegrain.sh


