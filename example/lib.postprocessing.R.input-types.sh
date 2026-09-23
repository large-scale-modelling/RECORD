FOR=postprocessing.R source lib.tail.output-types.sh

PROG_BOX=$(record-get-value.py --table=Application --id_application=$PROG --location) || exit -1
INPUT="postprocessing.R"
i_scenarios_id=$(record_input_box_type \
    $PROG \
    "box_type.$INPUT.scenarios" \
    '^cfg/scenarios.cfg$' \
    in_file=$PROG_BOX \
) || exit -1


