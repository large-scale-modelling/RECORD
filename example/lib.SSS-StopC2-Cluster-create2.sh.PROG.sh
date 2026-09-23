PROG=$(record_application SSS-StopC2-Cluster-create2.sh \
    --purpose="""
    This is the script to actually run the SSS experiments.
    This was the second run with the higher values.
""" \
    --version=1.0 \
    --licence=GPLv3 \
) || exit -1 

record_contributor $PROG $gary_polhill_id Author
record_contributor $PROG $doug_salt_id Author

source lib.SSS-StopC2-Cluster-create2.sh.requirements.software.sh 
source lib.SSS-StopC2-Cluster-create2.sh.requirements.hardware.sh 

