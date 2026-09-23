FOR="figure2-3s.R"

a_splits=$(record_argument_type \
    $PROG \
    "argument.$FOR.splits" \
    --description="I think this might be to split the data" \
    --name="splits" \
    --type=flag \
) || exit -1

a_final_results=$(record_argument_type \
    $PROG \
    "argument.$FOR.final_results" \
    --description="Result files with selected scenarios" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_main_scenario=$(record_argument_type \
    $PROG \
    "argument.$FOR.main_scenario" \
    --description="Main scenario" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range='^.*$' \
) || exit -1

a_small_scenarios=$(record_argument_type \
    $PROG \
    "argument.$FOR.small_scenarios" \
    --description="Small scenarios" \
    --type=required \
    --order_value=3 \
    --arity=5 \
    --argsep='space' \
    --range='^A-ZA-Z?\/(V|F)\/[0-9][0-9]\/[0-9]$' \
) || exit -1

a_figure4=$(record_argument_type \
    $PROG \
    "argument.$FOR.figure5" \
    --description="PDF for figure 4" \
    --type=required \
    --order_value=4 \
    --arity=1 \
    --range=path \
) || exit -1


