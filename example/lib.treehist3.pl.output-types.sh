OUTPUT=treehist3.pl
o_figure5_id=$(record_output_box_type \
    $PROG \
    "box_type.$OUTPUT.figure5" \
    '^.*.PDF$' \
    "arg=3" \
) || exit -1


