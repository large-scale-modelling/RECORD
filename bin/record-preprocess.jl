#!/usr/bin/env julia

# This is a program to pre-process commands and produce the provenance scripts
# required for inclusion in the scripts to generate the provenance. This will
# produce the argument lines that go into the run of the program, some of the
# output types if they are required (only for redirection iin this case) and
# the source file for the argument types (see below).

# So if you run a command, then you can have the following cases.

# What you normally have is for:

# MSDOS: command /S1 /S2:value p1_value p2_value ... in any order

# Powershell: -param_1 -param_2 value_1 postion_value_1 ... in any order

# *NIX: command -ABC -D -E value --long-flag --long-parameter value --long-parameter=value_2 postion_value_1 position_value_2

# The commonality here is that the assignment-operator is space. The code
# should be intelligent enough to do the rest. However we should take a
# --assignment-operator=value or --assignment-operator value and the same with
# -a Therefore we should only start serious processing after --
#
# Ambiguities
# ===========
#
# Any ambiguities must be listed here. We will have assumption vs alternative.
# The code should offer between the two unless we have --suppress-choices|-S set

# In unix the assignment operator is equal or a space (or may even be both at
# the same time). You can work this out says for instance we have

# ASSUMPTION: command --option_1 value_1 --option_2 value_2 
# ALTERANTIVE: command --flag1 --flag2 position_value_1 position_value_2

# ASSUMPTION: command value1 value2 value3 
# Alternative command value1 ... (i.e. variable number of args - however this should be taken care of by "arity" and "separator")

using Logging
const VERSION = "0.1.0"
debug = false
assignment_operator = nothing   #= so this is the interesting one, we need to
                                redefine this because in unix this may be '='
                                or (crucially at the same time) it may be ' ',
                                so we need to be able to pass multiple parts of
                                these in the construction =#
unix_flags = false
PROG = nothing
suppress_alternatives = false
outputs_path = nothing
arguments_path = nothing

function print_help()
    println("""
Usage:
  script.jl [options] -- [passthrough args...]

Options (parsed only before --):
  -a <val>                          Set assignment-operator (same as --assignment-operator)
  -a=<val>                          Set assignment-operator
  --assignment-operator <val>       Set assignment-operator
  --assignment-operator=<val>       Set assignment-operator
  -D, --debug                       Enable debug mode
  -H, --help                        Show this help
  -l <val>                          Argument types library file
  -l=<val>                          Argument types library file
  --argument-types-library <val>    Argument library file for \$PROG
  --argument-types-library=<val>    Argumentlibrary file \$PROG
  -o <val>                          Output type library file
  -o=<val>                          Output type library file
  --output-types-library <val>      Output type library file
  --output-types-library=<val>      Output type library file
  -R, --run                         Run the code
  -S, --suppress-alterantives       Do not show any ambiguity in argument assingment, but take the default
  -U, --unix-flags                  Treat single hyphen options as single letter flags
  -V, --version                     Show version

Everything after -- is treated as positional passthrough and printed as-is.

If --argument-types-lib or -a  is specified, this will overwrite the default argument path which will be

"lib.\$PROG.argument-types.sh"

where \$PROG is the command being run, e.g `SSS-StopC2-create.sh` and this will be written to the current directory.

Similarly

This program will produce line to the stdout that needs to be included in the call to add the paremeter using the provenance For example if we had

prog.py \
   --out-file=dougs.file" \
   -on-flag \
   -A \
   -i input_path.dat \
   "pickling times are fun times"
   2>&1 \
   > dougs.out
 
\$ARGS=\"\"\"\$ARGS 
--record-argument-\${id_prog.py_i}=input_path.dat"
--record-argument-\${id_prog.py_out-file}=dougs.file"
--record-argument-\${id_prog.py_A}
--record-argument-\${id_prog.py_on_flag}
--record-stdout-\$
\"\"\"

Note there is some ambiguity above "input_path.dat" might be a positional parameter and "-i" might be a flag.

It will produce the argument file types file

```
FOR="prog.py"

# The regex in range and the descriptions need adjusting

\$a_prog.py_i_id=\$(record_argument_type \\
    \$PROG \\
    a_\$FOR_i \\
    --description="Please add a description." \\
    --type=option \\
    --name=i  \\
    --range='^input_file.dat\$' \\
) || exit -1 

\$a_prog.py_out-file_id=\$(record_argument_type \\
    \$PROG \\
    a_\$FOR_out-file \\
    --description="Please add a description." \\
    --type="option" \\
    --name="out-file"  \\
    --range='^dougs.file\$' \\ 
) || exit -1 

\$a_prog.py_A_id=\$(record_argument_type \\
    \$PROG \\
    a_\$FOR_A \\
    --description="Please add a description." \\
    --type=flag \\
    --name=A  \\
) || exit -1 

\$a_prog.py_on_flag_id=\$(record_argument_type \\
    \$PROG \\
    a_\$FOR_i \\
    --description="Please add a description." \\
    --type="flag"\\
    --name=on_flag  \\
) || exit -1 

\$a_prog.py_pos_one_id=\$(record_argument_type \\
    \$PROG \\
    a_\$FOR_pos_one \\
    --identifier=1 \\
    --description="Please add a description." \\
    --type="required"\\
    --name=pos_one  \\
    --arity=1 \\
    --order_value=1 \\
    --range='^pickling times are fun times\$'
) || exit -1 
```

Additionly because of the redirection this would also produce the addition to the output (see `record-get-io.jl --help` on how to produce this)

```
FOR="prog.py"

\$o_prog.py_stdout_id =\$(record_output_type \\
    \$PROG \\
    boxtype.\$FOR.stdout \\
    arg=2 \\
) || exit -1

\$o_prog.py_stdout_id =\$(record_output_type \\
    \$PROG \\
    boxtype.\$FOR.stderr \\
    arg=3 \\
) || exit -1
```

""")
end

