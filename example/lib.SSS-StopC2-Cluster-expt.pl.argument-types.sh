FOR="SSS-StopC2-Cluster-expt.pl"

a_govt_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.govt" \
    --description="Type of governance" \
    --type=required \
    --name=govt \
    --order_value=1 \
    --arity=1 \
    --range='^(ClusterActivity|ClusterSpecies|RewardActivity|RewardSpecies)$' \
) || exit -1

a_sink_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.sink" \
    --description="Type of governance" \
    --name=sink \
    --type=required \
    --order_value=2 \
    --arity=1 \
    --range='^(YES|NO)$' \
) || exit -1

a_market_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.market" \
    --description="Market" \
    --name=market \
    --type=required \
    --order_value=3 \
    --arity=1 \
    --range='^(flat|var1|var2)$' \
) || exit -1

a_zone_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.zone" \
    --description="Policy zone" \
    --name=zone \
    --type=required \
    --order_value=4 \
    --arity=1 \
    --range='^(all|random|rect)$' \
) || exit -1

a_reward_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.reward" \
    --description="Reward budget" \
    --name=reward \
    --type=required \
    --order_value=5 \
    --arity=1 \
    --range='[0-9]+(\.[0-9]+)?$' \
) || exit -1

a_ratio_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.ratio" \
    --description="Cluster reward ratio" \
    --name=ratio \
    --type=required \
    --order_value=6 \
    --arity=1 \
    --range='^[0-9]+(\.[0-9]+)?$' \
) || exit -1

a_bet_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.bet" \
    --description="Break-even threshold" \
    --name=bet \
    --type=required \
    --order_value=7 \
    --arity=1 \
    --range='^[0-9]+(\.[0-9]+)?$' \
) || exit -1

a_approval_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.approval" \
    --description="Approval" \
    --name=approval \
    --type=required \
    --order_value=8 \
    --arity=1 \
    --range='^(YES|NO)$' \
) || exit -1

a_iwealth_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.iwealth" \
    --description="Initial wealth" \
    --name=iwealth \
    --type=required \
    --order_value=9 \
    --arity=1 \
    --range='^[0-9]+(\.[0-9]+)?$' \
) || exit -1

a_aspiration_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.aspiration" \
    --description="Aspriation threshold" \
    --name=aspiration \
    --type=required \
    --order_value=10 \
    --arity=1 \
    --range='^[0-9]+(\.[0-9]+)?$' \
) || exit -1

a_run_id=$(record_argument_type \
    $PROG \
    "argument.$FOR.run" \
    --description="Run number" \
    --name=run \
    --type=required \
    --order_value=11 \
    --arity=1 \
    --range='^\d+$' \
) || exit -1


