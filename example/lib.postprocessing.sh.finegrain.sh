# Methods
# =======

sm_aic_id=$(record_statistical_method \
    "statistical_method.processing.sh.aic" \
    "The Akaike information criterion (AIC) 
    is a measure of the relative quality of statistical models for a 
    given set of data. Given a collection of models for the data, AIC 
    estimates the quality of each model, relative to each of the other 
    models. Hence, AIC provides a means for model selection." \
) || exit -1

sm_bic_id=$(record_statistical_method \
    "statistical_method.processing.sh.bi" \
    "Bayesian Information Criterion (BIC) 
    or Schwarz criterion (also SBC, SBIC) is a criterion for model 
    selection among a finite set of models; the model with the lowest 
    BIC is preferred." \
) || exit -1

sm_edf_id=$(record_statistical_method \
    "statistical_method.processing.sh.edf" \
    "Empirical Distribution Function is the
    distribution function associated with the empirical measure of a
    sample. This cumulative distribution function is a step function that
    jumps up by 1/n at each of the n data points. Its value at any 
    specified value of the measured variable is the fraction of 
    observations of the measured variable that are less than or equal to 
    the specified value." \
) || exit -1

sm_anova_gam_id=$(record_statistical_method \
    "statistical_method.processing.sh.anova.gam" \
    "Performs
    hypothesis tests relating to one or more fitted gam objects." \
) || exit -1

sm_recursive_partitioning_id=$(record_statistical_method \
    "statistical_method.processing.sh.recursive_partioning" \
    "Recursive partitioning for classification,
    regression and survival trees.  An implementation of most of the
    functionality of the 1984 book by Breiman, Friedman, 
    Olshen and Stone." \
) || exit -1

vm_sunflower_plot_id=$(record_visualisation_method \
    "statistical_method.processing.sh.sunflower_plot" \
    "Looks like a sunflower drawn in a 2D space. The sunflower plots 
    are used as variants of scatter plots to display bivariate 
    distribution. When the density of data increases in a particular 
    region of a plot, it becomes hard to read." \
) || exit -1

vm_general_additive_model_id=$(record_visualisation_method \
    "statistical_method.processing.sh.general_additive_method" \
    "A generalized additive model (GAM) is a generalized linear model 
    in which the linear predictor depends linearly on unknown smooth 
    functions of some predictor variables, and interest focuses on 
    inference about these smooth functions.
    
    Note Bene: this is not a visualisation method, but I just wanted
    some more examples of visualisation methods." \
) || exit -1

# I really don't like the nomenclature here. I think the conventions adopted
# are totally confusing, but I will go with them.

# In finegrain and analysis it is the Values table we are interested in.

# Process level settings

# + Visualisation -> StatitisticalInput -> Value
# + Statistics -> StatitisticalInput -> Value

# (StatisticalVariable(generated_by) -> StatisticalMethod) ->

# So I have sorted out StatisticalVariable. This is any variable generated a
# statistical method, which can be used (via employs) by a method, and in fact,

# Parameters deal purely with methods. I am presuming all these may
# take values at run time.

# Parameters
# ==========

par_partitioning_complexity_id=$(record_parameter \
    "parameter.postprocessing.sh.complexity" \
    "Prune all nodes with a complexity less than cp from the output." \
    "x \in \Re: x \in [0,1]" \
    --statistical_method="$sm_recursive_partitioning_id" \
) || exit -1

# So a variable is in a box of some description and can act as an 
# input to VisualisationMethod, as opposed to a parameter, which is provided
# as an argument. Fair enough. 

# Variables
# =========

var_scenario_id=$(record_variable  \
    "variable.postprocessing.sh.scenario"  \
    "The combination of government, market, 
    break-even threshold and aspiration" \
    String \
) || exit -1


# Admittedly the next is not a statistical method, but I have used it as such
# to illustrate how these primitives might be employed.

sm_analysege_gpLU2_id=$(record_statistical_method \
    "statistical_method.postprocessing.sh.Post-run-analysis-script" \
    "The output is a CSV format
 summary of the results from each run, listing the parameters first, then
 the results: the number of bankruptcies, the amount of land use change,
 the year of extinction of each species, and the abundance of each species.

 Number of species at a given time step
 Level of occupancy at each time step
 Shannon index and evenness measure." \
) || exit -1

sos_statistics_set_1=$(record_statistics statistics.$(record_unique_string)\
    $sm_analysege_gpLU2_id \
    "analysege_gpLU2.pl 8" \
) || exit -1

sos_statistics_set_2=$(record_statistics statistics.$(record_unique_string)\
    $sm_analysege_gpLU2_id \
    "analysege_gpLU2.pl 9" \
) || exit -1

sv_bankruptcies_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.bankruptcies" \
    "A column containing the number of bankruptcies." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_land_use_change_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.land_use_change" \
    "A column containing land use change." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu1_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu1" \
    "A column containing occupancy for landuse 1." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu2_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu2" \
    "A column containing occupancy for landuse 3." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu3_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu3" \
    "A column containing occupancy for landuse 3." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu4_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu4" \
    "A column containing occupancy for landuse 4." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu5_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu5" \
    "A column containing occupancy for landuse 5." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_lu6_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_lu6" \
    "A column containing occupancy for landuse 6." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_1_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_1" \
    "A column containing the number of extinctions for species 1 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_2_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_2" \
    "A column containing the number of extinctions for species 2 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_3_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_3" \
    "A column containing the number of extinctions for species 3 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_4_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_4" \
    "A column containing the number of extinctions for species 4 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_5_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_5" \
    "A column containing the number of extinctions for species 5 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_6_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_6" \
    "A column containing the number of extinctions for species 6 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_7_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_7" \
    "A column containing the number of extinctions for species 7 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_8_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_8" \
    "A column containing the number of extinctions for species 8 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_9_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_9" \
    "A column containing the number of extinctions for species 9 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_extinction_spp_10_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.extinction_spp_10" \
    "A column containing the number of extinctions for species 10 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_1_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_1" \
    "A column containing the occupancy for species 1 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_2_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_2" \
    "A column containing the occupancy for species 2 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_3_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_3" \
    "A column containing the occupancy for species 3 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_4_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_4" \
    "A column containing the occupancy for species 4 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_5_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_5" \
    "A column containing the occupancy for species 5 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_6_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_6" \
    "A column containing the occupancy for species 6 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_7_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_7" \
    "A column containing the occupancy for species 7 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_8_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_8" \
    "A column containing the occupancy for species 8 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_9_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_9" \
    "A column containing the occupancy for species 9 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_occupancy_spp_10_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.occupancy_spp_10" \
    "A column containing the occupancy for species 10 per patch." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_Shannon_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.Shannon" \
    "A column containing the Shannon number." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_Equitability_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.Equitability" \
    "A column containing the equitabilty." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1

sv_richness_id=$(record_statistical_variable \
    "statistical_variable.postprocessing.sh.richness" \
    "A column containing the number of bankruptcies." \
    "\mathbb{R}" \
    "$sm_analysege_gpLU2_id" \
) || exit -1