function die(msg::String, code::Int=2)
    println(stderr, "Error: ", msg)
    println(stderr, "Try --help")
    exit(code)
end

function parse_before_double_dash(argv::Vector{String})

    i = 1
    execute = false
    suppress = false
    arguments_path = nothing
    outputs_path = nothing
    assignment_operator = nothing
    unix_flags = nothing

    while i <= length(argv)
         a = argv[i]

        # Stop parsing at --
        if a == "--"
            return (execute, arguments_path, outputs_path, unix_flags, assignment_operator, suppress, argv[(i+1):end])
        end

        # Help/version/debug (no values)
        if a == "--help" || a == "-H"
            print_help()
            exit(0)
        elseif a == "--version" || a == "-V"
            println(VERSION)
            exit(0)
        elseif a == "--debug" || a == "-D"
            global debug = true
            i += 1
            continue
        end

        # Flags
        if a == "--run" || a == "-R"
            execute = true
            i += 1
            continue
        end

        if a == "--suppress-alternatives" || a == "-S"
            suppress_alternatives = true
            i += 1
            continue
        end

        if a  == "--unix-flags" || a == "-U"
            assignment_operator = "="
            unix_flags = true
            i += 1
            continue
        end

        # Handle --assignment-operator / --assignment-operator with =value or next token
        if startswith(a, "--assignment-operator")
            name, value = split(a, "=", limit=2)
            if val === nothing
                if i == length(argv)
                    die("Missing value for $name")
                end
                assignment_operator = argv[i+1]
                i += 2
            else
                assignment_operator = val
                i += 1
            end
            continue
        end


        # Handle -a or -a=value for assignment operator
        if a == "-a" || startswith(a, "-a=")
            if a == "-a"
                if i == length(argv)
                    die("Missing value for -a")
                end
                assignment_operator = argv[i+1]
                i += 2
            else
                _, value = split(a, "=", limit=2)
                assignment_operator = val
                i += 1
            end
            continue
        end

        # Handle --argument-types-library/ --argument-type-library with =value or next token
        if startswith(a, "--argument-types-library")
            name, value = split(a, "=", limit=2)
            if val === nothing
                if i == length(argv)
                    die("Missing value for $name")
                end
                arguments_path = argv[i+1]
                i += 2
            else
                arguments_path = val
                i += 1
            end
            continue
        end

        # Handle -a or -a=value for argument types library
        if a == "-l" || startswith(a, "-l=")
            if a == "-l"
                if i == length(argv)
                    die("Missing value for -l")
                end
                arguments_path = argv[i+1]
                i += 2
            else
                _, value = split(a, "=", limit=2)
                arguments_path = val
                i += 1
            end
            continue
        end

        # Handle --argument-types-library/ --argument-type-library with =value or next token
        if startswith(a, "--output-types-library")
            name, value = split(a, "=", limit=2)
            if val === nothing
                if i == length(argv)
                    die("Missing value for $name")
                end
                outputs_path = argv[i+1]
                i += 2
            else
                outputs_path = val
                i += 1
            end
            continue
        end

        # Handle -a or -a=value for argument types library
        if a == "-o" || startswith(a, "-o=")
            if a == "-o"
                if i == length(argv)
                    die("Missing value for -o")
                end
                outputs_path = argv[i+1]
                i += 2
            else
                _, value = split(a, "=", limit=2)
                outputs_path = val
                i += 1
            end
            continue
        end

        # Unknown option before --
        if startswith(a, "-")
            die("Unknown option: $a")
        end

        # Positional encountered before --:
        # You didn’t specify what to do with these; safest is treat as error
        # because you said "treat the ones before as standard unix args".
        die("UnAdult expected positional argument before --: $a")
    end

    # No -- found: passthrough is empty
    return (execute, arguments_path, outputs_path, assignment_operator, suppress, String[])
