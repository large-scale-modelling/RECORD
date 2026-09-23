OUTPUT="figure2-3small.R"
o_appendix_id=$(record_output_box_type \
    $PROG \
    "box_type.$OUTPUT.appendix.pdf" \
    '^appendix.pdf$' \
    arg=3 \
) || exit -1



