#!/usr/bin/env bash 

# When this is called from OSX MAKE SURE YOU USE THE ABOVE HASH BANG IN THE
# CALLING PROGRAM. OSX does not support new versions of Bash (because of
# licence stupidity), so their version of bash is antiquated. You need to
# install from other sources. If you do not do the above then the script will
# pick up the older, default version of bash and this script will fail.  You
# have been warned.

# A series of functions to update ssrep.db with an actual run. 

# I have decided to do this in the bash script

# Remember because this is in-line, exit causes a stop program, return to
# abort to calling program.

# The convention here is that any function that starts with an underscore, "_"
# is an internal function.

# Conventions

# _ prefix means internal function  - not to be called in user space
# record_ prefix means exposed to for public use.

# I don't like this and it needs changing. For the gremlin variant, the
# framework is sensitive to parameter order, if it is creating an edge. This is
# not good enough, and I have entered it as an issue for dealing with later.

if [[ -n "$CONFIG_LOADED" ]]
then
    return
fi

record_require_minimum() {

    # This must return 0 for true anything else for false

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	# $1 - app id
	# $2 - executable name or function
	# $3 - required version literal or number
	# $4 - actual version literal or number

    required="$3"
    if [[ "$required" =~ ^[0-9]+T$ ]]
    then
        required=$(echo $required | sed "s/.$//")
        required=$(( $required * 1000000000))
    elif [[ "$required" =~ ^[0-9]+G$ ]]
    then
        required=$(echo $required | sed "s/.$//")
        required=$(( $required * 1000000))
    elif [[ "$required" =~ ^[0-9]+M$ ]]
    then
        required=$(echo $required | sed "s/.$//")
        required=$(( $required * 1000))
    elif [[ "$required" =~ ^[0-9]+K$ ]]
    then
        required=$(echo $required | sed "s/.$//")
    fi
    actual="$4"
    if [[ "$actual" =~ ^[0-9]+T$ ]]
    then
        actual=$(echo $actual | sed "s/.$//")
        actual=$(( $actual * 1000000000))
    elif [[ "$actual" =~ ^[0-9]+G$ ]]
    then
        actual=$(echo $actual | sed "s/.$//")
        actual=$(( $actual * 1000000))
    elif [[ "$actual" =~ ^[0-9]+M$ ]]
    then
        actual=$(echo $actual | sed "s/.$//")
        actual=$(( $actual * 1000))
    elif [[ "$actual" =~ ^[0-9]+K$ ]]
    then
        actual=$(echo $actual | sed "s/.$//")
    fi
	id_computer=$(record-update.py \
		--table=Computer \
		--id_computer=computer_$(hostname) \
		--name=$(hostname) \
		--host_id=$(_fqdn) \
		--ip_address=$(_ip_address) \
		--mac_address=$(_mac_address) \
	) || exit -1
	id_specification=$(record-update.py \
		--table=Specification \
		--id_specification=specification_$2 \
		--specification_of="$id_computer" \
		--value="$3" \
	) || exit -1	
    id_requirement=$(record-update.py \
        --table=Requirement \
        --minimum="$id_specification" \
        --application="$1" \
    ) || exit -1		

    if [ $(type -t "$2") = "function" ]
    then
        : 
    elif which "$2" 
    then
        :
    else 
		[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: executable $2 does not exist ...exit.")
		return -1
    fi

	if echo $required | egrep -q "^[0-9]+(\.[0-9]+)*$" && \
	   echo $actual | egrep -q "^[0-9]+(\.[0-9]+)*$"
	then 
        minimum_major=$(echo $required | cut -f 1 -d\.)
        current_major=$(echo $actual | cut -f 1 -d\.)
        minimum_minor=$(echo $required | cut -f 2 -d\.)
        current_minor=$(echo $actual | cut -f 2 -d\.)
        minimum_minor_sub=$(echo $3 | cut -f 3 -d\.)
        current_minor_sub=$(echo $4 | cut -f 3 -d\.)
        if [ -z "$minimum_minor" ]
        then
            minimum_minor=0
        fi
        if [ -z "$minimum_minor_sub" ]
        then
            minimum_minor_sub=0
        fi
        if [ -z "$current_minor" ]
        then
            current_minor=0
        fi
        if [ -z "$current_minor_sub" ]
        then
            current_minor_sub=0
        fi
        if [ "$current_major" -gt "$minimum_major" ]
        then
            :
        
        elif [ "$current_major" -eq "$minimum_major" ]
        then

            if [ "$current_minor" -gt "$minimum_minor" ]
            then
                :
            
            elif [ "$current_minor" -eq "$minimum_minor" ]
            then

                if  [ -n "$current_minor_sub" ] && [ -n "$minimum_minor_sub" ] && [ "$current_minor_sub" -lt "$minimum_minor_sub" ]
                then
                    [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: on minor sub...exit.")
                    return -1
                fi
            else
                
                [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: on minor...exit.")
                return -1
            fi

        else
            
		    [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: on major ...exit.")
		    return -1
        fi

    else	
		[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: on regex ...exit.")
		return -1
	fi
    id_meets=$(record-update.py \
        --table=Meets \
        --computer_specification="$id_computer" \
        --requirement_specification="$id_specification" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	return 0
}

record_require_exact() {

    # This must return 0 for satisfies/true anything else for false
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	# $1 - app id
	# $2 - spec name
	# $3 - required literal
	# $4 - actual literal

	id_computer=$(record-update.py \
		--table=Computer \
		--id_computer=computer_$(hostname) \
		--name=$(hostname) \
		--host_id=$(_fqdn) \
		--ip_address=$(_ip_address) \
		--mac_address=$(_mac_address) \
	) || exit -1
	id_specification=$(record-update.py \
		--table=Specification \
		--id_specification=specification_$2 \
		--specification_of="$id_computer" \
		--value="$3" \
	) || exit -1
    id_requirement=$(record-update.py \
        --table=Requirement \
        --exact="$id_specification" \
        --application="$1" \
    ) || exit -1
	if [[ "$3" != "$4" ]]
	then
		[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
		return -1
	fi
    id_meets=$(record-update.py \
        --table=Meets \
        --computer_specification="$id_computer" \
        --requirement_specification="$id_specification" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	return 0
}

_process() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_process=
	EXEC=
	if [[ "$@" != *--executable* ]]
	then
		EXEC="--executable="$(basename $0)
	else
		EXEC=''
	fi
	if [[ "$@" == *--id_process* ]]
	then
   		id_process=$(record-update.py \
			--table=Process \
			$@ \
		) || exit -1
	else
		id_computer=$(record-update.py \
			--table=Computer \
			--id_computer=computer_$(hostname) \
			--name=$(hostname) \
			--host_id=$(_fqdn) \
			--ip_address=$(_ip_address) \
			--mac_address=$(_mac_address) \
		)  || exit -1

		id_process=$(record-update.py \
			--table=Process \
			--id_process=process_$(record_unique_string) \
			--some_user=user_$USER \
			--working_dir=$PWD \
			--host="$id_computer" \
            		--start_time=$(date "+%Y%m%dT%H%M%S")  \
		$EXEC $@ \
        ) || exit -1

	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$id_process"
}

record_application() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	# $1 - executable or application_id
	# Free form except for --instance  which gets deleted as a prefix and
	# used to update the box and --model which is also deleted and
	# used to update the model entry.

    id_application="$1"
    id_box=
	APP=$(which "$id_application" 2>/dev/null)
    if [[ $(record-exists.py --table=Application --id_application="$id_application") == "True" ]]
    then
		id_box=$(record-get-value.py \
			--table=Application \
			--id_application="$id_application" \
			--location \
		) || exit -1
        APP=$(_get_executable $id_application)
   	elif [[ -z "$APP" || ! -f "$APP" ]]
	then
        APP=$(which $(_parent_script))
        id_application=application_$(cksum $(which $APP) | awk '{print $1}') 
        id_box=box_$(cksum $(which $APP) | awk '{print $1}') 
 	else
        id_application=application_$(cksum $(which $APP) | awk '{print $1}') 
        id_box=box_$(cksum $(which $APP) | awk '{print $1}') 
		shift
	fi

    id_box_type=
    if [[ $(file -L $(which $APP)) == *Bourne-Again* ]]
    then
        id_box_type="$id_box_bash"
        LANGUAGE="Bash"
    elif [[ $(file -L $(which $APP)) == *Perl* ]]
    then
        id_box_type="$id_box_perl"
        LANGUAGE="Perl"
    elif  [[ $(file -L $(which $APP)) == *Rscript* ]] || grep -q "\.R$" "$APP"
    then
        id_box_type="$id_box_R" 
        LANGUAGE="R"
    elif  [[ $(file -L $(which $APP)) == *"ELF 64"* ]]
    then
        id_box_type="$id_box_elf"
        LANGUAGE="Unknown"
    else
        (>&2 echo "BASH: $FUNCNAME $@: Trying to call a script $APP we recognise "$(file -L $(which $APP)))
    fi
    [ -n "$id_box_type" ] || exit -1

    PARAMS=("$@")

	id_model=
    INSTANCE=
    for i in "${!PARAMS[@]}"
    do
        if [[ "${PARAMS[i]}" == *--model=* ]]
        then	
            MODEL=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            id_model=$(record-update.py \
                --table=Model\
                --id_model=$MODEL
            ) || exit -1
        elif [[ "${PARAMS[i]}" == *--instance=* ]]
        then
            INSTANCE=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            unset "PARAMS[i]"
        fi
    done

	id_box=$(record-update.py \
		--table=Box \
		--id_box="$id_box" \
		--location_value=$(which $APP) \
		--location_type=local \
        --instance="$id_box_type" \
		--encoding=$(file -L -b --mime-encoding $(which $APP)) \
		--size=$(stat --printf="%s" $(which $APP)) \
		--modification_time=$(stat --printf="%y" $(which $APP) | \
			sed "s/://g" | \
			sed "s/-//g" | \
			sed "s/ /T/" | \
			cut -b1-15 ) \
		--update_time=$(stat --printf="%z" $(which $APP) | \
			sed "s/://g" | \
			sed "s/-//g" | \
			sed "s/ /T/" | \
			cut -b1-15 ) \
		--hash=$(cksum $(which $APP) | cut -f 1 -d' ') \
		$INSTANCE \
	    $GENERATED_BY \
	) || exit -1

	id_app=$(record-update.py \
		--table=Application \
		--id_application="$id_application" \
		--location="$id_box" \
        --language=$LANGUAGE \
        --name=$(basename $APP) \
		"$PARAMS[@]" \
	) || exit -1

	id_box=$(record-update.py \
		--table=Box \
		--id_box="$id_box" \
		--location_application="$id_app" \
	) || exit -1

    # Lastly set up a pipeline if this needs it.
    
    id_pipeline=$(record-update.py \
        --table=Pipeline \
        --id_pipeline="pipeline_${id_app}" \
        --calls="$id_app" \
    ) || exit -1

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    echo $id_app
}

_get_executable() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME ($1): entering...")
	id_application=
	if [ -z "$1" ] || [[ "$1" =~ ^\-\-  ]]
    then
        id_application=$(which $(_parent_script))
    else
        id_application="$1"
        shift
    fi 

	executable=
	if [[ $(record-exists.py --table=Application --id_application=$id_application)  = True ]]
	then
		id_box=$(record-get-value.py \
			--table=Application \
			--id_application="$id_application" \
			--location \
		) || exit -1
		executable=$(record-get-value.py \
			--table=Box \
			--id_box="$id_box" \
			--location_value \
		) || exit -1

	elif [ -x $(which $id_application) ]
    then  
        PARAMS=("$@")
        for i in "${!PARAMS[@]}"
        do
            if [[ "${PARAMS[i]}" == *--record-argument-* ]]
            then
                unset 'PARAMS[i]'
            fi
        done
		executable=$id_application
		id_application=$(record_application \
			$id_application \
			"$PARAMS[@]" \
		) || exit -1
	else
		(>&2 echo "BASH: $FUNCNAME $@: Application $id_application does not exist")
		exit -1
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME ($1): ...exit.")
	echo $executable
}

record_block() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    if [ -n "$RECORD_SLURM" ]
    then
        while (( $(squeue -u $USER --format="%.18i %.9P %.30j %.8u %.2t %.10M %.6D %R" | grep $RECORD_SLURM_PREFIX | grep -v JOBID | wc -l) > 0 ))
        do
            [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: $(date): sleeping because sbatch has not finished...")
            sleep $RECORD_SLEEP
        done
    else
        if [ -n "$1" ]
        then
            THIS_SCRIPT=$(_get_executable $1) || exit -1
        else
            THIS_SCRIPT=$0
        fi
        instances=$(_get_instances $THIS_SCRIPT) || exit -1
        [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: There are $instances running of $THIS_SCRIPT.")
        while [ $instances -ge $RECORD_MAX_PROCESSES ]
        do
            [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: Only have $RECORD_MAX_PROCESSES processes and $instances are running of $THIS_SCRIPT, so blocking...")
            sleep $RECORD_SLEEP
            instances=$(_get_instances $THIS_SCRIPT)
        done
    fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_run() {
    [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

    PARAMS=($@)

    # If we have more than RECORD_SLURM_MAX_SBATCH_CHARS in the parameter string, then it
    # is passed as a file. We now process this. Remember the upper limit is
    # done using `getconf ARG_MAX`. This is currently reporting just over
    # 2,000,000 on the cluster.

    parameter_file=
    for i in "${!PARAMS[@]}"
    do
        if [[ "${PARAMS[i]}" == *--parameters* ]]
        then
            parameter_file=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            if [ ! -f "$parameter_file" ]
            then
                (>&2 echo "BASH: $FUNCNAME $@: no such file: $parameter_file.")
                exit -1
            fi
            mapfile -O "${#PARAMS[@]}" -t PARAMS < "$parameter_file"
            unset 'PARAMS[i]'
            break
        fi
    done
    CWD=
    batch_invoked_by=
    MODIFIED_PARAMS=()
    for i in "${!PARAMS[@]}"
    do
        if [[ "${PARAMS[i]}" == *--cwd* ]]
        then	
            CWD=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            if [ ! -d "$CWD" ]
            then
                mkdir "$CWD"
            fi
            unset 'PARAMS[i]'
        elif [[ "${PARAMS[i]}"  == *--batch_invoked_by* ]]
        then
            batch_invoked_by=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            unset 'PARAMS[i]'
        elif [[ "${PARAMS[i]}"  == *--dependency=* ]]
        then
            # This is for something that must be run before this part can
            # be run. For instance we may have some post processing to be
            # done, or pre-processing. We need some way of determing
            # whether this has been run. I think we we will have to look
            # through the database looking to see if there is a record of
            # the dependency have been executed successfully this time.

            DEPENDENCY=$(echo "${PARAMS[i]}" | cut -f2 -d=)
            id_call_application=$(record_application $DEPENDENCY \
                --instance=$(which $DEPENDENCY) \
            ) || exit -1
            [ -n "$id_call_application" ] || exit -1
            
            id_dependency=$(record-update.py \
                --table=Dependency \
                --dependant="$id_application" \
                --dependency="$id_call_application" \
                --optionality=required \
            ) || exit -1
            unset 'PARAMS[i]'
            [ -n "$id_dependency" ] || exit -1
        elif  [[ "${PARAMS[i]}"  == *--record-* ]]
        then
            continue
        else
            MODIFIED_PARAMS+=("${PARAMS[i]}")
        fi
    done

    # The reasoning behind the next two lines is that the argument may be
    # an id_application or a path may be passed as the first argument
    

    APP=$(_get_executable "$MODIFIED_PARAMS")
    id_application=$(record_application "$MODIFIED_PARAMS")

    invoking_application=application_$(cksum $(_parent_script) | awk '{print $1}')

    # Arguably all this could be done from with the the thing that is being
    # called here, i.e. at a level lower than this (and we may do this later),
    # but for now we are going to assume that the thing being called has no
    # provenance primitives and we are having to do this external to the
    # script. It makes the coding slightly awkward but leaves a lot of room for
    # speed improvement at a later date. This means the primitives could be
    # embedeed in Perl, R, NetLogo, and elf exectuables. I will put this
    # comment everywhere where we stoop to do provenance at a level higher than
    # it should. I am doing this because this got very confused in my head to
    # start with. To be clear, provenance for a bunch of code should explicitly
    # be done by that code if at all possible.						

    proper_args=
    declare -A argument_value
    position_arg=()
    for arg in "${PARAMS[@]}"
    do
        if [[ "$arg" == *--record-argument-* ]]
        then
            if [[ "$arg" == *=* ]]
            then
                id_arg=$(echo "$arg" | cut -f1 -d= | sed 's/--record-argument-//')
                value=$(echo "$arg" | cut -f2 -d=)
                pos=$(record-get-value.py \
                    --table=Argument \
                    --application="$id_application" \
                    --id_argument="$id_arg" \
                    --order_value \
                ) || exit -1
                if [[ $pos = 'None' ]]
                then
                    name=$(record-get-value.py \
                        --table=Argument \
                        --application="$id_application" \
                        --id_argument="$id_arg" \
                        --name) || exit -1
                    separator=$(record-get-value.py \
                        --table=Argument \
                        --application="$id_application" \
                        --id_argument="$id_arg" \
                        --separator) || exit -1
                    [ -n "$separator" ] || exit -1
                    if [[ "$separator" == "None" ]]
                    then
                        separator="--"
                    fi
                    assignment_operator=$(record-get-value.py \
                        --table=Argument \
                        --application="$id_application" \
                        --id_argument="$id_arg" \
                        --assignment_operator \
                    ) || exit -1
                    if [[ $assignment_operator == "equal" ]]
                    then
                        assignment_operator="="
                    elif [[ $assignment_operator == "space" ]]
                    then
                        assignment_operator=" "
                    elif [[ $assignment_operator == "None" ]]
                    then
                        assignment_operator=" "
                    fi
                    proper_args="$proper_args ${separator}${name}${assignment_operator}$value"
                else
                    arity=$(record-get-value.py \
                        --table=Argument \
                        --application="$id_application" \
                        --id_argument="$id_arg" \
                        --arity\
                    ) || exit -1
                    argsep=$(record-get-value.py \
                        --table=Argument \
                        --application="$id_application" \
                        --id_argument="$id_arg" \
                        --argsep \
                    ) || exit -1
                    if ( [[ $arity == "+" ]] || (( $arity > 1 )) ) && [[ "$argsep" == "space" ]] 
                    then
                        value=$(echo "$arg" | cut -d= -f2)
                    fi
                    if [[ $arity != "+" ]] && (( $arity > 1 )) 
                    then
                        if [[ $argsep == "space" ]]
                        then
                            argsep=' '
                        fi
                        actual_nof_args=$(( $(echo $value | grep -o "$argsep" | wc -l) + 1 ))
                        if (( $actual_nof_args != $arity ))
                        then
                            (>&2 echo "BASH: $FUNCNAME $@: Trying to call a script $APP with wrong number of arguments in $id_arg. Asked for $arity, got $actual_nof_args")
                            exit -1
                        fi
                    fi
                    position_arg[$pos]=$value
                fi
                argument_value[$id_arg]=$value
            else
                id_arg=$(echo "$arg" | cut -f1 -d= | sed 's/--record-argument-//')
                name=$(record-get-value.py \
                    --table=Argument \
                    --application="$id_application" \
                    --id_argument="$id_arg" \
                    --name
                ) || exit -1 
                separator=$(record-get-value.py \
                    --table=Argument \
                    --application="$id_application" \
                    --id_argument="$id_arg" \
                    --separator\
                ) || exit -1
                if [[ "$separator" == "None" ]]
                then
                    separator="--"
                fi
                proper_args="$proper_args ${separator}${name}"
                argument_value[$id_arg]='True'
            fi
        fi
    done
    
    # This is a pipeline dependency

    invoking_application=application_$(cksum $(_parent_script) | awk '{print $1}')
    if [[ $(record-exists.py --table=Application --id_application=$invoking_application) == "True" ]] 
    then
        id_dependency=$(record-update.py \
            --table=Dependency \
            --dependant="$id_application" \
            --dependency=$invoking_application \
            --optionality=required \
        ) || exit -1
    fi
 
    THIS_PROCESS=$(_process \
        --executable="$id_application" \
    )

    if [ -n "$CWD" ]
    then
        cd "$CWD"
    fi
    for id in "${!argument_value[@]}"
    do
        [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME: Blocking _argument_value $THIS_PROCESS $id ${argument_value[$id]}")
        _argument_value $THIS_PROCESS $id ${argument_value[$id]}
    done

    stdout=
    stderr=

    for arg in "${PARAMS[@]}"
    do
        running=0
        if [[ "$arg" == *--record-input-* ]]
        then
            input_type_id=$(echo "$arg" | cut -f1 -d= | sed 's/--record-input-//')
            value=$(echo "$arg" | cut -f2 -d=)
            if [ -n "$RECORD_SLURM_HEAD_NODE" ] && [ $(hostname) != "$RECORD_SLURM_HEAD_NODE" ]
            then

                _input_value "$id_application" "$THIS_PROCESS" "$input_type_id" "$value" &
                ((running++))

                if (( running >= $RECORD_MAX_PROCESSES ))
                then
                    [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME: Waiting to for _input_value to complete")
                    wait -n          # Wait for one job to finish
                    ((running--))
                fi

            else
                _input_value $id_application $THIS_PROCESS $input_type_id $value
            fi
        elif [[ "$arg" == *--record-extend-stdout-* ]]
        then
            value=$(echo "$arg" | cut -f2 -d=)
            stdout=' >>'"$value"
        elif [[ "$arg" == *--record-stdout-* ]]
        then
            value=$(echo "$arg" | cut -f2 -d=)
            stdout=' >'"$value"
        elif [[ "$arg" == *--record-stderr-* ]]
        then
            value=$(echo "$arg" | cut -f2 -d=)
            stderr=' 2>'"$value"
        fi
    done

    wait

    # So this leaves the problem of the invoking program, how do we initially
    # populate the pipelines table?

    if [ -n "$batch_invoked_by" ]
    then
        id_pipeline=$(record-update.py \
            --table=Pipeline \
            --id_pipeline=pipeline_${id_application} \
            --calls="$id_application" \
            --previous=pipeline_${batch_invoked_by}
         ) || exit -1
    elif [ "$(record_called_by)" = "" ]
    then
        id_pipeline=$(record-update.py \
            --table=Pipeline \
            --id_pipeline=pipeline_${id_application} \
            --calls="$id_application" \
         ) || exit -1
    else
        id_pipeline=$(record-update.py \
            --table=Pipeline \
            --id_pipeline=pipeline_${id_application} \
            --calls="$id_application" \
            --previous=pipeline_${invoking_application}
         ) || exit -1
    fi

    [ -n "$DEBUG" ] && (>&2 echo CWD: $PWD)
    if [ ! -x "$APP" ]
    then
        (>&2 echo "APP: $APP does not exist")
        exit -1
    fi
    [ -n "$DEBUG" ] && (>&2 echo RUNNING: $APP $proper_args ${position_arg[*]} $stdout $stderr)

    eval $APP $proper_args ${position_arg[*]} $stdout $stderr 
    SYS=$?
    if [ $SYS -ne 0 ]
    then
        exit -1
    else
        if [ -n "$parameter_file" ] && [ -f "$parameter_file" ]
        then
            rm "$parameter_file"
        fi
    fi

    for arg in "${PARAMS[@]}"
    do
        if 	[[ "$arg" == *--record-output-* ]] || \
            [[ "$arg" == *--record-extend-stdout-* ]] || \
            [[ "$arg" == *--record-stdout-* ]] || \
            [[ "$arg" == *--record-stderr-* ]]
        then
            value=$(echo $arg | cut -f2 -d=)
            output_type_id=$(echo $arg | cut -f1 -d= | \
                sed 's/--record-output-//' | \
                sed 's/--record-stderr-//' | \
                sed 's/--record-extend-stdout-//' | \
                sed 's/--record-stdout-//')
            _output_value $THIS_PROCESS $output_type_id $value
        fi
    done

    THIS_PROCESS=$(_process \
        --id_process=$THIS_PROCESS \
        --executable="$id_application" \
        --end_time=$(date "+%Y%m%dT%H%M%S") \
    ) || exit -1

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_batch() {

    # Be aware if a job fails in sbatch, there is currently no way of checking
    # whether the job has worked or failed, other than inspecting the ouput
    # logs, or running something like:
    
    # sacct -u $USER --starttime=$(date -d '7 days ago' +%Y-%m-%d) | grep FAILED
    
    # And then inspecting the logs for that run. This code will pick it up, if
    # an input is missing, but ONLY IF the depenedent code is also not being
    # sbatch'ed, otherwise the code will blithely continue.

    # It would make sense to some something dependent upon all inputs in the
    # top, controlling script (because this would bail if a file were missing),
    # but, unfortunately, we are trying to reduce loading the head-node.

    if [ -n "$RECORD_SLURM_LIMIT" ]
    then

        nof_running=$(squeue --user $USER | grep $RECORD_SLURM_PREFIX | wc -l) 
        if [ $nof_running -gt $RECORD_SLURM_LIMIT ]
        then 
            (>&2 echo "BASH: $FUNCNAME $@: There are $nof_running jobs queued or running. This is limited to $RECORD_SLURM_PREFIX. Sleep for 60s...")
            sleep 60
        fi
    fi
    [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    EXTRA=
    if [[ "$PARAMS[@]" == *--wait_for=* ]]
    then
        for PARAM in "$PARAMS"
        do
            EXTRA=$EXTRA":"$(echo "$PARAM" | egrep -s "wait\_for=" | \
                sed "s/^.*--wait_for=\([^ ][^ ]*\).*$/\1/")

        done
        PARAMS=$(echo "$PARAMS" | egrep -s "wait_for=" | \
            sed "s/--wait_for=[^ ][^ ]* *//g")
        EXTRA="--dependency=afterany:$EXTRA"
    fi	    
    batch_invoked_by=$(record_application) || exit -1 
    OTHER="--batch_invoked_by=$batch_invoked_by"
    if [[ -n "$RECORD_SLURM" ]]
    then
        name=${RECORD_SLURM_PREFIX}_$(record_unique_string)
        IFS=" "
        count_the_length_of_args="$*"
        [ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: RUNNING sbatch nof args = ${#count_the_length_of_args}")
        if (( ${#count_the_length_of_args} > $RECORD_SLURM_SBATCH_MAX_CHARS ))
        then
            parameter_file="$RECORD_TMPDIR"/"$name".parameters
            echo $@ | sed 's/  */\n/g' > "$parameter_file"
            mkdir slurm-outputs 2>/dev/null
            [ -n "$DEBUG" ] && (>&2 echo;echo;echo "BASH: $FUNCNAME $@: RUNNING sbatch --export=ALL,TMPDIR=/tmp -o ./slurm-outputs/slurm-%j.out --job-name=${name} $EXTRA record-run.sh --parameters="$parameter_file"; echo;echo;echo")
            sbatch --export=ALL,TMPDIR=/tmp -o ./slurm-outputs/slurm-%j.out --job-name="$name" $EXTRA record-run.sh --parameters="$parameter_file" "$OTHER"
            if [ $? -ne 0 ]
            then
                (>&2 echo "BASH: $FUNCNAME $@: SBATCH just failed.")
                exit -1
            fi
        else
            [ -n "$DEBUG" ] && (>&2 echo;echo;echo "BASH: $FUNCNAME $@: RUNNING sbatch --export=ALL,TMPDIR=/tmp -o ./slurm-outputs/slurm-%j.out --job-name=${name} $EXTRA record-run.sh $@; echo;echo;echo")
            mkdir slurm-outputs 2>/dev/null
            sbatch --export=ALL,TMPDIR=/tmp -o ./slurm-outputs/slurm-%j.out --job-name="$name" $EXTRA record-run.sh $@ "$OTHER"
        fi
        unset IFS
    else
        # Do our own scheduling...
        record_block 
        record_run "$@" "$OTHER" &
        record_block 
    fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_argument_type() {
	# $1 - application_id
	# $2 - id_argument
	# $@ - the rest
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_application="$1"
	shift
	id_argument="$1"
	shift
	id_argument=$(record-update.py \
		--table=Argument \
		--id_argument="$id_argument" \
		--application="$id_application" \
		$@ \
	) || exit -1	
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_argument
}

_argument_value() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_argument_value=$(record-update.py \
		--table=ArgumentValue \
		--for_process="$1" \
		--for_argument="$2" \
		--has_value="$3" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
}

record_output_box_type() {

	# $1 - id_application
	# $2 - box_type_name
    # $3 - file-pattern (regex of the file name)
    # $4 - locator_for_output_box_type (must fit the regex '^(stdout|stderr|arg=[0-9]+|argid=.+|opt=.+|env=.+|in_file=.+)$')

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

    id_output_box_type=$(record-update.py \
        --table=BoxType \
        --id_box_type="$2" \
        --format='text/plain' \
        --identifier="name:$3" \
    ) || exit -1

    extra_args=
    locator="$4"
    if [[ "$locator" =~ ^in_file=.* ]]
    then
        box=$(echo "$4" | sed 's/in_file\=//')
        locator="in_file"
        if [[ $(record-exists.py --table=Box --id_box=$box) == True ]]
        then
            extra_args="--in_file=$box"
        else 
            (>&2 echo "BASH: $FUNCNAME $@: the box $box for box type $2 does not exist.")
            exit -1
        fi
    fi
    id_product=$(record-update.py \
        --table=Product \
        --application="$1" \
        --box_type="$id_output_box_type" \
        --optionality=always \
        --locator=$locator $extra_args
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    echo $id_output_box_type
}

_output_value() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
 
	# $1 - process_id - specifically output of
	# $2 - box_type_id - type of output
	# $3 - path to object

	if [ ! -e $3 ]
	then
		(>&2 echo "BASH: $FUNCNAME $@: Something wrong in the call \"--record-\(output|stdout|stderr|extend-stdout\)-$2=$3\": $3 does not exist")
		exit -1 
	fi

	id_box=
	if [ -d $3 ]
	then
		id_box=$(record-update.py \
			--table=Box \
			--id_box=box_$(cksum "$3" | awk '{print $1}') \
			--location_value=$(readlink -f "$3") \
			--location_type=local \
            --instance="$2" \
			--encoding=$(file -L -b --mime-encoding "$3") \
			--size=4096 \
			--modification_time=$(stat --printf="%y" "$3" | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--update_time=$(stat --printf="%z" "$3" | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--output_of="$1" \
			--instance="$2" \
			$GENERATED_BY \
		) || exit -1
	else	
		id_box=$(record-update.py \
			--table=Box \
			--id_box=box_$(cksum "$3" | awk '{print $1}') \
			--location_value=$(readlink -f "$3") \
			--location_type=local \
            --instance="$2" \
			--encoding=$(file -L -b --mime-encoding "$3") \
			--size=$(stat --printf="%s" "$3") \
			--modification_time=$(stat --printf="%y" "$3" | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--update_time=$(stat --printf="%z" "$3" | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--hash=$(cksum "$3" | cut -f 1 -d' ') \
			--output_of="$1" \
			--instance="$2" \
			$GENERATED_BY \
		) || exit -1
	fi

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}
	
record_input_box_type() {
  
	# $1 - id_application
	# $2 - input_box_type_name
    # $3 - file-pattern_for_input_container_type (regex of the file name)
    # $4 - locator_for_input_box_type (must fit the regex '^(stdout|stderr|arg=[0-9]+|argid=.+|opt=.+|env=.+|in_file=.+)$')

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

    id_input_box_type=$(record-update.py \
        --table=BoxType \
        --id_box_type="$2" \
        --format='text/plain' \
        --identifier="name:$3" \
    ) || exit -1

    extra_args=
    locator="$4"
    if [[ "$locator" =~ ^in_file=.* ]]
    then
        locator="in_file"
        box=$(echo "$4" | sed 's/in_file=//')
        if [[ $(record-exists.py --table=Box --id_box=$box) == True ]]
        then
            extra_args="--in_file=$box"
        else 
            (>&2 echo "BASH: $FUNCNAME $@: the box for the input box type $box does not exist.")
            exit -1
        fi
    fi
    id_product=$(record-update.py \
        --table=Product \
        --application=$1 \
        --box_type="$id_input_box_type" \
        --optionality=always \
        --locator=$locator $extra_args
    ) || exit -1 	
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    echo $id_input_box_type
}

_input_value() {

	# $1 - id_application
	# $2 - id_process
	# $3 - id_box_type
	# $4 - path to object

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	if [ ! -e $4 ]
	then
		(>&2 echo "BASH: $FUNCNAME $@: Something seriously wrong in the call \"--record-input-$id_box_type="$4"\": $4 does not exist")
		exit -1 
	fi

	id_box=
	if [ -d $4 ]
	then
		id_box=$(record-update.py \
			--table=Box \
			--id_box=box_$(cksum $4 | awk '{print $1}') \
			--location_value=$(readlink -f $4) \
			--location_type=local \
            --instance="$3" \
			--location_application="$1" \
			--encoding=$(file -L -b --mime-encoding $4) \
			--size=4096 \
			--modification_time=$(stat --printf="%y" $4 | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--update_time=$(stat --printf="%z" $4 | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--instance="$3" \
			$GENERATED_BY \
		) || exit -1
	else	
		id_box=$(record-update.py \
			--table=Box \
			--id_box=box_$(cksum $4 | awk '{print $1}') \
			--location_value=$(readlink -f $4) \
			--location_type="local" \
            --instance="$3" \
			--location_application="$1" \
			--encoding=$(file -L -b --mime-encoding $4) \
			--size=$(stat --printf="%s" $4) \
			--modification_time=$(stat --printf="%y" $4 | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--update_time=$(stat --printf="%z" $4 | \
				sed "s/://g" | \
				sed "s/-//g" | \
				sed "s/ /T/" | \
				cut -b1-15 ) \
			--hash=$(cksum $4 | cut -f 1 -d' ') \
			--instance="$3" \
			$GENERATED_BY \
	    ) || exit -1
			
	fi
	

    id_input=$(record-update.py \
        --table=Input \
        --process="$2" \
        --box="$id_box" \
        --usage=data \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}
record_project() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    project="$1"
    shift
	id_project=$(record-update.py \
		--table=Project \
        --id_project=$project \
		$@
	) || exit -1	
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_project
}
record_study() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    study="$1"
    part="$2"
    shift 2
    if [[ "$study" == "$part" ]]
    then
        # We have a top level study
        id_study=$(record-update.py \
            --table=Study \
            --id_study=$study \
            $@ \
        ) || exit -1
    else
        id_study=$(record-update.py \
            --table=Study \
            --id_study=$study \
            --part=$part \
            $@ \
        ) || exit -1
    fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_study
}
record_set() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	# You would think that this should be done in the function above.
	# However the script above is called by command substitution, which is
	# a subprocess. A subprocess for which all environment variables are
	# wiped out, as soon as it terminates. So we have to do this directly.
	STANDARD_ARGS=
	while [[ $# -gt 0 ]]; do
		case $1 in
			--study*) 
				STUDY=$(echo $1 | sed 's/\-\-study=//')
				export record_STUDY=$STUDY
				export GENERATED_BY=--generated_by=$record_STUDY
				shift;;
	       --model*) 
				export STANDARD_ARGS="$STANDARD_ARGS $1"
				shift;;
           --licence*) 
				export STANDARD_ARGS="$STANDARD_ARGS $1"
				shift;;
			--version*) 
				export STANDARD_ARGS="$STANDARD_ARGS $1"
				shift;;
		esac
	done
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}
record_involvement() {

    # $1 - Study
    # $2 - Person
    # $3 - Role

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    id_involvement=$(record-update.py \
        --table=Involvement \
        --study="$1" \
        --person="$2" \
        --role="$3" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}
record_paper() {

    # $1 - path to document
    # $2 - held by - person ID
    # £3 - sourced_from - person ID
    # $4 - study ID
    # $5 - date of publishing

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	DOC="$1"
    # So if the first argument does not exist
	if [[ ! -f "$DOC" ]]
	then
        (>&2 echo "BASH: Paper $DOC does not exist.")
	    exit -1
	fi
	sourced_from="$2"
	held_by="$3"
	describes="$4"
	date="$5"

	id_paper_box_type=$(record-update.py \
		--table=BoxType \
		--id_box_type=box_type_paper \
		--description="Published or draft paper" \
		--format='application/pdf;application/msword' \
		--identifier=magic:'^.*Microsoft Word*$;magic:^.*PDF Document.*$' \
	) || exit -1

	id_box=$(record-update.py \
		--table=Box \
		--id_box=box_$(cksum "$DOC" | awk '{print $1}') \
		--location_value=$(readlink -f "$DOC") \
		--held_by=$held_by \
	    	--sourced_from=$sourced_from \
		--location_type="local" \
		--encoding=$(file -L -b --mime-encoding "$DOC") \
		--size=$(stat --printf="%s" "$DOC") \
		--modification_time=$(stat --printf="%y" "$DOC" | \
			sed "s/://g" | \
			sed "s/-//g" | \
			sed "s/ /T/" | \
			cut -b1-15 ) \
		--update_time=$(stat --printf="%z" "$DOC" | \
			sed "s/://g" | \
			sed "s/-//g" | \
			sed "s/ /T/" | \
			cut -b1-15 ) \
		--hash=$(cksum "$DOC" | cut -f 1 -d' ') \
		--instance="$id_paper_box_type" \
		$GENERATED_BY \
	) || exit -1
	

	id_paper=$(record-update.py \
		--table=Documentation \
		--id_documentation="documentation.$DOC" \
		--title=$(basename "$DOC") \
		--describes=$describes \
	) || exit -1
		#--date=$date \
		#--location="$id_box" \

	id_box=$(record-update.py \
		--table=Box \
		--id_box="$id_box" \
		--location_type="local" \
		--location_value=$(readlink -f "$DOC") \
		--location_documentation="$id_paper" \
	) || exit -1

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_paper

}
record_make_tag() {

    # $1 - tag ID
    # $2 - description

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_tag=$(record-update.py \
		--table=Tag \
		--id_tag="$1" \
		--description="$2" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_tag
}

record_tag() {

    # $1 - tag ID
    # $2 - target
   
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    if [ $# -ne 2 ]
    then
        (>&2 echo "BASH: $FUNCNAME $@: incorrect number of arguments $# should be 2")
        exit -2
    fi
    id_tag_map=$(record-update.py \
        --table=TagMap \
        --tag="$1" \
        "$2"
    ) || exit -1
    
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_contributor() {

	# $1 - id_application
	# $2 - contributor
	# $3 - type of contribution

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_contributor="$2"
	if [[ $(record-exists.py --table=Person --id_person=$2) != True ]]
	then
		id_contributor=$(record-update.py \
			--table=Person \
			--email=$(grep "$2" "$RECORD_USER_FILE" 2>/dev/null | cut  -f3 -d,) \
			--id_person="$2" \
			--name="$2" \
		) || exit -1
	fi
	if [[ $(record-exists.py --table=Application --id_application="$1") == True ]]
	then
		id_contributor=$(record-update.py \
			--table=Contributor \
			--application="$1" \
			--contributor="$id_contributor" \
			--contribution="$3" \
		) || exit -1
	elif [[ $(record-exists.py --table=Box --id_box="$1") == True ]]
	then
        id_contributor=$(record-update.py \
            --table=Contributor \
            --box="$1" \
            --contributor="$id_contributor" \
            --contribution="$3" \
        ) || exit -1 
	elif [[ $(record-exists.py --table=Documentation --id_documentation="$1") == True ]]
	then
		id_contributor=$(record-update.py \
			--table=Contributor \
			--documentation="$1" \
			--contributor="$id_contributor" \
			--contribution="$3" \
		) || exit -1
	else
		(>&2 echo "BASH: $FUNCNAME $@: $1 neither application nor box")
		exit -1
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_statistical_method() {

    # $1 - statistical_method ID
    # $2 - description.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_statistical_method=$(record-update.py \
		--table=StatisticalMethod \
		--id_statistical_method="$1" \
		--description="$2" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$id_statistical_method"
}

record_visualisation_method() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_visualisation_method=$(record-update.py \
		--table=VisualisationMethod \
		--id_visualisation_method="$1" \
		--description="$2" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$id_visualisation_method"
}

record_statistics() {

	# A set of statistics

	# $1 - id for this statistic
	# $2 - id for the statistical method
	# $3 - query used to produce the statistics

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_statistics=$(record-update.py \
		--table="Statistics" \
		--id_statistics="$1" \
		--date=$(date "+%Y%m%dT%H%M%S") \
		--used="$2" \
		--query="$3" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_statistics
}
record_visualisation() {

	# $1 - id_visualisation
	# $2 - method - points at VisualisationMethod
	# $3 - the means by  which the visualisation is produced
	# $4 - the box for the visualisation

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	if [ -z "$4" ] || [ ! -f "$4" ]
	then
		(>&2 echo "BASH: $FUNCNAME $@: Unable to find $4")
		exit -1
	fi
	id_box=box_$(cksum $4 | awk '{print $1}')

	# The previous few lines are a real hack. This needs to be done better.
	# These objects should be returned as part of the _run() method. Using
	# the cksum is contrived IPC, i.e. the spawned process in _run()
	# talking to the calling process. This will "always" work, but it is
	# invisible to the coder and can easily be missed and thus broken in
	# future releases.  Hmmmmm, need to think about this, but for now we
	# will hack.

	id_visualisation=$(record-update.py \
		--table="Visualisation" \
		--id_visualisation="$1" \
		--date=$(date "+%Y%m%dT%H%M%S") \
		--visualisation_method="$2" \
		--query="$3" \
		--contained_in="$id_box" \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_visualisation
}

record_implements() {

    # $1 - Application ID
    # $2 - StatisticalMethod or VisualisationMethod 

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    id_implements=$(record-update.py \
        --table=Implements \
        --application="$1" \
        $2 \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
}

record_parameter() {

    # $1 - parameter id
    # $2 - description
    # $3 - data type
    
    # $@ - optional parameters

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_parameter=$(record-update.py \
		--table=Parameter \
		--id_parameter="$1" \
		--description="$2" \
		--data_type="$3" \
		$@ \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_parameter
}
record_statistical_variable() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

	# $1 - id_statistical_variable
    # $2 - Description
    # $3 - data type	
	# $4 - generated_by statistical method

	id_statistical_variable=$(record-update.py \
		--table=StatisticalVariable \
		--id_statistical_variable="$1" \
		--description="$2" \
		--data_type="$3" \
		--statistic_generated_by="$4" \
	) || exit -1
    id_employs=$(record-update.py \
        --table=Employs \
        --statistical_variable="$id_statistical_variable" \
        --statistical_method="$4" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_statistical_variable
}
record_visualisation_variable() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

	# $1 - id_visualisation_variable
    # $2 - Description
    # $3 - data type	
	# $4 - generated_by visualistion method

	id_statistical_variable=$(record-update.py \
		--table=StatisticalVariable \
		--id_statistical_variable="$1" \
		--description="$2" \
		--data_type="$3" \
		--visualisation_generated_by="$4" \
	) || exit -1
    id_employs=$(record-update.py \
        --table=Employs \
        --statistical_variable="$id_statistical_variable" \
        --visualisation_method="$4" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_statistical_variable
}

record_variable() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

	# $1 - id_variable
	# $2 - description
	# $3 - data_type

	# So a variable may be one of:

	# * Argument
	# * Assumes
	# * Content
	# * Value

	extra=
	if [[ "$@" = *--link* ]]
	then 
		extra=--is_link=1
	elif [[ "$@" = *--space* ]]
	then 
		extra=--is_space=1
	elif [[ "$@" = *--time* ]]
	then 
		extra=--is_time=1
	elif [[ "$@" = *--agent* ]]
	then 
		extra=--is_agent=1
	fi
	id_variable=$(record-update.py \
		--table=Variable \
		--id_variable="$1" \
		--description="$2" \
		--data_type="$3" $extra \
	) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_variable
}
record_statistical_variable_value() {

    # A setter - no return.

	# $1 - value
	# $2 - id_statistical_variable
	# $3 - file/image/visualisation/db in which it resides (the box)
    # $4 - instance of statistics this refers to.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	val="$1"
	shift 
	id_variable="$1"
	shift
	if [ ! -f $1 ]
	then
		(>&2 echo "BASH: $FUNCNAME $@ Unable to find $1")
		exit -1
	fi
	id_box=box_$(cksum $1 | awk '{print $1}')
	shift

	# The last line is a real hack. This needs to be done better. These
	# objects should be returned as part of the _run() method. Using the
	# cksum is contrived IPC, i.e. the spawned process in _run() talking to
	# the calling process. This will "always" work, but it is invisible to
	# the coder and can easily be missed and thus broken in future
	# releases.  Hmmmmm, need to think about this, but for now we will
	# hack.

	id_value=$(record-update.py \
		--table=Value \
		--id_value=$val \
		--statistical_variable="$id_variable" \
		--contained_in="$id_box" \
        --result_of="$4" \
        $@ \
	) || exit -1

    # Now need to link this statistical variable to the value using StatisticalInput.
    
    id_statistical_input=$(record-update.py \
        --table=StatisticalInput \
        --value="$id_value" \
        --statistics="$4" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_visulisation_variable_value() {

    # A setter - no return.

	# $1 - value
	# $2 - id_visualisation_variable
	# $3 - visualisation in which it resides (the box)
    # $4 - instance of visualisation this refers to.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	val="$1"
	shift 
	id_value="$1"
	shift
	if [ ! -f $1 ]
	then
		(>&2 echo "BASH: $FUNCNAME $@ Unable to find $1")
		exit -1
	fi
	id_box=box_$(cksum $1 | awk '{print $1}')
	shift

	# The last line is a real hack. This needs to be done better. These
	# objects should be returned as part of the _run() method. Using the
	# cksum is contrived IPC, i.e. the spawned process in _run() talking to
	# the calling process. This will "always" work, but it is invisible to
	# the coder and can easily be missed and thus broken in future
	# releases.  Hmmmmm, need to think about this, but for now we will
	# hack.

	id_value=$(record-update.py \
		--table=Value \
		--id_value=$val \
		--visualisation_parameter="$id_variable" \
		--contained_in="$id_box" \
        --result_of="$4" \
        $@ \
	) || exit -1

    # Now need to link this statistical variable to the value using StatisticalInput.

    id_statistical_input=$(record-update.py \
        --table=StatisticalInput \
        --value="$id_value" \
        --visulisation="$4" \
    ) || exit -1
	
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_value() {

    # A setter - no return

	# $1 - value
	# $2 - id_value
	# $3 - file/imagedb in which it resides (the box)
	# Any other arguments to specify this more accurately.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	val="$1"
	shift 
	id_variable="$1"
	shift
	if [ ! -f $1 ]
	then
		(>&2 echo "BASH: $FUNCNAME $@ Unable to find $1")
		exit -1
	fi
	id_box=box_$(cksum $1 | awk '{print $1}')
	shift

	# The last line is a real hack. This needs to be done better. These
	# objects should be returned as part of the _run() method. Using the
	# cksum is contrived IPC, i.e. the spawned process in _run() talking to
	# the calling process. This will "always" work, but it is invisible to
	# the coder and can easily be missed and thus broken in future
	# releases.  Hmmmmm, need to think about this, but for now we will
	# hack.

	id_value=$(record-update.py \
		--table=Value \
		--id_value=$val \
		--variable="$id_variable" \
		--contained_in="$id_box" \
		$@
	) || exit -1
	
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}
record_content() {

    # $1 - source containing the content in $2 
    # $2 - boxtype of content

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    id_content=$(record-update.py \
        --table=Content \
        $@ \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo $id_content
}

record_person_makes_assumption() {

    person="$1"
    id_assumption="$2"
    description="$3"

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	id_assumption=$(record-update.py \
		--table=Assumption \
		--id_assumption="$id_assumption" \
		--description=$description \
	) || exit -1
   id_assumes=$(record-update.py \
        --table=Assumes \
        --person=$person \
        --assumption="$id_assumption" \
    ) || exit -1
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$id_assumption"
}

record_end() {
    # All the tidying up, but only if this is the last thing called.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    if [[ -n "$RECORD_SLURM" ]] && [[ "$1" = "--block" ]]
    then
        record_block
    fi
    if [ "$(record_called_by)" = "" ] 
    then
        (>&2 echo "BASH: $(_parent_script): $(date): SUCCESS SUCCESS SUCCESS")
        echo "BASH: $(_parent_script): $(date): SUCCESS SUCCESS SUCCESS"
        rm $RECORD_PID_FILE 2>/dev/null
    fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

record_start() {
    # All the initialisation, but only if this is the first thing called.

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    if [ "$(record_called_by)" = "" ] 
    then
        (>&2 echo "BASH: $(_parent_script): $(date): Started!")
        echo "BASH: $(_parent_script): $(date): Started!"
    fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    return 0
}

_ip_address() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	if [[ $(uname -o) == "Darwin" ]]
	then
		IP=$(/sbin/ifconfig en0 | sed -n "5p" | awk '{print $2}' |cut -f2 -d:)
	elif [[ $(uname -o) == "Cygwin" ]]
	then
		IP=$(ipconfig | grep "IPv4 Address" | head -1 | sed 's/^.*: //' | sed 's/\r//')
	else
		IP=$(ip address | grep -A 4 ' UP ' | grep 'inet ' | head -1 | awk '{print $2}')
		#IP=$(/sbin/ifconfig | sed -n "2p" | awk '{print $2}' |cut -f2 -d:)
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$IP"
}

_mac_address() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	MAC=
	if [[ $(uname -o) == "Darwin" ]]
	then
		MAC=$(/sbin/ifconfig en0 | sed -n "3p" | awk '{print $2}')
	elif [[ $(uname -o) == "Cygwin" ]]
	then
		MAC=$(ipconfig /all | grep -B 5 "IPv4 Address" | grep "Physical Address" | sed 's/^.*: //' | sed 's/-/:/g' | tr '[:upper:]' '[:lower:]' | sed 's/[\r\n]//g' | head -1)
	else
		MAC=$(ip address | grep -A 2 ' UP ' | grep link | awk '{print $2}' | head -1)
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$MAC"
}

_fqdn() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

	if hostname -f | grep -qs "\."
	then 
        response=$(hostname -f)
	elif [ -z "$(nslookup -host $(hostname) | grep ^Name | awk '{print $2}')" ]
	then
        response=$(hostname -f)
	else
        response=$(nslookup -host $(hostname) | grep ^Name | awk '{print $2}')
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    echo "$response"
}

_parent_script() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")

	# Should be able to do this in one line, but bash doesn't like it for
	# some reason

	ME=$BASHPID
	if [[ $(uname -o) = "Cygwin" ]]
	then
		BASH_PROB=$(cat /proc/$ME/cmdline | sed 's/\x0//g' | sed 's/^bash//')
	else
		BASH_PROB=$(ps -o args= $ME)
        if [[ "$BASH_PROB" = "-bash" ]]
        then
            # So it turns out this is an error. Something has been called
            # without the "#!" at the start of the script, which is sloppy and
            # the OS has no way of invoking it correctly. 
            (>&2 echo "BASH: $FUNCNAME $@: ERROR: The immediately calling script "\
                "is invoking Bash without a hash bang at the start. This is "\
                "poor practice and breaks this code. FIX IT!")
             exit -1
        fi
	fi

	if [[ "$BASH_PROB" == *-xv* ]]
	then
		RESULT=$(echo $BASH_PROB | awk '{print $3}') 
	elif [[ "$BASH_PROB" = *-zsh* ]]
	then
		RESULT=$0
	elif [[ "$BASH_PROB" = *_parent_script* ]]
	then
		RESULT=CLI
	elif  [[ $(uname -o) == "Cygwin" ]]
	then
		RESULT="$BASH_PROB"
	else
		RESULT=$(echo $BASH_PROB | awk '{print $2}') 
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$RESULT"
}

record_called_by() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
    PS=$(ps -h -o "%a" --width=512 $PPID)
    RESULT=$(echo "$PS" | awk '{print $2}')
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$RESULT"
   
}

record_unique_string() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	#cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1
    result=$(cat /dev/urandom | tr -dc '0-9' | fold -w 32 | head -n 1)
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
    echo "$result"
}

_getent() {

    # $1 - type of database, e.g. passwd
    # $2 - user or thing filtering on

	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	if [[ "$1" != "passwd" ]]
	then
		echo "This only works for 'passwd'"
		exit -1
	fi
	if [[ $(uname -o) == "Cygwin" ]]
	then
		/cygdrive/c/Windows/System32/whoami.exe /upn | sed 's/\r//g'
	elif [[ $(uname -o) == "Darwin" ]]
	then
		if [ -z "$2" ];
		then
			USERS=`dscl . list /Users | grep -v "^_"`
		else
			USERS="$2"
		fi
		for user in $USERS
		do
			result=`dscl . -read /Users/$user RecordName | \
				sed 's/RecordName: //g'`:*:`dscl . -read /Users/$user UniqueID | \
				sed 's/UniqueID: //g'`:`dscl . -read /Users/$user PrimaryGroupID | \
				sed 's/PrimaryGroupID: //g'`:`dscl . -read /Users/$user RealName | \
				sed -e 's/RealName://g' -e 's/^ //g' | \
				awk '{printf("%s", $0 (NR==1 ? "" : ""))}'`:/Users/$user:`dscl . -read /Users/$user UserShell | \
				sed 's/UserShell: //g'`
		done
	else
        result=$(getent passwd $2)
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$result"
}

disk_space() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	SPACE=
	if [[ $(uname -o) == "Darwin" ]]
	then
		SPACE=$(df -k . | tail -1 | awk '{print $4}' | sed 's/G$//')
	elif [[ $(uname -o) == "Cygwin" ]]
	then
		SPACE=$(df -k -h . | tail -1 | awk '{print $4}' | sed 's/G$//')
	else
        SPACE=$(df -k . | tail -1 | awk '{print $2}')
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$SPACE"
}

memory() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	MEM=
	if [[ $(uname -o) == "Darwin" ]]
	then
		MEM=$(echo $(sysctl hw.memsize | cut -f2 -d' ') / 1024 / 1024 / 1024 | bc)
	elif [[ $(uname -o) == "Cygwin" ]]
	then
		MEM=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')
	else
		MEM=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$MEM"
}
cpus() {
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: entering...")
	CPUS=
	if [[ $(uname -o) == "Darwin" ]]
	then
		CPUS=$(sysctl hw.ncpu | cut -f2 -d ' ')
	elif [[ $(uname -o) == "Cygwin" ]]
	then
		CPUS=$(($(cat /proc/cpuinfo | awk '/^processor/{print $3}' | tail -1) + 1))
	else
		CPUS=$(($(cat /proc/cpuinfo | awk '/^processor/{print $3}' | tail -1) + 1))
	fi
	[ -n "$DEBUG" ] && (>&2 echo "BASH: $FUNCNAME $@: ...exit.")
	echo "$CPUS"

}

_get_instances() {
    THIS_SCRIPT="$1"
    if [[ $(uname -o) == "Cygwin" ]]
    then
        instances=$(ps -af | awk '{$1=$2=$3=$4=$5=""; print $0}'| grep "$THIS_SCRIPT" | wc -l)
    elif [[ $(uname -o) == "Darwin" ]]
    then
        instances=$(ps -af | awk '{print $7}' | grep "$THIS_SCRIPT" | wc -l)
    else
        instances=$(ps -ef | grep "$THIS_SCRIPT" | grep -v grep | grep -v ps | wc -l)
        ps -ef | grep "$THIS_SCRIPT" >&2 
    fi
#        instances=$(( $(squeue -t RUNNING | grep $RECORD_SLURM_PREFIX | wc -l) - 1 ))
#        if [ -n "$RECORD_SLURM_PENDING_BLOCKS" ]
#        then
#            instances=$(($instances + $(( $(squeue -t PENDING | grep $RECORD_SLURM_PREFIX | wc -l) -1 )) ))
#        fi
#    fi
    if [ -z "$instances" ] 
    then
        instances=0
    fi

    echo "$instances"
}


DEBUG=
if [ -n "$RECORD_DEBUG" ]
then 
    export DEBUG=$RECORD_DEBUG
fi

# To reduce the instantiation time when testing, this is so it does not run
# everything after this. 

if [[ -n "$TESTING" ]]
then
    return
fi

# Defaults

if [ -z "$RECORD_USER_FILE" ]
then
    export RECORD_USER_FILE=data/ssrepi.users
fi

if [ -z "$RECORD_MAX_PROCESSES" ]
then
    export RECORD_MAX_PROCESSES=4
fi

if [ -z "$RECORD_SLURM_PREFIX" ]
then
  	export RECORD_SLURM_PREFIX=record
fi

if [ -z "$RECORD_REQUIRED_NOF_CPUS" ]
then
  	export RECORD_REQUIRED_NOF_CPUS=4
fi

if [ -z "$RECORD_SLEEP" ]
then
  	export RECORD_SLEEP=30
fi

if [ ! -f $RECORD_USER_FILE ]
then
    (>&2 echo "BASH: No user file available.") 
    exit -1
fi

if [ -n "$RECORD_SLURM" ] && ! which squeue > /dev/null 
then
    (>&2 echo "BASH: No squeue and RECORD_SLURM is set
        Is Slurm installed?")
    exit -1
fi

if [ -n "$RECORD_SLURM" ] 
then
    if [ -z "$RECORD_SLURM_PREFIX" ]
    then
        export RECORD_SLURM_PREFIX="record"
    fi
fi

if [ -n "$RECORD_SLURM" ] 
then
    if [ -z "$RECORD_SLURM_SBATCH_MAX_CHARS" ]
    then
        export RECORD_SLURM_SBATCH_MAX_CHARS="1000000"
    fi
fi

if [[ "$RECORD_DBTYPE" = "postgres" ]]
then
    if [ -z "$RECORD_DBUSER" ]
    then
        export RECORD_DBUSER="ds42723"
    fi
    if [ -z "$RECORD_POSTGRES_HOST" ]
    then
        export RECORD_POSTGRES_HOST="localhost"
    fi
    if [ -z "$RECORD_POSTGRES_PORT" ]
    then
        export RECORD_POSTGRES_PORT="5432"
    fi
    if [ -z "$RECORD_POSTGRES_PASSWORD" ]
    then
        (>&2 echo "BASH: Need to set a password to use the database.")
        exit -1
    fi
    if [ "$RECORD_POSTGRES_PASSWORD" = "xxxx" ]
    then
        (>&2 echo "BASH: Need to set a password to use the database.")
        exit -1
    fi
elif [[ "$RECORD_DBTYPE" = "gremlin" ]]
then
    if [ -z "$RECORD_GREMLIN_HOST" ]
    then
        export RECORD_GREMLIN_HOST="ws://127.0.0.1:8182/gremlin"
    fi
    if [ -z "$RECORD_GREMLIN_TIMEOUT" ]
    then
        export RECORD_GREMLIN_TIMEOUT=1200000
    fi
else
    if [ -z "$RECORD_DBFILE" ]
    then
        export RECORD_DBFILE="ssrepi.db"
    fi
fi

if which record-create-database.py >/dev/null 2>&1
then
    record-create-database.py
else
    (>&2 echo "No record python functions available. 
        Have you set the PATH variable correct?")
    exit -1
fi

# Check we have a sufficiently advanced version of Bash

BASH_MAJOR_VERSION=$(bash --version | sed -n 1p | awk '{print $4}' | cut -f1 -d.)
if [ "$BASH_MAJOR_VERSION" -lt 4 ]
then
    (>&2 echo "BASH: $0: Minimum requirement for bash failed")
    (>&2 echo "BASH: $0: Required 4 got " \
    $(bash --version | sed -n 1p | awk '{print $4}' | cut -f1 -d.))
    exit -1
fi

source lib.folksonomy.sh

# So you cannot do this in a while read ... do ... done loop on the end of
# a pipe, so I have done this with a for loop, but unfortunately this picks
# up on spaces as delimiters, so we have to set/unset IFS.

my_file=$(<$RECORD_USER_FILE)
IFS=$'\n'
for details in $my_file
do
    if [[ "$details" =~ ^record_user ]]
    then
        continue
    fi
    record_user_id=$(echo $details | cut -f 1 -d,)
    name=$(echo $details | cut -f 2 -d,)
    email=$(echo $details | cut -f 3 -d,)
    user=$(echo $details | cut -f 4 -d,)
    homedir=$(echo $details | cut -f 5 -d,)

    id_person=$(record-update.py \
         --table=Person \
         --id_person=person_$record_user_id \
         --name="$name" \
         --email=$email \
    ) || exit -1
    declare $record_user_id=$id_person
    if [ -n "$user" ]
    then
        id_user=$(record-update.py \
              --table=User \
              --home_dir=$homedir \
              --account_of=person_$record_user_id \
              --id_user=user_$user \
        ) || exit -1
    fi
done 
unset IFS


# Create some standard boxs

id_box_bash=$(record-update.py \
    --table=BoxType \
    --id_box_type=box_type_bash \
    --description="A Bourne-again bash script" \
    --format='text/x-shellscript' \
    --identifier=magic:'^.*shell script text executable.*$' \
) || exit -1
export bash=$id_box_bash

id_box_perl=$(record-update.py \
    --table=BoxType \
    --id_box_type=box_type_perl \
    --description="A Perl script" \
    --format='text/x-perl' \
    --identifier=magic:'^.*perl script text executable$' \
) || exit -1
export perl=$id_box_perl

id_box_R=$(record-update.py \
    --table=BoxType \
    --id_box_type=box_type_R \
    --description="An R  script" \
    --format='text/plain' \
    --identifier=magic:'^.*Rscript script text executable.*'
) || exit -1
export R=$id_box_R

export id_box_elf=$(record-update.py \
    --table=BoxType \
    --id_box_type=box_type_elf \
    --description="64bit Linux Executable" \
    --format='application/x-executable' \
    --identifier=magic:'^.*ELF 64-bit LSB executable\, x86-64.*$'
) || exit -1

export elf=$id_box_elf

[ -n "$DEBUG" ] && (>&2 echo "BASH: record.sh: LOADED")
CONFIG_LOADED=1


