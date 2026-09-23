#!/usr/bin/env bash

# Date: January 2017 - Need to date a script

. lib/record.sh

record_start

# Identity
# ========

source lib.SSS-StopC2-Cluster-run2.sh.PROG.sh

# Execution specific
# ==================

# Identify for what we are running. You only need to do this if you cannot include the code in the script.
# Ideally the next line would be done from within the code itself, but sometime you cannot modify the code

source lib.fearlus-1.1.5.2_spom-2.3.PROG.sh

for govt in RewardActivity RewardSpecies 
do
    for run in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020
    do
        for market in flat var2
        do
            for sink in nosink
            do
                for rwd in 15.0 20.0 25.0 30.0 40.0 50.0 100.0
                do
                    for asp in 1.0 5.0
                    do
                       for bet in 25.0 30.0
                        do
                            for rat in 1.0
                            do

                                DIR=Cluster2-2/SSS_dir_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_
                                report=${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}
                                param=SSS_top-level_${report}.model

                                ARGS="""
                                --record-argument-${a_batch_id}
                                --record-argument-${a_varyseed_id}
                                --record-argument-${a_repconfig_id}=SSS_report-config_${report}.repcfg
                                --record-argument-${a_report_id}=SSS_report_${report}.txt
                                --record-argument-${a_parameters_id}=$param
                                """

                                ARGS="""$ARGS
                                --record-input-${io_SSS_economystate_id}=SSS_economystate______${market}_____.state 
                                --record-input-${io_SSS_top_level_subpop_id}=SSS_top-level-subpop________noapproval_0_${asp}_.ssp 
                                --record-input-${io_SSS_grid_id}=SSS_grid___________${run}.grd 
                                --record-input-${io_SSS_top_level_id}=SSS_top-level_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.model 
                                --record-input-${io_SSS_species_id}=SSS_species_${sink}__________.csv 
                                --record-input-${io_SSS_subpop_id}=SSS_subpop________noapproval_0_${asp}_.sp 
                                --record-input-${io_SSS_yieldtree_id}=SSS_yieldtree___________.tree 
                                --record-input-${io_SSS_fearlus_id}=SSS_fearlus__${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.fearlus 
                                --record-input-${io_SSS_government_id}=SSS_government__${govt}_all_${rwd}_${rat}______.gov 
                                --record-input-${io_SSS_sink_id}=SSS_sink_${sink}__________.csv 
                                --record-input-${io_SSS_incometree_id}=SSS_incometree______${market}_____.tree 
                                --record-input-${io_SSS_luhab_id}=SSS_luhab___________.csv 
                                --record-input-${io_SSS_climateprob_id}=SSS_climateprob___________.prob 
                                --record-input-${io_SSS_patch_id}=SSS_patch_${sink}__________${run}.csv 
                                --record-input-${io_SSS_report_config_id}=SSS_report-config_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.repcfg 
                                --record-input-${io_SSS_yielddata_id}=SSS_yielddata___________.data 
                                --record-input-${io_SSS_spom_id}=SSS_spom_${sink}__________${run}.spom 
                                --record-input-${io_SSS_economyprob_id}=SSS_economyprob___________.prob 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-1.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-2.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-3.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-4.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-5.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-6.csv 
                                --record-input-${io_SSS_dummy_id}=SSS_dummy___________-7.csv 
                                --record-input-${io_SSS_incomedata_id}=SSS_incomedata______${market}_____.data 
                                --record-input-${io_SSS_event_id}=SSS_event________noapproval___.event 
                                --record-input-${io_SSS_trigger_id}=SSS_trigger________noapproval___.trig 
                                 """

                                ARGS="""$ARGS
                                --record-stdout-${o_SSS_OUT_id}=${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.out
                                --record-stder-${o_SSS_ERR_id}=${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.err
                                --record-output-${io_SSS_report_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.txt
                                --record-output-${io_SSS_report_grd_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.grd
                                --record-output-${o_SSS_spomresult_prop_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-prop.csv
                                --record-output-${o_SSS_spomresult_nspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-nspp.csv
                                --record-output-${io_SSS_spomresult_lspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-lspp.csv
                                --record-output-${io_SSS_spomresult_extinct_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-extinct.csv
                                --record-output-${o_SSS_spomresult_pspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-pspp.csv
                                --record-output-${o_SSS_spomresult_habgrid_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-habgrid.csv
                                --record-output-${o_SSS_spomresult_area_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-area.csv
                                """

                                record_batch $PROG $ARGS --cwd=$DIR
                            done
                        done
                    done
                done
            done
        done
    done
done

wait

record_end --block
