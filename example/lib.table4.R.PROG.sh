# table 4 paper CSV
# =================

PROG=$(record_application table4.R \
    --description="""
    A small script to prodce a text version of the table found in
    Polhil et al (2013) - Nonlinearities in biodiversity incentive
    schemes: A study using an integrated agent-based and
    metacommunity model The original diagram was done with a
    mixture of R and Excel. I have automated this part.
""" \
) || exit -1


source lib.table4.R.requirements.software.sh
source lib.table4.R.requirements.hardware.sh
FOR=table4.R source lib.table4.R.input-types.sh
source lib.table4.R.output-types.sh
source lib.table4.R.argument-types.sh


