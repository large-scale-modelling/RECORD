FOR="fearlus-1.1.5.2_spom-2.3" source lib.analysege_gpLU2.pl.input-types.sh
OUTPUT="fearlus-1.1.5.2_spom-2.3"

o_SSS_OUT_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.OUT" \
	"[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_].out" \
    in_file=$PROG_BOX \
) || exit -1

o_SSS_ERR_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.ERR" \
	"[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_].err" \
    in_file=$PROG_BOX \
) || exit -1

# SSS_spomresult_nosink_ClusterActivity_all_1.0_1.0_var2_25.0_noapproval_0.0_1.0_001-prop.csv
o_SSS_spomresult_prop_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.SSS_spomresult" \
	"SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-prop.csv" \
    in_file=$PROG_BOX \
) || exit -1

# o_SSS_spomresult_nosink_ClusterActivity_all_1.0_1.0_var2_25.0_noapproval_0.0_1.0_001-pspp.csv
o_SSS_spomresult_pspp_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.SSS_spomresult_pspp" \
	"SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-pspp.csv" \
    in_file=$PROG_BOX \
) || exit -1

# o_SSS_spomresult_nosink_ClusterActivity_all_1.0_1.0_var2_25.0_noapproval_0.0_1.0_001-nspp.csv
o_SSS_spomresult_nspp_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.SSS_spomresult_pspp" \
	"SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-pspp.csv" \
    in_file=$PROG_BOX \
) || exit -1

# o_SSS_spomresult_nosink_ClusterActivity_all_1.0_1.0_var2_25.0_noapproval_0.0_1.0_001-habgrid.csv
o_SSS_spomresult_habgrid_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.SSS_spomresult_habgrid" \
	"SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-habgrid.csv" \
    in_file=$PROG_BOX \
) || exit -1

# o_SSS_spomresult_nosink_ClusterActivity_all_1.0_1.0_var2_25.0_noapproval_0.0_1.0_001-area.csv
o_SSS_spomresult_area_id=$(record_output_box_type \
    $PROG \
	"box_type.$OUTPUT.SSS_spomresult_area" \
	"SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-area.csv" \
    in_file=$PROG_BOX \
) || exit -1

	

