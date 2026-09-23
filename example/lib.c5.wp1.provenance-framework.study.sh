source lib.c5.wp1.study.sh

c5_wp1_provenance_framework_study_id=$(record_study \
    study_c5_wp1_provenance_framework_study \
    $c5_wp1_study_id \
	--project=$project_id \
	--start_time="2022-04-01" \
	--end_time="2027-03-31" \
    --description="Taking the work of miracle and generalising it for any kind
of modelling. That is to provide an easily implementable, reusable provenance
and metadata recording framework." \
	--title="RESAS - C5 - WP1 - Provenance framework " \
) || exit -1

record_involvement \
    $c5_wp1_provenance_framework_study_id \
    $gary_polhill_id \
	"Lead investigator"

record_involvement \
    $c5_wp1_provenance_framework_study_id \
    $doug_salt_id \
	"Developer"


