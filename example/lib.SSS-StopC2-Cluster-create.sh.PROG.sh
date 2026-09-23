PROG=$(record_application SSS-StopC2-Cluster-create.sh \
    --purpose="

                Sets up the run for the lower value rewards
                and this is to test out multi-line,
                to see if it works. Which it does but removes the
                carriage returns and tabs. So you can nicely format it.

		         Add some documentary stuff here." \
    --version=1.0 \
    --licence=GPLv3 \
) || exit -1 

record_contributor $PROG $gary_polhill_id Author
record_contributor $PROG $doug_salt_id Author

source lib.SSS-StopC2-Cluster-create.sh.requirements.software.sh 
source lib.SSS-StopC2-Cluster-create.sh.requirements.hardware.sh 