end

function preprocessor(
        arguments::IO,
        outputs::IO,
        PROG::String,
        name::String,
        type::String,
        value::Any,
        order_value::Any = nothing,
        separator::Any = nothing,
        assignment::Any = nothing,
        )

    @debug """\
    PROG $PROG 
    name $name
    type $type
    value $value
    order_value $order_value
    separator $separator
    assignment $assignment"""

    # Do the necessary printy and writey stuff.
    if type == "extend_stdout"
        println("--record-extend-stdout-\${o_$(PROG)_$(name)_id}=$value")
    elseif type == "stdout"
        println("--record-stdout-\${o_$(PROG)_$(name)_id}=$value")
    elseif type == "extend_stderr"
        println("--record-extend-stderr-\${o_$(PROG)_$(name)_id}=$value")
    elseif type == "stderr"
        println("--record-stderr-\${o_$(PROG)_$(name)_id}=$value")
    else
        println("--record-argument-\${a_$(PROG)_$(name)_id}=$value")
    end


    if type == "stdout" || type == "extend_stdout" || type == "stderr" || type == "extend_stderr"
        kind = "stdout"
        if occursin("stderr", type)
            kind = "stderr"
        end
        println(outputs, "\$o_$(PROG)_$(name)_id=\$(record_output_box_type \\\\")
        println(outputs, "\tbox_type.$(PROG).$(name) \\\\")
        println(outputs, "\t\"^$value\$\" \\\\")
        println(outputs, "\t\"$kind\" \\\\")
        println(outputs, ") || exit -1\n")
    else
        # Now do the arguments file
        
        println(arguments, "\$a_$(PROG)_$(name)_id=\$(record_argument_type \\\\")
        println(arguments, "\t\$PROG \\\\")
        println(arguments, "\t\"argument.$PROG.name\" \\\\")
        println(arguments, "\t--description=\"Please add a description.\" \\\\")
        println(arguments, "\t--type=\"$type\"\\\\")
        println(arguments, "\t--name=\"$name\"  \\\\")
        if assignment != nothing
            println(arguments, "\t--assignment_operator=\"$assignment\"  \\\\")

        end
        if type == "option"
            println(arguments, "\t--range=\"^$value\$\" \\\\")
        elseif type == "flag"
        elseif type == "required"
            println(arguments, "\t--range='^$value\$' \\\\")
            println(arguments, "\t--arity=1 \\\\")
            println(arguments, "\t--order_value=$order_value \\\\")
            println(arguments, "\t--identifier=$order_value \\\\")
            # TODO deal with multiple arity arguments
            #println(arguments, "\t--arity=$arity \\\\")
            #println(arguments, "\t--separator=$separator \\\\")
            
        end
        println(arguments, ") || exit -1\n")
    end

