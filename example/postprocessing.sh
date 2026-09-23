#!/usr/bin/env bash

# This is the workflow script used tie all the results together in the post
# processing for this experiment.

# Author: Doug Salt

# Date: Jan 2017

# So if any script or part of the script returns non-zero then the script will
# fail
# set -e

. lib/record.sh

# b_ for box
# a_ for argument
# io_ for an input/output - input for one prog, output for another
# o_ for a _pure_ output
# i_ for a _pure_ input
# PROG is always the application

# I have not done this in the other scripts, but I recommend in the case of
# complicated script some kind of convention is adopted purely for your own
# sanity.

# I find the metadata very, very confusing, so to mitigate this I have adopted
# the following conventions for prefices:

# sm_ is a statistical method
# vm_ is a visualisation method
# sos_ is a set of statistics
# var_ is a variable
# con_ is content (????)
# vis_ is a visualisation
# sv_ is a statistical_variable
# par_ is a parameter

# Seemingly the difference between a parameter is that it is fixed.
# and a parameter may change

# sv_ is used by a sm_

# vis_ has a vm_ and points to the visualisation box, a_
# con_ can have a  vm_, sm_, 
# An a_ can implement a vm_ or sm_

# Remembering the setting values does not return anything and can set an

# sv_
# sp_
# vp_

record_start

# Identity
# ========

source lib.postprocessing.sh.PROG.sh

ass_id=$(record_person_makes_assumption  \
    $doug_salt_id \
    "assumption.postprocesing.sh.complete" \
    "Everything else has been run" \
) || exit -1

