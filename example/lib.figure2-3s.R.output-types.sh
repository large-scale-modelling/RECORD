OUTPUT="figure2-3s.R"
o_figure4_id=$(record_output_box_type \
    $PROG \
    "box_type.$OUTPUT.figure4.pdf" \
    '^figure4.*\.pdf$' \
    "arg=4" \
) || exit -1


