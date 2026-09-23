#!/usr/bin/env python3

__copyright__ = "Copyright 2016"
__license__ = "This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
__version__ = "1.0.0"
__authors__ = "Doug Salt"
__credits__ = "Gary Polhill, Lorenzo Milazzo"
__modified__ = "2017-03-02"


import sys
from os.path import basename

# I am going to have to think of a better way of doing this. Need to 
# research site level Python paths. Additionally I only want to import
# some functionality. In this instance 

sys.path.append("lib")
import record as record

# A program to initialise the database

if record.debug:
    sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]) + ": Entering...\n")

print(record.specification())

if record.debug:
    sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]) + ": ...Exiting.\n")