end

function trace_file_io(passthrough::Vector{String};
                       exclude_prefixes = ["/lib", "/usr/lib", "/proc", "/sys", "/dev", "/etc/ld",
                                           "/usr/share", passthrough[1]],
                       STDERR::IO = stderr,
                       STDOUT::IO = stdout)
    println("pickle")    
    (path, io) = mktemp()
    strace_cmd = `strace -o  $(path) -e trace=openat,open,creat,rename,unlink -f -s 512 $(passthrough)`
    println("pockle")    
    
    run(pipeline(strace_cmd, stderr=STDERR, stdout=STDOUT))
    data = read(path)
    err = IOBuffer(data)
    strace_out = String(take!(err))

    println("=====================================")
    println(strace_out)
    println("=====================================")
    reads  = Set{String}()
    writes = Set{String}()

    for line in split(strace_out, "\n")
        # Extract filename from the syscall
        m = match(r"openat\(.*?,\s*\"(.*?)\".*?(O_[A-Z|]+)", line)
        m === nothing && continue

        filepath = m.captures[1]
        flags    = m.captures[2]

        # Skip system/library paths
        any(startswith(filepath, p) for p in exclude_prefixes) && continue
        # Skip relative junk and anonymous
        startswith(filepath, "//") && continue

        if occursin("O_RDONLY", flags)
            push!(reads, filepath)
        elseif occursin("O_WRONLY", flags) || occursin("O_RDWR", flags) || occursin("O_CREAT", flags)
            push!(writes, filepath)
        end
    end

    return (reads=reads, writes=writes)
end

