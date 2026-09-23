FOR="nonlinearK4bsI.R"

a_final_results_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.result-file" \
    --description="Argument for results files with selected scenarios" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_table4_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.table4" \
    --description="Argument for raw table 4 in the paper" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range=path \
) || exit -1


