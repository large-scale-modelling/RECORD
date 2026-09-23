PROG=$(record_application SSS-StopC2-Cluster-run2.sh \
    --purpose="Does the runs for the higher value rewards" \
    --version=1.0 \
    --licence=GPLv3 \
) || exit -1 

record_contributor $PROG $gary_polhill_id Author
record_contributor $PROG $doug_salt_id Author

source lib.SSS-StopC2-Cluster-run2.sh.requirements.software.sh 
source lib.SSS-StopC2-Cluster-run2.sh.requirements.hardware.sh 

