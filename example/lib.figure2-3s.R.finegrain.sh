
record_implements $PROG --visualisation_method=$vm_sunflower_plot_id

con_figure4_sunflower_plot_id=$(record_content \
    --visualisation_method=$vm_sunflower_plot_id \
    --box_type=$o_figure4_id \
) || exit -1

con_varscenario_id=$(record_content \
    --variable=$var_scenario_id \
    --box_type=$o_figure4_id \
    --locator='grep -v ^scenario | cut -f1 -3,' \
) || exit -1

vis_sunflower_plot_fig4=$(record_visualisation \
    visualisation_$(record_unique_string) \
    $vm_sunflower_plot_id \
    "\"figure2-3s.R -splits final_results.csv Richness A/F/25/5 A/F/25/1 A/F/30/5 O/F/25/5 CA/F/25/5 figure4.a_and_b.pdf\"" \
    figure4.a_and_b.pdf \
) || exit -1


