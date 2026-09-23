RECORD_PROG=
OUTPUT=postprocessing.R
remainder=
if [ "$FOR" = "$OUTPUT" ]
then
    RECORD_PROG=record_output_box_type
    remainder="arg=3"
elif [ "$FOR" =  "figure2-3part.R" ] || \
     [ "$FOR" =  "nonlinearK4bsI.R" ] || \
     [ "$FOR" =  "figure2-3s.R" ] || \
     [ "$FOR" =  "treehist3.pl" ] 
then
    RECORD_PROG=record_input_box_type
    remainder="arg=1"
elif [ "$FOR" =  "figure2-3small.R" ] || \
     [ "$FOR" =  "table4.R" ] 
then
    RECORD_PROG=record_input_box_type
    remainder="in_file="$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1
else
    (>&2 echo "BASH: lib.postprocesing.R.output-types.sh: 'FOR' is incorrect: $FOR, should be one of
            postprocessing.R
            figure2-3part.R;
            figure2-3small.R;
            figure2-3s.R;
            nonlinearK4bsI.R;
            table4.R or
            treehist3.pl")
    exit -1
fi
eval io_final_results_id=$($RECORD_PROG \
    $PROG \
    "box_type.$OUTPUT.final_results.csv" \
    '^final_results.csv$' \
    $remainder \
) || exit -1



