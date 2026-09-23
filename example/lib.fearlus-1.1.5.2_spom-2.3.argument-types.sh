FOR="fearlus-1.1.5.2_spom-2.3.batch"

a_batch_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.batch" \
	--description="Run in batch mode" \
	--name="batch" \
	--short_name="b" \
	--type=flag \
) || exit -1

a_varyseed_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.varyseed" \
	--short_name="s" \
	--name="varyseed" \
	--description="Select random number seed from current time" \
	--type=flag \
) || exit -1

a_show_current_time_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.show_current_time" \
	--short_name="t" \
	--name="show-current-time" \
	--description="Show current time in control panel" \
	--type=flag \
) || exit -1

a_no_init_file_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.no_init_file" \
	--name="no-init-file" \
	--description="Inhibit loading of ~/.swarmArchiver" \
	--type=flag \
) || exit -1

a_verbose_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.verbose" \
	--short_name="v" \
	--name="verbose" \
	--description="Activate verbose messages" \
	--type=flag \
) || exit -1

a_append_report_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.append_report" \
	--short_name="a" \
	--name="append-report" \
	--type=flag \
	--arity=0 \
	--description="If report file exists, then append to it" \
) || exit -1

a_ontology_all_years_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.ontology_all_years" \
	--short_name="A" \
	--name="ontology-all-years" \
	--description="Output a model state ontology each year (warning:" \
	--type=flag \
) || exit -1

a_conditions_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.conditions" \
	--short_name="-c" \
	--name="conditions" \
	--description="Show conditions of redistribution" \
	--type=flag \
) || exit -1

a_warranty_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.warranty" \
	--short_name="w" \
	--name="warranty" \
	--description="Show warranty information" \
	--type=flag \
) || exit -1

a_help_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.help" \
	--short_name="?" \
	--name="help" \
	--description="Give this help list" \
	--type=flag \
) || exit -1

a_usage_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.usage" \
	--name="usage" \
	--description="Give a short usage message" \
	--type=flag \
) || exit -1

a_version_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.version" \
	--short_name="V" \
	--name="version" \
	--description="Print program version" \
	--type=flag \
) || exit -1

a_seed_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.seed" \
	--short_name="S" \
	--name="seed" \
	--description="Specify seed for random numbers" \
	--arity=1 \
	--range='[0-9]+' \
	--type=option \
) || exit -1

a_mode_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.mode" \
	--short_name="m" \
	--name="mode" \
	--description="Specify mode of use (for archiving) will potentially require a lot of disk space)" \
	--arity=1 \
	--type=option \
	--range='^\s+' \
) || exit -1
	

a_ontology_class_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.ontology_class" \
	--short_name="C" \
	--name="ontology-class" \
	--description="Record structural ontology from subclasses of CLASS" \
	--arity=1 \
	--type=option \
	--range='^\s+' \
) || exit -1

a_debug_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.debug" \
	--short_name="D" \
	--name="debug" \
	--description="Debug level (integer) and/or a list of +/- separated message symbols" \
	--arity=1 \
	--type=option \
	--range='^\s+((\+|\-)\s+)?$' \
) || exit -1

a_gridServiceUID_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.gridServiceUID" \
	--short_name="g" \
	--name="gridServiceUID" \
	--description="User ID for FEARLUS-G Service" \
	--arity=1 \
	--type=option \
	--range='^\s+' \
) || exit -1

a_gridServiceURL_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.gridServiceURL" \
	--short_name="G" \
	--name="gridServiceURL" \
	--description="URL for FEARLUS-G Service" \
	--arity=1 \
	--type=option \
	--range='absolute_URI' \
) || exit -1

a_gridModelDescription_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.gridModelDescription" \
	--short_name="H" \
	--name="gridModelDescription" \
	--description="Description for this model" \
	--arity=1 \
	--type=option \
	--range='^\s+$' \
) || exit -1

a_javapath_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.javapath" \
	--short_name="j" \
	--name="javapath" \
	--description="Path to java Grid Client" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_rng_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.rng" \
	--short_name="n" \
	--name="rng" \
	--description="Class of RNG to use" \
	--arity=1 \
	--type=option \
	--range='^\s+$' \
) || exit -1

a_observers_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.observers" \
	--short_name="o" \
	--name="observers" \
	--description="File for the observer settings to be loaded from" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_ontology_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.ontology" \
	--short_name="O" \
	--name="ontology" \
	--description="Name of file to output ontology to" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_parameters_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.parameters" \
	--short_name="p" \
	--name="parameters" \
	--description="File for the model parameters to be loaded from" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_report_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.report" \
	--short_name="r" \
	--name="report" \
	--description="File to save the report to (stdout by default)" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_repconfig_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.repconfig" \
	--short_name="R" \
	--name="repconfig" \
	--description="Reporter configuration file" \
	--arity=1 \
	--type=option \
	--range='path' \
) || exit -1

a_ontology_uri_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.ontology_uri" \
	--short_name="U" \
	--name="ontology-uri=URI" \
	--description="URI for ontology" \
	--arity=1 \
	--type=option \
	--range='absolute_URI' \
) || exit -1

a_withseed_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.withseed" \
	--short_name="X" \
	--name="withseed" \
	--description="Specify the seed. [0-9]+, TIME or DEFAULT" \
	--arity=1 \
	--type=option \
	--range='^([0-9]+|TIME|DEFAULT)$' \
) || exit -1

a_postinitseed_id=$(record_argument_type \
	$PROG \
	"argument.$FOR.postinitseed" \
	--short_name="-Z" \
	--name="postinitseed" \
	--description="Specify a separate seed to use after initialisation: [0-9]+ or TIME" \
	--arity=1 \
	--type=option \
	--range='^([0-9]+|TIME)' \
) || exit -1


