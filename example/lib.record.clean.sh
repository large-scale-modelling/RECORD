# From the working directory, do the following
# grep '\-\-record-output' example/*.sh | grep -v SSS-StopC2-Cluster-create

# which gives:

# example/postprocessing.sh:--record-output-${io_final_results_id}=final_results.csv
# example/postprocessing.sh:--record-output-${o_figure3_id}=figure3.pdf
# example/postprocessing.sh:--record-output-${io_table4_id}=table4.csv
# example/postprocessing.sh:--record-output-${o_table4_paper_id}=table4.paper.csv
# example/postprocessing.sh:--record-output-${o_figure4_id}=figure4.a_and_b.pdf
# example/postprocessing.sh:--record-output-${o_figure5_id}=LOBEC.rpart3Xfr.pdf 
# example/postprocessing.sh:--record-output-${o_appendix_id}=appendix.pdf
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${io_SSS_report_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.txt
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${io_SSS_report_grd_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.grd
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${o_SSS_spomresult_prop_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-prop.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${o_SSS_spomresult_nspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-nspp.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${io_SSS_spomresult_lspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-lspp.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${io_SSS_spomresult_extinct_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-extinct.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${o_SSS_spomresult_pspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-pspp.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${o_SSS_spomresult_habgrid_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-habgrid.csv
# example/SSS-StopC2-Cluster-run2.sh:                                --record-output-${o_SSS_spomresult_area_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-area.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${io_SSS_report_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.txt
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${io_SSS_report_grd_id}=SSS_report_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}.grd
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${o_SSS_spomresult_prop_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-prop.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${o_SSS_spomresult_nspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-nspp.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${io_SSS_spomresult_lspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-lspp.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${io_SSS_spomresult_extinct_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-extinct.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${o_SSS_spomresult_pspp_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-pspp.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${o_SSS_spomresult_habgrid_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-habgrid.csv
# example/SSS-StopC2-Cluster-run.sh:                                    --record-output-${o_SSS_spomresult_area_id}=SSS_spomresult_${sink}_${govt}_all_${rwd}_${rat}_${market}_${bet}_noapproval_0_${asp}_${run}-area.csv

rm all_results.csv
rm final_results.csv
rm figure3.pdf
rm table4.csv
rm table4.paper.csv
rm figure4.a_and_b.pdf
rm LOBEC.rpart3Xfr.pdf 
rm appendix.pdf
rm batch?.*

set -xv
find Cluster2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*.txt" -exec rm {} \;
find Cluster2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2grd" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-propCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-nsppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-lsppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-extinctCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-psppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-habgridCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-areaCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2txt" -exec rm {} \;
find Cluster2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2grd" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-propCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-nsppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-lsppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-extinctCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-psppCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-habgridCluster2csv" -exec rm {} \;
find Cluster2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-areaCluster2csv" -exec rm {} \;

find Cluster2-2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*.txt" -exec rm {} \;
find Cluster2-2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2grd" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-propCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-nsppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-lsppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-extinctCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-psppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-habgridCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-areaCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2txt" -exec rm {} \;
find Cluster2-2 -name "SSS_report_*_*_all_*_*_*_*_noapproval_0_*_*Cluster2grd" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-propCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-nsppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-lsppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-extinctCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-psppCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-habgridCluster2csv" -exec rm {} \;
find Cluster2-2 -name "SSS_spomresult_*_*_all_*_*_*_*_noapproval_0_*_*-areaCluster2csv" -exec rm {} \;
set +xv
