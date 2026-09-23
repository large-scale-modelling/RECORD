FOR="figure2-3small.R"

a_splits=$(record_argument_type \
    $PROG \
    "argument.$FOR.splits" \
    --description="I think this might be split the data" \
    --name="splits" \
    --type=flag \
) || exit -1

a_final_results=$(record_argument_type \
    $PROG \
    "argument.$FOR.final_results" \
    --description="Results files with selected scenarios" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_y_axis=$(record_argument_type \
    $PROG \
    "argument.$FOR.y_axis" \
    --description="y-axis label" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range='.*' \
) || exit -1

a_appendix=$(record_argument_type \
    $PROG \
    "argument.$FOR.appendix" \
    --description="The diagram for inclusion in the appendix" \
    --type=required \
    --order_value=3 \
    --arity=1 \
    --range='^.*pdf$' \
) || exit -1

a_scenarios=$(record_argument_type \
    $PROG \
    "argument.$FOR.scenarios" \
    --description="The Scenarios to include in the diagram" \
    --type=required \
    --order_value=4 \
    --arity=+ \
    --argsep='space' \
    --range='^A-ZA-Z?\/(V|F)\/[0-9][0-9]\/[0-9]$' \
) || exit -1


