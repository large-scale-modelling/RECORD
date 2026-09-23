export PATH=$PWD/bin:$PWD/lib:$PATH
export PYTHONPATH=$PWD/lib:$PYTHONPATH

export PATH=$PWD/example:$PATH

# This takes any value. If this value is present, debug is assumed to be on.

#export RECORD_DEBUG=True

# Any script file in the path, or an absolute path name.
# So for the example, might `SSS-StopC2-create.sh`

export RECORD_START_PROGRAM=workflow.sh

# The next may be:

# + sqlite3
# + postgres
# + gremlin
# + janusgraph

export RECORD_DBTYPE=postgres

# Valid users of the system, created in the data directory using `make-user-file.sh`

export RECORD_USER_FILE=data/ssrepi.users

# Temporary files are stored. That is system wide temporary files. If you want
# the temp files to be available to everybody, then this directory must be
# shared across the whole system. Be careful, this is one of the common gotchas
# on an HPC system. Remember that the nodes cannot necessarily see everything.
# This is why the ssrepi.users is in this directory

export RECORD_TMPDIR=data

# If the code is sleep, how many seconds it should wait before trying again.

export RECORD_SLEEP_PERIOD=30

# DO NOT BE TEMPTED TO DO THE FOLLOWING
#export RECORD_DBFILE=$(pwd)/ssrep.db
#export RECORD_DBFILE=~/ssrep.db
# It will make relative paths

# Postgresql stuff...

export RECORD_DBTYPE=postgres
export RECORD_DBUSER=ssrepi
export RECORD_POSTGRES_HOST=10.0.0.1
export RECORD_POSTGRES_PORT=5432
export RECORD_POSTGRES_PASSWORD='some-password'

# Multi processing. If you do not have slurm installed on your machine, then
# you can use the home-grown job scheduler, built into these scripts, noting that
# this scheduler is single machine limited.

# This controls both local scheduler and Slurm scheduler and addtionally the
# RECORD_block number of simultaneous processes.

export RECORD_REQUIRED_NOF_CPUS=4
export RECORD_MAX_PROCESSES=32

# The next are Slurm specific.

export RECORD_SLURM=1
export RECORD_SLURM_PREFIX=janusgraph
export RECORD_SLURM_LIMIT=10

# If you don't want any parallelisation on your head node, then set this to the
# headname host name. Fill with $(hostname) on the head machine - this is to
# stop hogging the head node

export RECORD_SLURM_HEAD_NODE=tupple

# Activate the python environment for RECORD

if [ -d postgres ]
then
   source postgres/bin/activate
else
   source gremlin/bin/activate
fi

