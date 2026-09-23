OUTPUT="nonlinearK4bsI.R"
RECORD_PROG=
remainder=
if [ "$FOR" = "$OUTPUT" ]
then
    RECORD_PROG=record_output_box_type
    remainder="arg=2"
elif [ "$FOR" = "table4.R" ]
then
    RECORD_PROG=record_input_box_type
    remainder="arg=1"
else
    (>&2 echo "BASH: lib.nonlinearK4bsI.sh: 'FOR' is incorrect: $FOR, should be one of
         nonlinearK4bsI.R or
         table4.R")
    exit -1
fi

eval io_table4_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.table4.csv" \
    '^table4.csv$' \
    $remainder \
) || exit -1


