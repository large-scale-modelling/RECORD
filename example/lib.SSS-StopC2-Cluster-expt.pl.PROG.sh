# Program being called
# ====================

# This could probably be done within a Perl program itself, for the purposes of
# this instance of generating metadata, I have done everything in the shell
# scripts.

PROG=$(record_application "SSS-StopC2-Cluster-expt.pl" \
    --purpose="Perl script to create the SSS preliminary experiments. These are designed to cover sinks/nosinks and RewardActivity/RewardSpecies, at various BETs and ASPs, and for flat and var2 market." \
    --version=1.0 \
    --licence=GPLv3 \
) || exit -1 

source lib.SSS-StopC2-Cluster-expt.pl.requirements.hardware.sh
source lib.SSS-StopC2-Cluster-expt.pl.requirements.software.sh
source lib.SSS-StopC2-Cluster-expt.pl.argument-types.sh
FOR=SSS-StopC2-Cluster-expt.pl source lib.SSS-StopC2-Cluster-expt.pl.output-types.sh

# Metadata
# ========

record_contributor $PROG $gary_polhill_id Author

# Assumptions
# ===========

first_governance_assumption=$(record_person_makes_assumption \
    $gary_polhill_id \
    assumption.SSS-StopC2-Cluster-expt.pl.governance \
    "The assumption for this run of the script is that the reward 
    governance has more of an effect than clustering in changing behaviour
     of land-owners." \
) || exit -1 

second_governance_assumption=$(record_person_makes_assumption \
    $gary_polhill_id \
    assumption.SSS-StopC2-Cluster-expt.pl.prerun \
    "One of the main themes of the Global Land Project concerns understanding the effects of
    human land use activities in altering the structure and functioning of terrestrial landscapes
    and ecosystems. Improved knowledge of the decision-making processes related to land use
    and land use management provides the foundation for evaluating the interactions among
    factors influencing human activities and feedbacks within the coupled human–environment
    system. Modelling can contribute to a better understanding of such systems, and it is now
    generally accepted that to adequately capture the complex dynamics of landscapes, it is
    often necessary for models thereof to include a simulation of the human social processes
    embedded within them." \
) || exit -1

bugless_assumption=$(record_person_makes_assumption \
    $doug_salt_id \
    assumption.SSS-StopC2-Cluster-expt.pl.bug-free \
    "This code is bug free." \
) || exit -1

# TODO check out whether you can link assumptions elsewhere.


