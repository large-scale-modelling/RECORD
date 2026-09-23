# PURPOSE

This directory provides a reference implementation for RECORD.

This is based on the SSS-complex runs, where, I believe SSS stands for Swarm Social Simulation. The original repository for this is [here](https://https://github.com/garypolhill/FEARLUS-SPOMM).

The key files to inspect are:

+ `workflow.sh`

this calls:

+ `SSS-StopC2-Cluster-create2.sh`
+ `SSS-StopC2-Cluster-create.sh`
+ `SSS-StopC2-Cluster-run2.sh`
+ `SSS-StopC2-Cluster-run.sh`
+ `postprocessing.sh`

This is run from the directory above this.

1. `source example/ENVIRONMENT.sh` (presuming the ENVIRONMENT.sh file has been
   created and modified and the Python environments created.
2. record-start.sh

# MANIFEST

The actual model itself is this file:

+ `fearlus-1.1.5.2_spom-2.3` - the model.

This are the scripts to set up the runs and run the runs.

+ `workflow.sh` - this recreates the main workflow program, eventually this will be done by SSS-cluster.py2.py

calls the remainder:

+ `SSS-StopC2-Cluster-create2.sh` - creates the input values for the low reward/incentives run
+ `SSS-StopC2-Cluster-create.sh` - creates the input values for the higt reward/incentives run
+ `SSS-StopC2-Cluster-run2.sh` - runs the model for the low reward/incentives 
+ `SSS-StopC2-Cluster-run.sh` -  runs the model for the high reward/incentives 

The following are the scripts that do the post-run analysis.

+ `postprocessing.sh` calls the following

+ `analysege_gpLU2.pl` - collects all the output data from all runs

with the remainder, which produce the results and diagrams are:

+ `figure2-3part.R`
+ `figure2-3.R`
+ `figure2-3small.R`
+ `figure2-3s.R`
+ `nonlinearK4bsI.R`
+ `nonlinearK4I.R`
+ `table4.R`
+ `treehist3.pl`

+ `postprocessing.R` - this recreates the manual R manipulation that Gary did to get the results. `postprocessing.R` and `table4.R` are scripts I have created to recreate what Gary did manually.

+ `figure3.cfg` - this is the configuration input to `figure2-3part.R`
+ `scenarios.cfg` - this is a configuration input to `postprocessing.R`

+ `lib.` _program_name_`.PROG.sh`
+ `lib.` _program_name_`.input-types.sh`
+ `lib.` _program_name_`.output-types.sh`
+ `lib.` _program_name_`.argument-types.sh`
+ `lib.` _program_name_`.requirements.hardware.sh`
+ `lib.` _program_name_`.requirements.software.sh`

    where _program_name_ can be any of the following:

        - `workflow.sh`
        - `SSS-StopC2-Cluster-create2.sh`
        - `SSS-StopC2-Cluster-create.sh`
        - `SSS-StopC2-Cluster-run2.sh`
        - `SSS-StopC2-Cluster-run.sh`
        - `postprocessing.sh`
        - `fearlus-1.1.5.2_spom-2.3`
        - `figure2-3part.R`
        - `figure2-3.R`
        - `figure2-3small.R`
        - `figure2-3s.R`
        - `nonlinearK4bsI.R`
        - `nonlinearK4I.R`
        - `table4.R`
        - `treehist3.pl`
        - `postprocessing.R`
    
    These are "sourced" into the code and are organized in such a way, so it is easy to construct them (this will all be automated at some point).

    The `PROG` is the overall source file, contains the application definition and sources all the other specifications, which consist of

        1. hardware required to run the application
        2. software required to run the application
        3. the input box types required to run the application
        4. the output box types required to run the application
        5. the argument types that an application takes.
    
+ `Reconstructing the diagrams and results in Polhill et al.docx` - a blank document representing a place holder for documentation in referrred to in the metadata

This is the re-usable part of the study metadata. These are nested in the following manner, allowing component re-use.

+ `lib.c5.study.sh` ->
+ `lib.c5.wp1.study.sh`  ->
+ `lib.c5.wp1.provenance-framework.study.sh` ->
+ `lib.c5.wp1.provenance-framework.miracle-reconstruction.study.sh`

The next are experimental and are not actually included in the actual system testing. They have been written to test out 

+ `lib.figure2-3part.R.finegrain.sh`
+ `lib.figure2-3s.R.finegrain.sh`
+ `lib.postprocessing.sh.finegrain.sh`
+ `lib.treehist3.pl.finegrain.sh`

+ `lib.record.clean.sh` - Any specific cleaning which is specific to this example

+ `lib.folksonomy.sh` - The folksonomy.
