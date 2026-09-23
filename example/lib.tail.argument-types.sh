FOR="tail"

a_batch_csv_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.batch_csv" \
    --description="One of the two outputs from analysege_gpLU2.pl" \
    --type=required \
    --arity=1 \
    --order_value=1 \
    --range=path \
) || exit -1

a_lines_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.nof_lines" \
    --description="The number of lines to omit from the file at the start" \
    --type=option \
    --name=n \
    --separator="-" \
    --assignment_operator="space" \
    --range='^(\+|-)?[0-9]+$' \
) || exit -1
