FOR="figure2-3part.R"

a_final_results_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.final_results" \
    --description="Argument for the results files with all scenarios" \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range=path \
) || exit -1

a_figure3_cfg_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.figure3_cfg" \
    --description="Argument for the configuration to pick correct scenarios for figure 3" \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range=path \
) || exit -1

a_figure3_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.figure3" \
    --description="Argument for the output Figure 3 pdf for the paper containing six graphs" \
    --type=required \
    --order_value=3 \
    --arity=1 \
    --range=path \
) || exit -1