another_ass_id=$(record_person_makes_assumption \
    $doug_salt_id \
    "assumption.postprocesing.sh.not_production" \
    "This is not a production environment 

otherwise this will not work and you will have to copy files from somewhere to
fool the process." \
) || exit -1


source lib.postprocessing.sh.requirements.software.sh
source lib.postprocessing.sh.requirements.hardware.sh
#source lib.postprocessing.sh.finegrain.sh


# Now run the all important scripts...

# analysege_gpLU2.pl
# ==================

source lib.analysege_gpLU2.pl.PROG.sh

# So these are taken from he actual harvesting programming analysege_gpLU2.pl



governments=("ClusterActivity" "ClusterSpecies" "RewardActivity" "RewardSpecies" )
rewards=( "1.0" "2.0" "3.0" "4.0" "5.0" "6.0" "7.0" "8.0" "9.0" "10.0" )
ratios=( "1.0" "2.0" "10.0" )
sinks=( "nosink" );
asps=( "1.0" "5.0" )

rm batch1.csv 2>/dev/null

parameters=/tmp/$$.$USER.$(basename $0).analysege_gpLU2.pl.parameters

echo """--record-argument-$a_experiment=8
--record-stdout-${io_batch_csv_id}=batch1.csv""" > "$parameters"

# The first three are hardcoded in to analysege_gpLU3.pl

for run in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020
do  
    for market in flat var2
    do
        for bet in 25.0 30.0
        do
            for govt in "${governments[@]}"
            do
                for rwd in "${rewards[@]}"
                do
                    for asp in "${asps[@]}"
                    do
                        for sink in "${sinks[@]}"
                        do
                            for rat in "${ratios[@]}"
                            do
                                
                                DIR="Cluster2/SSS_dir_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_"
                                IN_1="SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.txt"
                                IN_2="SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.grd"
                                IN_3="SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-extinct.csv"
                                IN_4="SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-lspp.csv"

                                echo "--record-input-${io_SSS_report_id}=$DIR/$IN_1" >> "$parameters"
                                echo "--record-input-${io_SSS_report_grd_id}=$DIR/$IN_2" >> "$parameters"
                                echo "--record-input-${io_SSS_spomresult_extinct_id}=$DIR/$IN_3" >> "$parameters"
                                echo "--record-input-${io_SSS_spomresult_lspp_id}=$DIR/$IN_4" >> "$parameters"

                            done
                        done
                    done
                done
            done
        done
    done
done

ARGS=$(cat "$parameters")
record_batch "$PROG" "$ARGS"

record_block

rm batch2.csv 2>/dev/null
 
governments=("RewardActivity" "RewardSpecies" )
rewards=("15.0" "20.0" "25.0" "30.0" "40.0" "50.0" "100.0")
ratios=( "1.0" )
sinks=( "nosink" );
asps=( "1.0" "5.0" )


echo """--record-argument-$a_experiment=9
--record-stdout-${io_batch_csv_id}=batch2.csv""" > "$parameters"

# The first three are hardcoded in to analysege_gpLU3.pl

for run in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020
do  
    for market in flat var2
    do
        for bet in 25.0 30.0
        do
            for govt in "${governments[@]}"
            do
                for rwd in "${rewards[@]}"
                do
                    for asp in "${asps[@]}"
                    do
                        for sink in "${sinks[@]}"
                        do
                            for rat in "${ratios[@]}"
                            do
                                
                                DIR="Cluster2-2/SSS_dir_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_"
                                IN_1="SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.txt"
                                IN_2="SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.grd"
                                IN_3="SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-extinct.csv"
                                IN_4="SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-lspp.csv"

                                echo "--record-input-${io_SSS_report_id}=$DIR/$IN_1" >> "$parameters"
                                echo "--record-input-${io_SSS_report_grd_id}=$DIR/$IN_2" >> "$parameters"
                                echo "--record-input-${io_SSS_spomresult_extinct_id}=$DIR/$IN_3" >> "$parameters"
                                echo "--record-input-${io_SSS_spomresult_lspp_id}=$DIR/$IN_4" >> "$parameters"

                            done
                        done
                    done
                done
            done
        done
    done
done

ARGS=$(cat "$parameters")
record_batch "$PROG" "$ARGS"

record_block

#rm "$parameters"

#source lib.postprocessing.sh.statistics.sh

# Merge
# =====

rm all_results.csv 2>/dev/null

source lib.tail.PROG.sh

# Was:

#tail -n +2 batch1.csv > all_results.csv
#tail -n +3 batch2.csv >> all_results.csv


record_run $PROG \
   --record-input-${io_batch_csv_id}=batch1.csv \
   --record-extend-stdout-${io_all_results_id}=all_results.csv \
   --record-argument-${a_batch_csv_id}=batch1.csv \
   --record-argument-${a_lines_id}=+2 


record_run $PROG \
   --record-input-${io_batch_csv_id}=$file \
   --record-extend-stdout-${io_all_results_id}=all_results.csv \
   --record-argument-${a_batch_csv_id}=batch2.csv \
   --record-argument-${a_lines_id}=+3 


# postprocessing.R
# ================

# postprocessing.R \
#    all_results.csv \
#    example/scenarios.csv \
#    final_results.csv

source lib.postprocessing.R.PROG.sh
rm final_results.csv 2>/dev/null

record_run $PROG  \
    --record-input-${io_all_results_id}=all_results.csv \
    --record-input-${i_scenarios_id}=example/scenarios.cfg \
    --record-argument-${a_all_results}=all_results.csv \
    --record-argument-${a_scenarios}=example/scenarios.cfg \
    --record-argument-${a_final_results}=final_results.csv \
    --record-output-${io_final_results_id}=final_results.csv

record_block

# Figure 3
# ========

# figure2-3part.R \
#    final_results.csv \
#    example/figure3.cfg \
#    figure3.pdf

source lib.figure2-3part.R.PROG.sh

record_batch $PROG \
    --record-argument-${a_final_results_id}=final_results.csv \
    --record-argument-${a_figure3_cfg_id}=example/figure3.cfg \
    --record-argument-${a_figure3_id}=figure3.pdf \
    --record-input-${io_final_results_id}=final_results.csv \
    --record-input-${i_figure3_cfg_id}=example/figure3.cfg \
    --record-output-${o_figure3_id}=figure3.pdf
   
record_block

# ========================
# table 4 for presentation
# ========================

# nonlinearK4bsI.R \
#   final_results.csv \
#   table4.csv

source lib.nonlinearK4bsI.R.PROG.sh

record_batch $PROG \
    --record-input-${io_final_results_id}=final_results.csv \
    --record-output-${io_table4_id}=table4.csv \
    --record-argument-${a_final_results_id}=final_results.csv \
    --record-argument-${a_table4_id}=table4.csv

record_block

# ===========
# table 4 CSV
# ===========

# table4.R \
#   table4.csv \
#   table4.paper.csv

source lib.table4.R.PROG.sh

record_batch $PROG \
    --record-input-${io_table4_id}=table4.csv \
    --record-output-${o_table4_paper_id}=table4.paper.csv \
    --record-argument-${a_table4_id}=table4.csv \
    --record-argument-${a_table4_paper_id}=table4.paper.csv

record_block

# ========
# figure 4
# ========

#figure2-3s.R \
#   -s \
#   final_results.csv \
#   Richness \
#   O/V/25/5 O/V/25/1 O/V/30/5 A/V/25/5 CO/V/25/5 \
#   figure4.a_and_b.pdf

source lib.figure2-3s.R.PROG.sh

record_batch $PROG \
    --record-argument-${a_splits} \
    --record-argument-${a_final_results}=final_results.csv \
    --record-argument-${a_main_scenario}=Richness \
    --record-argument-${a_small_scenarios}="O/V/25/5 O/V/25/1 O/V/30/5 A/V/25/5 CO/V/25/5" \
    --record-argument-${a_figure4}=figure4.a_and_b.pdf \
    --record-input-${io_final_results_id}=final_results.csv \
    --record-output-${o_figure4_id}=figure4.a_and_b.pdf

record_block

# ========
# figure 5
# ========

#treehist3.pl \
#    -cp 0.0075 \
#    final_results.csv  \
#    LOBEC.rpart3Xfr.pdf  \
#    Richness \
#    Government,Market,BET,ASP,Expenditure 

source lib.treehist3.pl.PROG.sh

record_batch $PROG \
    --record-input-${io_final_results_id}=final_results.csv \
    --record-argument-${a_complexity_variable_id}=0.0075 \
    --record-argument-${a_response_variable_id}=Richness \
    --record-argument-${a_final_results_id}=final_results.csv \
    --record-argument-${a_figure5_id}=LOBEC.rpart3Xfr.pdf  \
    --record-argument-${a_explanatory_variables_id}=Government,Market,BET,ASP,Expenditure  \
    --record-output-${o_figure5_id}=LOBEC.rpart3Xfr.pdf 

record_block

# ========
# Appendix 
# ========

#figure2-3small.R -splits final_results.csv \
#    Richness \
#    appendix.pdf \
#    A/F/30/1 A/V/25/1 CO/F/25/5 CO/F/30/1 CO/F/30/5 CO/V/25/1 CO/V/30/1 \
#    CO/V/30/5 CA/F/25/1 CA/F/30/1 CA/F/30/5 CA/V/25/1 CA/V/25/5 CA/V/30/1 \
#    CA/V/30/5 CO/F/25/1 CO/F/25/5 CO/F/30/1 CO/F/30/5 CO/V/25/1 CO/V/30/1 \
#    CO/V/30/5

source lib.figure2-3small.R.PROG.sh

record_batch $PROG \
    --record-argument-${a_splits} \
    --record-argument-${a_final_results}=final_results.csv \
    --record-argument-${a_appendix}=appendix.pdf \
    --record-argument-${a_y_axis}=Richness \
    --record-argument-${a_scenarios}="A/F/30/1 A/V/25/1 CO/F/25/5 CO/F/30/1 CO/F/30/5 CO/V/25/1 CO/V/30/1 CO/V/30/5 CA/F/25/1 CA/F/30/1 CA/F/30/5 CA/V/25/1 CA/V/25/5 CA/V/30/1 CA/V/30/5 CO/F/25/1 CO/F/25/5 CO/F/30/1 CO/F/30/5 CO/V/25/1 CO/V/30/1 CO/V/30/5" \
    --record-input-${io_final_results_id}=final_results.csv \
    --record-output-${o_appendix_id}=appendix.pdf

record_block

# This is a bit of a PITA. Sometimes you need the following, sometimes you
# don't. But it ensures that zero status is returned from the $record_run
# program above, and thus the flow of the code is not terminated

record_end
exit 0

