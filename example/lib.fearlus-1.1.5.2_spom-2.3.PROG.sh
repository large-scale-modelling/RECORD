PROG=$(record_application "fearlus-1.1.5.2_spom-2.3" \
	--licence=GPLv3 \
	--version="1.1.5.2_spom-2.3" \
	--description="Framework for Evaluation and Assessment of Regional Land Use Scenarios (FEARLUS) = Stochastic Patch Occupancy Model (SPOM)" \
) || exit -1

record_contributor $PROG $gary_polhill_id Author

source lib.fearlus-1.1.5.2_spom-2.3.requirements.software.sh
source lib.fearlus-1.1.5.2_spom-2.3.requirements.hardware.sh
FOR=fearlus-1.1.5.2_spom-2.3 source lib.fearlus-1.1.5.2_spom-2.3.input-types.sh
source lib.fearlus-1.1.5.2_spom-2.3.output-types.sh
source lib.fearlus-1.1.5.2_spom-2.3.argument-types.sh

	
