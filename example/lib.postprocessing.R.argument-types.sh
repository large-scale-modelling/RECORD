FOR="postprocessing.R"

a_all_results=$(record_argument_type \
    $PROG \
    "argument.$FOR.result" \
    --description="All the results from all the runs" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1


a_scenarios=$(record_argument_type \
    $PROG \
    "argument.$FOR.scenarios" \
    --description="The scenarios that are required for processing" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range=path \
) || exit -1

a_final_results=$(record_argument_type \
    $PROG \
    "argument.$FOR.experiment" \
    --description="The actual results from which diagrams will be created." \
    --type=required \
    --order_value=3 \
    --arity=1 \
    --range=path \
) || exit -1