function main(argv::Vector{String})


    (execute, 
     arguments_path, 
     outputs_path, 
     unix_flags,
     assignment_operator, 
     suppress_alternatives, 
     passthrough) = parse_before_double_dash(argv)
    
    debug && global_logger(ConsoleLogger(stderr, Logging.Debug))

    arguments = nothing
    outputs = nothing
    position = 0

    PROG  = nothing
    
    # This next is used to store for redirection
    
    STDOUT = stdout
    STDERR = stderr
    
    # The pathnames for the above, if the above are custom.

    custom_stderr = nothing
    custom_stdout = nothing

    @debug "assignment_operator=$(assignment_operator)"
    @debug "passthrough args (after --): $passthrough"
    println("\$ARGS=\"\"\"\$ARGS")
    i = 1
    while i <= length(passthrough)

        # These are values for the table Argument

        # Arguments
        # =========

        id_argument = nothing # Need a random way of generating this
        assignment = nothing
        type = nothing # "required", "option", "flag" - so this is a bit of an oversight because you can have nameioinal positional arguments, but this can be covered by arity.
        order_value = nothing # used to indicate position if a positonal character
        identifier = nothing # A number or short identifying string for required arguments to identify them. String. Null if the argument is not required.
        name = nothing # The name of the argument
        description = nothing # might be able to work this out. "
        separator = nothing # "-", "--"  or "/" (windows)
        arity = nothing # number of parts of a particular argument, may be a number, ?, * or + (one or none,none to many, 1 to many, respectively)
        range = nothing # Can build a regex from the original answer
        application = nothing # Gonna point at PROG above

        # Argument Value
        # ==============

        #has_value = Nothing
        #for_process = Nothing  # (don't need this done by the code)
        #for_argument = Nothing

        # We don't need any of this because we just need to producte the string
        #"--record-argument-\${$id_argument}=$has_value\n"

        a = passthrough[i]
        if i == 1
            if Sys.which(a) == nothing
                die("The executable $a is missing.")
            else 
                PROG = a
                if arguments_path == nothing
                    arguments_path = "lib." * PROG * ".argument-types.sh"
                end
                arguments = open(basename(arguments_path), "a")
                println(arguments, "FOR=$PROG\n")

                println(arguments, "# The regex in range and the descriptions need adjusting\n")

                if outputs_path == nothing
                    outputs_path = "lib." * PROG * ".output-types.sh"
                end
                outputs = open(basename(outputs_path), "a")
                println(outputs, "FOR=$PROG\n")
            end
            @debug "Going to run $PROG"
            i += 1
            continue
        else
            if startswith(a, "--")
                separator = "--"
                if unix_flags
                    assignment = "="
                    occursin("=", a) ? (name, value) = split(a, assignment_operator, limit=2) : (name, value) = (a, true)
                    if value == nothing
                        type = "flag"
                    else
                        type = "option"
                    end
                    name = name[3:end]
                elseif assignment_operator != nothing
                    @debug "Assignment operator detected on $a"
                    assignment = assignment_operator
                    # Fixed assingment operator
                    occursin(assignment_operator, a) ? (name, value) = split(a, assignment_operator, limit=2) : (name, value) = (a, true)
                    if value == nothing
                        type = "flag"
                    else
                        type = "option"
                    end
                    name = name[3:end]
                elseif occursin("=", a)
                    @debug "= used as assignment operator in $a"
                    assignment = "="
                    name, value = split(a, "=", limit=2)
                    type = "option"
                    name = name[3:end]
                elseif i + 1 > length(passthrough) || 
                    startswith(passthrough[i + 1], '-') || 
                    startswith(passthrough[i + 1], '/') ||
                    startswith(passthrough[i + 1], '>')
                    # Read ahead
                    @debug "no possible value for $a"
                    name = a[3:end]
                    type = "flag"
                    value = true
                else
                    @debug "next value is for $a"
                    assingment = ' '
                    name = a[3:end]
                    i += 1
                    value = passthrough[i]
                    type = "option"
                end
            elseif startswith(a, "-")
                separator = "-"
                if unix_flags == true
                    name = a[2:end]
                    if length(name) > 1 
                        for c in name[1:(end - 1)]
                            preprocessor(arguments, 
                                         outputs, 
                                         PROG, 
                                         c, 
                                         "flag", 
                                         nothing, 
                                         nothing, 
                                         nothing, 
                                         '-')
                        end
                    else
                        # Do a single option, or do the last flag (it may have a value in *nix)
                        if i + 1 > length(passthrough) || 
                        startswith(passthrough[i + 1], '-') || 
                        startswith(passthrough[i + 1], '/') ||
                        startswith(passthrough[i + 1], '>')
                            # Read ahead
                            i += 1
                            value = passthrough[i]

                            preprocessor(arguments, 
                                         outputs, 
                                         PROG, 
                                         name,
                                         "option",
                                         value, 
                                         nothing, 
                                         ' ', 
                                         '-')
                        else
                            preprocessor(arguments, 
                                         outputs, 
                                         PROG, 
                                         name,
                                         "flag",
                                         nothing, 
                                         nothing, 
                                         nothing, 
                                         '-')
                        end 
                    end
            elseif assignment_operator != nothing
                    @debug "Assignment operator detected on $a"
                    assignment = assignment_operator
                    occursin(assignment_operator, a) ? (name, value) = split(a, assignment_operator, limit=2) : (name, value) = (a, true)
                    name = name[2:end]
                    if name == nothing
                        i += 1
                        continue
                    else
                        if value == nothing
                            type = "flag"
                        else
                            type = "option"
                        end
                    end
                elseif occursin("=", a)
                    @debug "= used as assignment operator in $a"
                    assignment = "="
                    name, value = split(a, "=", limit=2)
                    type = "option"
                    name = name[2:end]
                elseif  i + 1 > length(passthrough) || 
                    startswith(passthrough[i + 1], '-') || 
                    startswith(passthrough[i + 1], '/') ||
                    startswith(passthrough[i + 1], '>')
                    # Read ahead
                   @debug "no possible value for $a"
                    name = a[2:end]
                    type = "flag"
                    value = true
                else
                    @debug "next value is for $a"
                    assingment = ' '
                    name = a[2:end]
                    i += 1
                    value = passthrough[i]
                    type = "option"
                end
            elseif startswith(a, "/")
                separator = "/"
                if assignment_operator != nothing
                    @debug "Assignment operator detected on $a"
                    assignment = assignment_operator
                    occursin(assignment_operator, a) ? (name, value) = split(a, assignment_operator, limit=2) : (name, value) = (a, true)
                    if value == nothing
                        type = "flag"
                    else
                        type = "option"
                    end
                    name = name[2:end]
                elseif occursin(":", a)
                    assignment = ":"
                    @debug ": used as assignment operator in $a"
                    name, value = split(a, ":", limit=2)
                    type = "option"
                    name = name[2:end]
                elseif i + 1 > length(passthrough) || 
                    startswith(passthrough[i + 1], '-') || 
                    startswith(passthrough[i + 1], '/') ||
                    startswith(passthrough[i + 1], '>')
                    # Read ahead
                    @debug "no possible value for $a"
                    name = a
                    type = "flag"
                    value = true
                else
                    @debug "next value is for $a"
                    assingment = ' '
                    name = a[2:end]
                    i += 1
                    value = passthrough[i]
                    type = "option"
                end
            elseif startswith(a, "2>>")
                type = "extend_stderr"
                name = "stderr"
                if length(a) == 3
                    @debug "next value is for $a"
                    i += 1
                    value = passthrough[i]
                    STDERR = open(value, "a")
                    custom_stderr = value
                    deleteat!(passthrough, (i - 1):i)
                    i -= 2
                elseif occursin("&1", a)
                    if STDOUT == stdout
                        value = "stdout"
                    else
                        value = custom_stdout
                        STDERR = STDOUT
                    end
                    deleteat!(passthrough, i)
                    i -= 1
                else
                    value = a[4:end]
                    STDERR = open(value, "a")
                    custom_stderr = value
                    deleteat!(passthrough, i)
                    i -= 1
                end
            elseif startswith(a, "2>")
                type = "stderr"
                name = "stderr"
                if length(a) == 2
                    @debug "next value is for $a"
                    i += 1
                    value = passthrough[i]
                    STDERR = open(value, "w")
                    custom_stderr = value
                    deleteat!(passthrough, (i - 1):i)
                    i -= 2
                elseif occursin("&1", a)
                    if STDOUT == stdout
                        value = "stdout"
                    else
                        value = custom_stdout
                        STDERR = STDOUT
                    end
                    deleteat!(passthrough, i)
                    i -= 1
                else
                    value = a[3:end]
                    STDERR = open(value, "w")
                    custom_stderr = value
                    deleteat!(passthrough, i)
                    i -= 1
                end
            elseif startswith(a, ">>")
                type = "extend_stdout"
                name = "stdout"
                if length(a) == 2
                    @debug "next value is for $a"
                    i += 1
                    value = passthrough[i]
                    deleteat!(passthrough, (i - 1):i)
                    i -= 2
                else
                    value = a[3:end]
                    deleteat!(passthrough, i)
                    i -= 1
                end
                STDOUT = open(value, "a")
                custom_stdout = value
            elseif startswith(a, ">")
                @debug "extend $a"
                type = "stdout"
                name = "stdout"
                if length(a) == 1
                    @debug "next value is for $a"
                    name = 
                    i += 1
                    value = passthrough[i]
                    custom_stdout = value
                    @debug "removing $passthrough[(i-1):i]" 
                    deleteat!(passthrough, (i -1):i)
                    i -= 2
                else
                    value = a[2:end]
                    deleteat!(passthrough, i)
                    i -= 1
                    @debug "removing single $passthrough[i]" 
                end
                STDOUT = open(value, "w")
                custom_stdout = value
            elseif !isempty(a)
                @debug "Positional Argument $a"
                position += 1
                value = a
                name = string(position)
                order_value = position
                type = "required"
            end

        end

        i += 1

        preprocessor(arguments, 
                     outputs, 
                     PROG, 
                     string(name), 
                     type, 
                     value, 
                     order_value, 
                     separator, 
                     assignment)

    end
    println("\"\"\"")

    close(arguments)
    close(outputs)

    @debug """
    execute = $execute
    debug = $debug
    unix_flags = $unix_flags
    asssignment_operator = $assignment_operator
    executing: $passthrough
    """

    if execute && !isempty(passthrough)
        result = trace_file_io(passthrough, STDOUT = STDOUT, STDERR = STDERR)

        # So we have two things we have four things we have to create here.
        #
        println("Files read:    ", result.reads)
        println("Files written: ", result.writes)
    end
    
end

main(ARGS)
