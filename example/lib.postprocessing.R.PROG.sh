PROG=$(record_application postprocessing.R \
    --description="
    A small R script that emaulates what Gary did with the outputs from the
    model in an R script. That is it reconstructs what he did
    originally in what we presume was an interactive R
    session. Essentially this scrpt takes the combined results from the
    model and:

    1. Adds two empty columns TSNE.1.X and TSNE.1.Y - this were going to be
    used for visualisation of the data, but were late abaondoned. The columns have
    been retained, so that they do not mess up any subsequent programs that use the
    output.

    2. Adds an incentive column.

    3. Removes the high bankruptcy rates.

    4. Removes high expenditure." \
) || exit -1

source lib.postprocessing.R.requirements.software.sh
source lib.postprocessing.R.requirements.hardware.sh
source lib.postprocessing.R.input-types.sh
FOR=postprocessing.R source lib.postprocessing.R.output-types.sh
source lib.postprocessing.R.argument-types.sh

# Metadata
# --------

record_contributor $PROG $doug_salt_id Developer
record_contributor $PROG $doug_salt_id Author

