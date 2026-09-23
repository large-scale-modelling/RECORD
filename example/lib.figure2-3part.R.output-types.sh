OUTPUT=figure2-3part.R
o_figure3_id=$(record_output_box_type \
    $PROG \
    "box_type.$OUTPUT.pdf" \
    '^figure3.pdf$' \
    "arg=3" \
) || exit -1


