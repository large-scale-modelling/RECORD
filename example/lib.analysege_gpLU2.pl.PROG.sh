PROG=$(record_application analysege_gpLU2.pl \
    --purpose="
Analysis script to prepare results from SSS runs. The output is a CSV format
summary of the results from each run, listing the parameters first, then
the results: the number of bankruptcies, the amount of land use change,
the year of extinction of each species, and the abundance of each species.

Number of species at a given time step
Level of occupancy at each time step
Shannon index and evenness measure." \
) || exit -1

# You are a complete and total idiot. My stupidity tends to infinity as I
# approach one. Unbelievabe. I am not going to reveal what I did here before
# but you can probably guess. Let's just say my output file was _considerably_
# larger than it should have been.

# There is the usual lesson here - which is do not make assumptions (problem
# being is that you didn't of course know you were making those assumptions
# until you are slapped in the face by a wet haddock because of those
# assumptions, and even then being slapped in the face by a wet haddock seems
# like the behaviour you are expecting until something alerts you to the fact
# that being slapped in the face by a wet haddock is probably not something you
# should be expecting. So the endeavour becomes: the recognition of piscean
# countenance concussion (the clue should have been the length of time).

source lib.analysege_gpLU2.pl.requirements.software.sh
source lib.analysege_gpLU2.pl.requirements.hardware.sh
source lib.analysege_gpLU2.pl.argument-types.sh
source lib.analysege_gpLU2.pl.input-types.sh
FOR=analysege_gpLU2.pl source lib.analysege_gpLU2.pl.output-types.sh


