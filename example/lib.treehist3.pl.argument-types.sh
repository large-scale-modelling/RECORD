FOR="treehist3.pl"

a_complexity_variable_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.complexity_variable" \
    --description="Complexity Parameter" \
    --name="cp" \
    --separator='-' \
    --assignment_operator="space" \
    --type=option \
    --arity=1 \
    --range='^(1|[0\.[0-9]+)$' \
) || exit -1

a_final_results_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.final_results" \
    --description="Results files with selected scenarios" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_figure5_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.figure5" \
    --description="PDF for figure 5" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range=path \
) || exit -1

a_response_variable_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.response_variable" \
    --description="Response variable" \
    --type=required \
    --order_value=3 \
    --arity=1 \
    --range='.*' \
) || exit -1

a_explanatory_variables_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.explanatory_variables" \
    --description="Explanatory variables
    Comma (no space) separated values" \
    --name=expiriment \
    --type=required \
    --order_value=4 \
    --range='^(..*)(\,..*)*$' \
) || exit -1


