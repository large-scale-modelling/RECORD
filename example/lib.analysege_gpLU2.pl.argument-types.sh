FOR="analysege_gpLU2.pl"

a_experiment=$(record_argument_type \
    $PROG \
    "argument.$FOR.experiment" \
    --description="The experimental run for this model. In the range 1-9." \
    --type=required \
    --order_value=1 \
    --arity=1 \
    --range='^[0-9]$' \
) || exit -1


