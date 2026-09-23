source lib.c5.study.sh

c5_wp1_study_id=$(record_study \
    study_c5_wp1_study \
    $c5_study_id \
	--project=$project_id \
	--start_time="2023-03-31" \
	--description=" The objective is to co-construct guidance for
integrative and reproducible modelling and to prototype and iteratively co-develop
digital infrastructure to provide a digital environment for policy-led large-scale
modelling of Scotland’s rural human-environmental system based on international
best practices and innovative uses of existing and novel data sources by January
2027. The guidance and digital prototypes will be co-developed through three linked
3
activities: (1) reviewing and reflecting on previous and current projects and best
practices; (2) using IT infrastructure to build a prototype digital environment for
integrative and reproducible modelling, demonstrating its value through three case
studies in other WPs; and (3) evaluating the guidance and digital environment
prototype and the modelling services it provides. We will prepare databases on
model integration and reproducibility technologies, relevant models and data
sources; and open source digital prototypes that demonstrate the application of the
integration and reproducibility modelling environment to support policy needs." \
    --title="WP1 – Digital Environment (RQ8)a" \
) || exit -1

record_involvement \
    $c5_wp1_study_id \
    $gary_polhill_id \
	"Lead investigator"

record_involvement \
    $c5_wp1_study_id \
    $gary_polhill_id \
	"Reviewer"

record_involvement \
    $c5_wp1_study_id \
    $doug_salt_id \
	"Developer"

record_involvement \
    $c5_wp1_study_id \
    $doug_salt_id \
	"Work package leader of WP1"

record_tag $mad_tag --person=$doug_salt_id
record_tag $too_old_tag --person=$doug_salt_id

record_involvement \
    $c5_wp1_study_id \
    $becky_smith_id \
	"Developer"



