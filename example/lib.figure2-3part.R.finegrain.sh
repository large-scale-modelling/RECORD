vm_figure3_id=$(record_visualisation_method \
    "visualisation_method.figure2-3part.R.figure_3" \
    "A sunflower plot with curve fitting, plotting incentive (x-axis)
    against landscape scale species richness (y-axis)" \
) || exit -1

record_implements $PROG \
    --visualisation_method=$vm_figure3_id

record_implements $PROG \
    --visualisation_method=$vm_sunflower_plot_id
record_implements $PROG \
    --statistical_method=$sm_recursive_partitioning_id
record_implements $PROG \
    --visualisation_method=$vm_general_additive_model_id

sv_min_incentive_id=$(record_visualisation_variable \
    "visualisation_method.figure2-3part.R.figure3_min_incentive" \
    "Minimum value for horizontal axis in figure 3" \
    "\Z_{\ne 0}" \
    $vm_sunflower_plot_id \
) || exit -1

sv_max_incentive_id=$(record_visualisation_variable \
    "visualisation_method.figure2-3part.R.figure3_max_incentive" \
    "Max value for horizontal axis in figure 3" \
    "\Z_{\ne 0}" \
    "$vm_sunflower_plot_id" \
) || exit -1

con_figure3_sunflower_plot_id=$(record_content \
    --visualisation_method="$vm_sunflower_plot_id" \
    --box_type=$o_figure3_id \
) || exit -1

con_scenario_id=$(record_content \
    --variable=$var_scenario_id \
    --box_type=$o_figure3_id \
    --locator='grep -v ^scenario | cut -f1 -d,' \
) || exit -1

con_min_incentive_id=$(record_content \
    --statistical_variable=$sv_min_incentive_id \
    --box_type=$o_figure3_id \
    --locator='grep -v ^scenario | cut -f2 -d,' \
) || exit -1

con_max_incentive_id=$(record_content \
    --statistical_variable=$sv_max_incentive_id \
    --box_type=$o_figure3_id \
    --locator='grep -v ^scenario | cut -f3 -d,' \
) || exit -1

sos_sunflower_values=$(record_statistics \
    statistics.$(record_unique_string) \
    $sm_recursive_partitioning_id \
    "Nonsy McNonsy Face Query" \
    figure3.pdf \
) || exit -1


vis_sunflower_plot_fig3=$(record_visualisation \
    visualisation.$(record_unique_string) \
    $vm_sunflower_plot_id \
    "figure2-3part.R final_results.csv cfg/figure3.cfg figure3.pdf" \
    figure3.pdf \
) || exit -1

# Need to add more specifics to these. That is there are more fields for the
# value record

record_value \
    "A/F/30/1" \
    $var_scenario_id \
    figure3.pdf

record_statistical_variable_value \
    2 \
    $sv_min_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_statistical_variable_value \
    10 \
    $sv_max_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_value \
    "A/V/30/1" \
    $var_scenario_id \
    figure3.pdf 

record_statistical_variable_value \
    2 \
    $sv_min_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_statistical_variable_value \
    15 \
    $sv_max_incentive_id \
    figure3.pdf \
    $vis_sunflower_plot_fig3

record_value "CA/F/25/5" \
    $var_scenario_id \
    figure3.pdf 

record_visualisation_variable_value \
    1 \
    $sv_min_incentive_id \
    figure3.pdf \
    $vis_sunflower_plot_fig3

record_statistical_variable_value \
    10 \
    $sv_max_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_value \
    "O/F/30/5" \
    $var_scenario_id \
    figure3.pdf \
    $vis_sunflower_plot_fig3

record_statistical_variable_value \
    1 \
    $sv_min_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_statistical_variable_value \
    8 \
    $sv_max_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_value \
    "O/V/25/1" \
    $var_scenario_id \
    figure3.pdf \
    $vis_sunflower_plot_fig3

record_statistical_variable_value \
    1 \
    $sv_min_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_statistical_variable_value \
    5 \
    $sv_max_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3

record_value \
    "CO/V/25/5" \
    $var_scenario_id \
    figure3.pdf 

record_statistical_variable_value \
    0.1 \
    $sv_min_incentive_id \
    figure3.pdf \ 
    $sos_sunflower_plot_fig3

record_statistical_variable_value \
    0.8 \
    $sv_max_incentive_id \
    figure3.pdf \
    $sos_sunflower_plot_fig3
 

