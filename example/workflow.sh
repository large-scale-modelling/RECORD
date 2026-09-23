#!/usr/bin/env bash

# A script which is trying to regenerate the data and consequently
# rerun the model for Gary's paper, automate the process and record
# lots and lots of metadata into a relational database, as a kind of
# diary for the model run.

# Author: Doug Salt

# Date: April 2017

. lib/record.sh

record_start

# Metadata
# ========

source lib.c5.wp1.provenance-framework.miracle-reconstruction.study.sh

experiment_id=$(record_study \
	study_experiment_$(record_unique_string) \
	$c5_wp1_provenance_framework_miracle_reconstruction_study_id \
	--project=$project_id \
	--start_time=$(date "+%Y-%m-%d") \
	--description="""
        This is a single run to reconstruct the diagrams and results
        in Polhill et al. 2013.  Originally we were going to use
        Python scripts to do the job control for us, but I have
        decided to remain with shell scripts, to try and preserve
        the original flavour. But these might be too slow.""" \
	--title="SSS-cluster2 reconstruction" \
) || exit -1

# This sets global values that are used as extra parameters
# should the schema call for them in particular it sets
# STANDARD_ARGS consisting of the model, licence and
# version. It also sets the GENERATED_BY variable to
# --generated_by=$experiment_id which is used internally.

record_set --study=$experiment_id \
	--model=model_fearlus-spom \
	--licence=GPLv3 \
	--version=1.0 \

# Local Identity (particulars of this script)
# ==============

ME=$(record_application \
    --language=bash \
    --version=1.0 \
    --licence=GPLv3 \
    --purpose="Overall workflow shell script" \
    --model=model_fearlus-spom \
) || exit -1

record_contributor $ME $doug_salt_id Developer
record_contributor $ME $doug_salt_id Author

record_tag $awkward_syntax_tag --application=$ME
record_tag $too_slow_tag --application=$ME
record_tag $awful_bash_code_tag --application=$ME

# Experiment set up
# =================

source lib.SSS-StopC2-Cluster-create.sh.PROG.sh
record_run $PROG

source lib.SSS-StopC2-Cluster-create2.sh.PROG.sh
record_run $PROG

# Run the experiment
# ==================

source lib.SSS-StopC2-Cluster-run.sh.PROG.sh
record_run $PROG

source lib.SSS-StopC2-Cluster-run2.sh.PROG.sh
record_run $PROG

# Processing the results
# ======================

source lib.postprocessing.sh.PROG.sh
record_run $PROG


record_study \
	$experiment_id \
    $c5_wp1_provenance_framework_miracle_reconstruction_study_id \
	--project=$project_id \
	--end_time=$(date "+%Y%m%dT%H%M%S") > /dev/null

record_end
