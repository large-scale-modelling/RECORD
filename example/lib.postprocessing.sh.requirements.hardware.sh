# This has an immediate ancestor condition, because this may be used in two
# places. In this case this may be called at the head of postprocessing.sh, if
# postprocessing.sh is being run ad-hoc, OR it is being called from
# workflow.sh, in which case workflow.sh is running it. So if there is no
# ancestor this needs to run, if there is an ancestor it has already run.

IS_CALLED_BY=$(record_called_by) || exit -1

if [ -z "$IS_CALLED_BY" ]
then
    if ! record_require_minimum $PROG disk_space 20G $(disk_space)
    then
        (>&2 echo "$0: Minimum requirement for disk space failed")
        (>&2 echo "$0: Required 20G of disk space got "$(disk_space))
        exit -1
    fi

    if ! record_require_minimum $PROG memory 4G $(memory)
    then
        (>&2 echo "$0: Minimum requirement for memory failed")
        (>&2 echo "$0: Required 4G of memory got $(memory)")
        exit -1
    fi

    if ! record_require_minimum $PROG cpus $RECORD_REQUIRED_NOF_CPUS $(cpus) 
    then
        (>&2 echo "$0: Minimum requirement for number of cpus failed")
        (>&2 echo "$0: Required $RECORD_REQUIRED_NOF_CPUS cpus of memory got $(cpus)")
        exit -1
    fi
fi


    
