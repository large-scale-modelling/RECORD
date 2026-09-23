PROG=$(record_application postprocessing.sh \
	--purpose="Post processing to almagamate results and produce pretty diagrams" \
    --version=1.0 \
    --licence=GPLv3 \
) || exit -1

[ -n $PROG ] || exit -1 

record_contributor $PROG $gary_polhill_id Author
record_contributor $PROG $doug_salt_id Author

source lib.postprocessing.sh.requirements.software.sh 
source lib.postprocessing.sh.requirements.hardware.sh 

