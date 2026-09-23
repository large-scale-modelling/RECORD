# Folksonomy
# ==========

source_tag=$(record_make_tag \
    "tag.source" \
    "This is a paper that is the source of the reproducibility." \
) || exit -1

mad_tag=$(record_make_tag \
    "tag.mad" \
    "Complete AWOL. About as useful as a chocolate teapot" \
) || exit -1

too_old_tag=$(record_make_tag \
    "tag.ancient" \
    "Past it." \
) || exit -1

frivilous_tag=$(record_make_tag \
    "tag.frivilous" \
    "Rather silly person." \
) || exit -1

urgent_tag=$(record_make_tag \
    "tag.urgent" \
    "Needs to be done yesterday." \
) || exit -1

awkward_syntax_tag=$(record_make_tag \
    "tag.awkward_syntax" \
    "The syntax in use in the script
	is still too awkward, and you have to be really in the zone to remember it, in 
	all its complexity. It is approaching some kind of language, but I am not sure 
	which kind." \
) || exit -1

too_slow_tag=$(record_make_tag \
    "tag.too_slow" \
    "This refers to the execution speed of a script or program." \
) || exit -1

objective_c_tag=$(record_make_tag \
    "tag.objective_c" \
    "Written in Objective C" \
) || exit -1

hacked_compiler_tag=$(record_make_tag \
    "tag.hacked_compiler" \
    "The compiler had to manually hacked" \
) || exit -1

dodgy_R_code_tag=$(record_make_tag \
    "tag.dodgy_R_code" \
    "Well dodgy code" \
) || exit -1

researcher_tag=$(record_make_tag \
    "tag.researcher_tag" \
    "A research scientist" \
) || exit -1

computer_research_engineer_tag=$(record_make_tag \
    "tag.computer_research_engineer" \
    "Somebody who falls in both camps, a developer and a scientist." \
) || exit -1

boss_tag=$(record_make_tag \
    "tag.boss" \
    "The boss person for this project." \
) || exit -1

old_fashioned_tag=$(record_make_tag \
    "tag.old_fashioned" \
    "Old fashioned way of doing stuff" \
) || exit -1

perl_code_tag=$(record_make_tag \
    "tag.perl_code" \
    "Some Perl - brilliant!" \
) || exit -1
    
r_code_tag=$(record_make_tag \
    "tag.r_code" \
    "Some R - boo!" \
) || exit -1
    
python_code_tag=$(record_make_tag \
    "tag.python_code" \
    "Some Python code - meh!" \
) || exit -1
# TODO need to cope with \' in these comments

awful_bash_code_tag=$(record_make_tag \
    "tag.awful_bash_code" \
    "I am not very happy with this Bash code" \
) || exit -1
    
figure_for_a_paper_id=$(record_make_tag \
    "tag.figure_for_paper" \
    "This produced by this figure is included in a paper" \
) || exit -1

figure_five_id=$(record_make_tag \
   "tag.figure5" \
   "Produces figure 5 for a paper" \
) || exit -1 

figure_four_id=$(record_make_tag \
    "tag.figure4" \
   "Produces figure 4 for a paper" \
) || exit -1 

appendix_id=$(record_make_tag \
    "tag.figure4" \
   "Produces an appendix for a paper" \
) || exit -1 


targetted_output_id=$(record_make_tag \
    "tag.targetted_output" \
    "This a target result that we required from this study." \
) || exit -1


# Tagging tags (or groups).

record_tag $frivilous_tag --other_tag=$mad_tag
record_tag $frivilous_tag --other_tag=$too_old_tag


