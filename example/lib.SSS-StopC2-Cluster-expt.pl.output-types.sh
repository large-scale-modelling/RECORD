RECORD_PROG=
OUTPUT="SSS-StopC2-Cluster-expt.pl"
if [ "$FOR" = "$OUTPUT" ]
then
    RECORD_PROG="record_output_box_type"
elif [ "$FOR" = "fearlus-1.1.5.2_spom-2.3" ]
then
    RECORD_PROG="record_input_box_type"
else
    (>&2 echo "BASH: lib.postprocesing.R.output-types.sh: 'FOR' is incorrect: $FOR, should be one of
            SSS-StopC2-cluster-expt.pl or
            fearlus-1.1.5.2_spom-2.3")
    exit -1
fi
PROG_BOX=$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1

eval io_SSS_economystate_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.SSS_economystate" \
    "______[^_]+_____.state" \
    "in_file=$PROG_BOX" 
) || exit -1

eval io_SSS_top_level_subpop_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.SSS_top-level-subpop" \
    "________[^_]+_[^_]+_[^_]+_.ssp" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_grid_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.SSS_grid" \
    "___________[^_]+.grd" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_top_level_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.SSS_top-level" \
    "_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+.model" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_species_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_species" \
    "_[^_]+__________.csv" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_subpop_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_subpop" \
    "________[^_]+_[^_]+_[^_]+_.sp" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_yieldtree_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_yieldtree" \
    "___________.tree)" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_fearlus_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_fearlus" \
    "__[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+.fearlus" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_government_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_government" \
    "__[^_]+_[^_]+_[^_]+_[^_]+______.gov" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_sink_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_sink" \
    "_[^_]+__________.csv" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_incometree_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_incometree" \
    "______[^_]+_____.tree" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_luhab_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_luhab" \
    "___________.csv" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_climateprob_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_climateprob" \
    "___________.prob" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_patch_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_patch" \
    "_[^_]+__________[^_]+.csv" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_report_config_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_report-config" \
    "_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+.repcfg" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_yielddata_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_yielddata" \
    "___________.data" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_spom_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_spom" \
    "_[^_]+__________[^_]+.spom" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_economyprob_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_economyprob" \
    "___________.prob" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_dummy_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_dummy" \
    "___________[^_]+.csv" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_incomedata_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_incomedata" \
    "______[^_]+_____.data" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_event_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_event" \
    "________[^_]+___.event" \
    "in_file=$PROG_BOX" \
) || exit -1

eval io_SSS_trigger_id=$($RECORD_PROG $PROG \
    "box_type.$OUTPUT.SSS_trigger" \
    "________[^_]+___.trig" \
    "in_file=$PROG_BOX" \
) || exit -1


