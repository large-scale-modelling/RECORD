project_id=$(record_project \
	project_c5 \
    --title="Integrated socio-environmental modelling of policy scenarios for Scotland" \
    --description="Computer modelling has an increasing role to play in helping to navigate the
landscapes of complex social-environmental decision-making processes and offer
decision-makers integrated, consistent guidance based on formalizations of
evidence. Such computer modelling needs to be accountable and transparent,
especially when the consequences of such decisions have impacts on businesses
and citizens. Modelling and data analysis in this project is driven by: (a) the need to
monitor the health of Scotland’s soils in support of production of land-derived goods,
biodiversity, regulation of water and nutrient flows, and carbon sequestration; (b)
biophysical and societal pressures on arable land systems and the threats and
opportunities from climate change; (c) changes in frameworks for supporting
production systems, changes in international trade agreements, and technological
innovations particularly in the circular economy.
This proposed project develops the science needed to integrate data and
models about Scotland’s rural social-environmental systems, with the goal of
developing the capability to answer policy-led questions quickly. In terms of spatial
extent, we interpret ‘large-scale’ as meaning the whole of Scotland, plus the national
and global contexts in which Scotland sits. ‘Large-scale’ also means including more
system components to avoid the ‘water-bed’ effect in which addressing one problem
causes another; and finer granularity in the explicit representation of space, time,
people and organizations.
To develop the capability to answer policy-led questions quickly, this project
will experiment with ‘agile’ modes of research project management (WP0), focusing
on early delivery of value through prototyping, followed by iterative cycles of
improvement [1]. Hence, we emphasize regular interaction with the stakeholders in
the research, while monitoring and adapting the measurement of the various
dimensions that constitute ‘value’. This is supported by the development of time-
efficient protocols for mediating stakeholder participation in model specification and implementation." \
    --funder="Scottish Government" \
    --grant_id="JHI-C5-1" \
) || exit -1

# Note the study and the part are the same here. This is because this is a
# top-level study and has no parent (other than itself).

c5_study_id=$(record_study \
    study_c5 \
    study_c5 \
	--project=$project_id \
	--start_time="2022-04-01" \
	--end_time="2027-03-31" \
	--description="Integrated socio-environmental modelling of policy scenarios for Scotland 
The project has the objective to conduct research in support of providing integrated
and transparent models, datasets and tools for analysis of rapid-response, policy-
led, rural social-environmental scenarios at the whole-of-Scotland scale. The
objective will be measured by: the number of scenarios explored that are linked to
documented requests from stakeholders; the time taken to provide results from
those scenarios; the adaptations made during the course of the project to improve
the previous two metrics; the novel software tools created or adapted; adherence to
FAIR (Findable, Accessible, Interoperable and Reusable) principles [2] through use
of well-known repositories, licensing and research done in WP1; contributions to the
scientific discourse (conference and journal papers, organized sessions and
workshops); and funding from competitively-tendered sources gained. The project
will review its progress against these metrics at least quarterly, with at least one such
review entailing a virtual or physical face-to-face meeting with stakeholders." \
	--title="Integrated socio-environmental modelling of policy scenarios for Scotland" \
) || exit -1


record_involvement \
    $c5_study_id \
    $doug_salt_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
    $gary_polhill_id \
    "Principal investigator"

record_involvement \
    $c5_study_id \
	$becky_smith_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
	$alessandro_gimona_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
	$matt_hare_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
	$allan_lilly_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
	$mike_rivington_id \
    "Primary investigator (deputy)"

record_involvement \
    $c5_study_id \
	$marie_castellazzi_id \
    "Co-investigator"

record_involvement \
    $c5_study_id \
	$ben_mccormick_id \
    "Co-investigator"


