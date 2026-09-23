OUTPUT=table4.R
o_table4_paper_id=$(record_output_box_type \
    $PROG \
    "box_type.$OUTPUT.table4" \
    '^table4.csv$' \
    "arg=2" \
) || exit -1


