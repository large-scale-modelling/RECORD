RECORD_PROG=
OUTPUT=tail
if [ "$FOR" = "tail" ]
then
    RECORD_PROG=record_input_box_type
#    remainder="arg=1"
elif [ "$FOR" = "analysege_gpLU2.pl" ]
then
    RECORD_PROG=record_output_box_type
    PROG_BOX=$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1
    remainder="in_file=$PROG_BOX"
else
    (>&2 echo "BASH: $FUNCNAME ($@): 'FOR' is incorrect: $FOR, should be one of 
         tail or
         analysege_gpLU2.pl")
    exit -1
fi

eval io_batch_csv_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.result" \
    "^(batch1|batch2).csv$"\
    $remainder
) || exit -1


