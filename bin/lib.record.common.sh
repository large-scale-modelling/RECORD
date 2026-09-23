check_for_errors() {
    egrep --color -n -H "(: line|Trace|does not exist|No such file or directory)" "$1" | grep -v -i "pipeline" | grep -v -- --error
#    grep --color -n -H "(: line" "$1"
#    grep --color -n -H "line " "$1" | grep -v -i pipeline
#    grep --color -n -H -i "error" "$1" | grep -v -- --error
#    grep --color -n -H "Trace" "$1"
#    grep --color -n -H "does not exist" "$1"
#    grep --color -n -H "No such file or directory" "$1"
}

# Stolen shamelessly from here https://superuser.com/questions/363169/ps-how-can-i-recursively-get-all-child-process-for-a-given-pid

pidtree() (
    [ -n "$ZSH_VERSION"  ] && setopt shwordsplit
    declare -A CHILDS
    while read P PP;do
        CHILDS[$PP]+=" $P"
    done < <(ps -e -o pid= -o ppid=)

    walk() {
        echo $1
        for i in ${CHILDS[$1]};do
            walk $i
        done
    }

    for i in "$@";do
        walk $i
    done
)

get_stderr() {
    PID="$1"

    if [ -z "$PID" ] 
    then
        echo ""
        exit -1
    fi

    FD="/proc/$PID/fd/2"

    echo "$FD"
}

export RECORD_PID_FILE=/tmp/record.$USER.$RECORD_DBTYPE.$RECORD_START_PROGRAM.pid
if [ -z "$RECORD_START_PROGRAM" ]
then
    (>&2 echo $BASH_SOURCE": "$(date)": The environment variable RECORD_START_PROGRAM has not been set.")
    exit -1
elif ! which $RECORD_START_PROGRAM 2>&1 >/dev/null
then
    (>&2 echo $BASH_SOURCE": "$(date)": The environment variable RECORD_START_PROGRAM=$RECORD_START_PROGRAM is not executable.")
    exit -1
elif [ -f $RECORD_PID_FILE ]
then
    pid_of_record_run=$(head -1 $RECORD_PID_FILE)
    if [ -z "$pid_of_record_run" ]
    then
        (>&2 echo $BASH_SOURCE": "$(date)": The PID is not present in the PID file: $RECORD_PID_FILE.")
        exit -1
    elif ! [[ "$pid_of_record_run" =~ ^[0-9]+$ ]]
    then
        (>&2 echo $BASH_SOURCE": "$(date)": The PID is not in a correct format in the PID file: $RECORD_PID_FILE: $pid_of_record_run.")
        exit -1
    fi
fi


