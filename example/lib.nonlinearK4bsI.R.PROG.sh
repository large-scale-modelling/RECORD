PROG=$(record_application "nonlinearK4bsI.R" \
    --description="This needs supplying" \
) || exit -1

source lib.nonlinearK4bsI.R.requirements.software.sh
source lib.nonlinearK4bsI.R.requirements.hardware.sh
FOR=nonlinearK4bsI.R source lib.nonlinearK4bsI.R.input-types.sh
FOR=nonlinearK4bsI.R source lib.nonlinearK4bsI.R.output-types.sh
source lib.nonlinearK4bsI.R.argument-types.sh


# Metadata
# --------

record_contributor $PROG $gary_polhill_id Developer
record_contributor $PROG $gary_polhill_id Author

#record_implements $PROG \
#    --statistical_method="$sm_aic_id"
#record_implements $PROG \
#    --statistical_method="$sm_bic_id"
#record_implements $PROG \
#    --statistical_method="$sm_edf_id"
#record_implements $PROG \
#    --statistical_method="$sm_anova_gam_id"
#
#sos_nonlinearK4bsI_aic_id=(record_statistics "nonlinearK4bsI.R final_results.csv table4.csv" $sm_aic_id)
#sos_nonlinearK4bsI_bic_id=$(record_statistics "nonlinearK4bsI.R final_results.csv table4.csv" $sm_bic_id )
#sos_nonlinearK4bsI_edf_id=$(record_statistics "nonlinearK4bsI.R final_results.csv table4.csv" $sm_edf_id )
#sos_nonlinearK4bsI_anova_id=$(record_statistics "nonlinearK4bsI.R final_results.csv table4.csv" $sm_anova_gam_id )
