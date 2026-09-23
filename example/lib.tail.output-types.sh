OUTPUT=tail
RECORD_PROG=
remainder=
if [ "$FOR" = "$OUTPUT" ]
then
    RECORD_PROG=record_output_box_type
    remainder=stdout
elif [ "$FOR" = "postprocessing.R" ]
then
    RECORD_PROG=record_input_box_type
    PROG_BOX=$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1
    remainder="in_file=$PROG_BOX"
else
    (>&2 echo "BASH: lib.tail.output-type.sh: 'FOR' is incorrect: $FOR, should be one of
         tail or
         postprocessing.R")
    exit -1
fi

eval io_all_results_id=$($RECORD_PROG  \
    $PROG \
    "box_type.$OUTPUT.all_results" \
    '^all_results.csv$' \
    $remainder \
) || exit -1

