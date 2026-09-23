sos_from_recursive_partioning_id=$(record_statistics \
    "statistics.treehist3.pl.sos_from_recursive_partitioning" \
    $sm_recursive_partitioning_id \
    'treehist3.pl -cp 0.0075 final_results.csv LOBEC.rpart3Xfr.pdf Richness Government,Market,BET,ASP,Expenditure' \
) || exit -1


record_implements $PROG \
    --statistical_method="$sm_recursive_partitioning_id"

var_partitioning_complexity_id=$(record_variable  \
    "variable.treehist3.pl.partitioining_complexity" \
    "A measure of complexity " \
    Integer \
) || exit -1

record_value "0.0075" \
    $var_partitioning_complexity_id \
    LOBEC.rpart3Xfr.pdf \
    --statistical_parameter=$sos_from_recursive_partioning_id


sv_partitioning_complexity_id=$(record_statistical_variable \
    "statistical_variable.treehist3.pl.partitioning_complexity" \
    "A measure of complexity used as a threshold in a classification to prune nodes." \
    "\mathbb{R}" \
    "$sm_recursive_partitioning_id" \
) || exit -1


