FOR="table4.R"

a_table4_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.table4.csv" \
    --description="Results files with selected scenarios from previous code." \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_table4_paper_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.table4.paper" \
    --description="Results for table 4 appearing in the paper" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range=path \
) || exit -1


