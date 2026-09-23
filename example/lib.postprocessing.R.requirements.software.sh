IS_CALLED_BY=$(record_called_by) || exit -1

if [ -z "$IS_CALLED_BY" ]
then

    if ! record_require_minimum $PROG "R" "3.3.1" $(R --version | head -1 | awk '{print $3}')
    then
        (>&2 echo "$0: Minimum requirement for R failed")
        (>&2 echo "$0: Required 3.3.1 got " \
            $(R --version | head -1 | awk '{print $3}'))
        exit -1
    fi
fi



