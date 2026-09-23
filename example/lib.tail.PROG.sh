PROG=$(record_application tail \
    --purpose="""
       tail - output the last part of files
""" \
) || exit -1

# No checking software/hardware requirements as this is an OS command

FOR=tail source lib.tail.input-types.sh
FOR=tail source lib.tail.output-types.sh
source lib.tail.argument-types.sh



