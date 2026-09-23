FOR=figure2-3part.R source lib.postprocessing.R.output-types.sh

INPUT="figure2-3part.R"
i_figure3_cfg_id=$(record_input_box_type \
    $PROG \
    "box_type.$INPUT.figure3_cfg" \
    '^cfg\/figure3\.cfg$'\
    "arg=2" \
) || exit -1

