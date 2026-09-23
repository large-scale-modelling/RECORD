if ! record_require_minimum $PROG perl  "5.0" $(perl -e 'print $];')
then
    (>&2 echo "$0: Minimum requirement for Perl failed")
    (>&2 echo "$0: Required at least Perl 5.0, got "$(perl -e 'print $];'))
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


