if ! record_require_minimum $PROG bash 4 $(bash --version | sed -n 1p | awk '{print $4}' | cut -f1 -d.)
then
    (>&2 echo "$0: Minimum requirement for bash failed")
    (>&2 echo "$0: Required 3 got " \
    $(bash --version | sed -n 1p | awk '{print $4}' | cut -f1 -d.))
    exit -1
fi

if record_require_exact $PROG os 'GNU/Linux' $(uname -o) 
then
    :
elif record_require_exact $PROG os Darwin $(uname -o) 
then
    :
elif record_require_exact $PROG os Cygwin $(uname -o) 
then
    :
else
    (>&2 echo "$0: Exact requirement for the OS failed")
    (>&2 echo "$0: Required GNU/Linux, Cygwin or  Darwin got "$(uname -o))
    exit -1
fi


