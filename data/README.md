# PURPOSE

The purpose of this directory is to provide data configuration services for the RECORD framework.

This will act as a temporary directory for parameters, so they are shared across the cluster

THIS DIRECTORY MUST BE SHARED ACROSS THE CLUSTER.

# MANIFEST

+ `make-user-file.sh` - takes all the users on the system and produces a RECORD recognized format for users. This script also adds exterrnal users ad hoc.
+ `ssrepi.users` - this is an empty file, because user information is sensitive. You can use the the shell script above to produce new users.
