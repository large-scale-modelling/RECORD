# Requirements for this script 
# ============================

# Software

if ! record_require_exact $PROG os 'GNU/Linux' $(uname -o) 
then
    (>&2 echo "$0: Exact requirement for the OS failed")
    (>&2 echo "$0: Required GNU/Linux, Cygwin or  Darwin got "$(uname -o))
    exit -1
fi

if ! record_require_exact $PROG fearlus "fearlus-1.1.5.2_spom-2.3" \
	$($(which fearlus-1.1.5.2_spom-2.3) --version | tail -1 | awk '{print $1}')
then
        (>&2 echo "$0: Exact requirement for fearlus-spom binary failed")
        (>&2 echo "$0: Required fearlus-1.1.5.2_spom-2.3 got " \
		$($(which fearlus-1.1.5.2_spom-2.3) --version | tail -1 | awk '{print $1}'))
        exit -1
fi


