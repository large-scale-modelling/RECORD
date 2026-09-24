# PURPOSE

This repository is for the Miracle simulation metadata outputs specification, now known as RECORD.

**R**eproducible
**E**xecution
**C**ollection and
**O**notological 
**R**epresentation of
**D**ata

# MANIFEST

+ `README.md` - this file
+ `bin` - the directory containing all executables. These are all written in Python.
+ `data` - data directory for the provenance framework, e.g. users of the system.
+ `example` - the example code or the reference example
+ `install-docs` - directory containing installation documents linked to in this file.
+ `lib` - bash and python libraries used by code in `bin`, and also the bash library is used by the code in `example`.
+ `LICENCSE` - GPLv3 license
+ `man` - a directory with a bunch of Unix man pages.
+ `miracle.python3.requirements` - the requirements needed to build the Python environment

# RUNNING THE EXAMPLE

To run the job, then in this direcotry.

```
. example/ENVIRONMENT.sh
record-clean.sh
record-start.sh

```

# INSTALLATION OF THE EXAMPLE

Make sure the postgres server is running or sqlite3 is installed.

In this directory:

`cp example/sample.ENVIRONMENT.postgres.sh example/ENVIRONMENT.sh` or `cp example/sample.ENVIRONMENT.gremlin.sh example/ENVIRONMENT.sh` 
and edit `example/ENVIRONMENT.sh` to match your example.

```
python -m venv postgres (or python -m venv gremlin)
bin/postgres/activate
pip install -r miracle.python3.requirements
```
also configure your users (note this will on work in *nix environment for now)
```
cd data
make-user-file.sh
```
edit the `make-user-file.sh` to add additional external users if needs be, before running it.

## DATBASES

Instructions on how to install the databases follow:

Note you only need to do the one you are using. This code will not currently work in a Windows environment, but you can connect to databases (other than sqlite) if they are runnning in another environment (say Windows native rather than WSL).

### POSTGRES

#### OSX

The instructions are [here](install-docs/INSTALL.osx.postgresql.md)

#### Linux

The instructions are [here](install-docs/INSTALL.linux.postgresql.md)

#### Windows

The instructions are [here](install-docs/INSTALL.windows.postgresql.md)

### SQLITE3

#### OSX

The instructions are [here](install-docs/INSTALL.osx.sqlite.md)

####  Linux

The instructions are [here](install-docs/INSTALL.linux.sqlite.md)

#### Windows

The instructions are [here](install-docs/INSTALL.linux.sqlite.md)

### Janusgraph

#### OSX

The instructions are [here](install-docs/INSTALL.osx.janusgraph.md).

#### Linux

The instructions are [here](install-docs/INSTALL.linux.janusgraph.md).

#### Windows

The instructions are [here](install-docs/INSTALL.windows.janusgraph.md).

### Tinkerpop

#### OSX

The instructions are [here](install-docs/INSTALL.osx.tinkerpop.md).

#### Linux

The instructions are [here](install-docs/INSTALL.linux.tinkerpop.md).

#### Windows

The instructions are [here](install-docs/INSTALL.windows.tinkerpop.md).


