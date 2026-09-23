## SYNOPSIS

`record-check-slurm-journals.sh`

## DESCRIPTION

`record-check-slurm-journals.sh` scans Slurm output files in the current
directory and checks them for errors.

The script searches for files matching the pattern `slurm*out`. For each
matching file it invokes the `check_for_errors` function provided by the
RECORD workflow library.

This command is intended to help detect errors that occurred during Slurm
batch job execution by inspecting the output journals produced by the
scheduler.

## OPTIONS

This command takes no command-line options.

## EXIT STATUS

Returns 0 on success.

Returns non-zero if the underlying error-checking functions report
failures.

## ENVIRONMENT

The script requires the RECORD workflow shell utilities provided by:

`lib.record.common.sh`
: provides the `check_for_errors` function used to analyse Slurm output
  files.

## RETURN VALUE

None.

## EXAMPLES

Check all Slurm job output files in the current directory:

    record-check-slurm-journals.sh

Typical usage after a batch run:

    sbatch run-model.sh
    record-check-slurm-journals.sh

## FILES

`lib.record.common.sh`
: provides shared functions used by RECORD shell tools.

## AUTHORS

Doug Salt, Lorenzo Milazzo, Gary Polhill

## REPORTING BUGS

Report bugs to the maintainers of the RECORD workflow tools.

## BUGS

The script only checks files matching the pattern `slurm*out` in the
current directory and does not recurse into subdirectories.

## COPYRIGHT

Copyright © 2022 The James Hutton Institute.  License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

## SEE ALSO

`sbatch`(1), `squeue`(1)

## HISTORY

Introduced as part of the RECORD workflow support scripts to automate
checking of Slurm journal files for runtime errors.
