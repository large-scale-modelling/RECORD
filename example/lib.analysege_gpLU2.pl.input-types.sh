record_prog=
if [ "$FOR"="analysege_gpLU2.pl" ]
then
    record_prog="record_input_box_type"
elif [ "$FOR"="fearlus-1.1.5.2_spom-2.3" ]
then
    record_prog="record_output_box_type"
else
    (>&2 echo "BASH: lib.postprocesing.R.output-types.sh: 'FOR' is incorrect: $FOR, should be one of
            fearlus-1.1.5.2_spom-2.3 or
            analysege_gpLU2.pl")
     exit -1
fi
PROG_BOX=$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1

eval io_SSS_report_id=$($record_prog \
    $PROG \
    box_type.SSS_report \
    "SSS_report_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_].txt" \
    in_file=$PROG_BOX \
) || exit -1

eval io_SSS_report_grd_id=$($record_prog \
    $PROG \
    box_type.SSS_report_grd \
    "SSS_report_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_].grd" \
    in_file=$PROG_BOX \
) || exit -1

eval io_SSS_spomresult_extinct_id=$($record_prog \
    $PROG \
    box_type.SSS_spomresult_extinct \
    "SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-extinct.csv" \
    in_file=$PROG_BOX \
) || exit -1

eval io_SSS_spomresult_lspp_id=$($record_prog \
    $PROG \
    box_type.SSS_spomresult_lspp \
    "SSS_spomresult_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]+_[^_]-lspp.csv" \
    in_file=$PROG_BOX \
) || exit -1


