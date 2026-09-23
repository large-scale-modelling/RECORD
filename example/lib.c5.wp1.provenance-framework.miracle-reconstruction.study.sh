source lib.c5.wp1.provenance-framework.study.sh

c5_wp1_provenance_framework_miracle_reconstruction_study_id=$(record_study \
    study_c5_wp1_provenance_framework_study \
    $c5_wp1_provenance_framework_study_id \
	--project=$project_id \
	--start_time="2022-04-01" \
	--end_time="2027-03-31" \
	--description="This is a run to reconstruct the diagrams 
			and results in Polhill et al. 2013.

			Originally we were going to use Python scripts to
			do the job control for us, but I have decided to remain
			with shell scripts, to try and preserve the original
			flavour. But these might be too slow." \
	--title="MIRACLE rerun on Polhill 2011" \
) || exit -1

record_involvement \
    $c5_wp1_provenance_framework_miracle_reconstruction_study_id \
    $lorenzo_milazzo_id \
	"Original author of the metadata gathering program"

record_involvement \
    $c5_wp1_provenance_framework_miracle_reconstruction_study_id \
    $gary_polhill_id \
	"Original author"

record_involvement \
    $c5_wp1_provenance_framework_miracle_reconstruction_study_id \
    $doug_salt_id \
	"Implementor of the metadata gathering framework

	and creator of enormously 
    
    and very, very,
    
    annoying,
    
    long comments."

paper_id=$(record_paper \
	'example/Reconstructing the diagrams and results in Polhill et al.docx' \
	$doug_salt_id \
	$gary_polhill_id \
    $c5_wp1_provenance_framework_miracle_reconstruction_study_id \
	20170414 \
) || exit -1

record_contributor "$paper_id" $gary_polhill_id Author

record_tag $source_tag --documentation="$paper_id"

# Assumptions
# ===========

garys_assumption=$(record_person_makes_assumption \
    $gary_polhill_id \
    assumption.dangerous \
    'Doug knows what he is doing. This is an example
of an assumption, which you might want to fill in....
...and could conceivably go over several lines.' \
) || exit -1 

dougs_1st_assumption=$(record_person_makes_assumption \
    $doug_salt_id \
    assumption.insane \
    "There are no bugs in this software." \
) || exit -1

dougs_2nd_assumption=$(record_person_makes_assumption \
    $doug_salt_id \
    assumption.likely \
    "There are bugs in this software." \
) || exit -1


# TODO Need to add in a load more documentation in terms of paper
