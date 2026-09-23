#!/usr/bin/env bash
#
# Shell script to create the SSS preliminary experiments. These are designed
# to cover sinks/nosinks and RewardActivity/RewardSpecies, at various BETs and
# ASPs, and for flat and var2 market. There will be 20 runs each

. lib/record.sh

record_start

# Identity (stuff about this script)
# ========

source lib.SSS-StopC2-Cluster-create.sh.PROG.sh

# Execution specific
# ==================

source lib.SSS-StopC2-Cluster-expt.pl.PROG.sh

for govt in ClusterActivity RewardActivity RewardSpecies ClusterSpecies 
do
    for run in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020
    do
        for market in flat var2
        do
            for sink in nosink
            do
                for rwd in 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0
                do
                    for asp in 1.0 5.0
                    do
                        for bet in 25.0 30.0
                        do
                            for rat in 1.0 2.0 10.0
                            do
                                DIR="SSS_dir_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_"
                                ARGS="""
                                --record-argument-${a_govt_id}=$govt
                                --record-argument-${a_sink_id}=NO
                                --record-argument-${a_market_id}=$market
                                --record-argument-${a_zone_id}=all
                                --record-argument-${a_reward_id}=$rwd
                                --record-argument-${a_ratio_id}=$rat
                                --record-argument-${a_bet_id}=$bet
                                --record-argument-${a_approval_id}=NO
                                --record-argument-${a_iwealth_id}=0
                                --record-argument-${a_aspiration_id}=$asp
                                --record-argument-${a_run_id}=$run
                                """

                                ARGS="""$ARGS
                                --record-output-${io_SSS_sink_id}="$DIR/SSS_sink_${sink}__________.csv"
                                --record-output-${io_SSS_incometree_id}="$DIR/SSS_incometree______${market}_____.tree"
                                --record-output-${io_SSS_luhab_id}="$DIR/SSS_luhab___________.csv"
                                --record-output-${io_SSS_climateprob_id}="$DIR/SSS_climateprob___________.prob"
                                --record-output-${io_SSS_patch_id}="$DIR/SSS_patch_${sink}__________${run}.csv"
                                --record-output-${io_SSS_report_config_id}="$DIR/SSS_report-config_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.repcfg"
                                --record-output-${io_SSS_yielddata_id}="$DIR/SSS_yielddata___________.data"
                                --record-output-${io_SSS_spom_id}="$DIR/SSS_spom_${sink}__________${run}.spom"
                                --record-output-${io_SSS_economyprob_id}="$DIR/SSS_economyprob___________.prob"
                                --record-output-${io_SSS_incomedata_id}="$DIR/SSS_incomedata______${market}_____.data"
                                --record-output-${io_SSS_event_id}="$DIR/SSS_event________noapproval___.event"
                                --record-output-${io_SSS_trigger_id}="$DIR/SSS_trigger________noapproval___.trig"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-1.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-2.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-3.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-4.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-5.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-6.csv"
                                --record-output-${io_SSS_dummy_id}="$DIR/SSS_dummy___________-7.csv"
                                """

                                record_batch $PROG $ARGS --cwd="Cluster2"
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
