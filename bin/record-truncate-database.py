#!/usr/bin/env python3

__copyright__ = "Copyright 2016"
__license__ = "This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
__version__ = "1.0.0"
__authors__ = "Doug Salt"
__credits__ = "Gary Polhill, Lorenzo Milazzo"
__modified__ = "2017-03-02"


import sys
import argparse

sys.path.append("lib")
import record as record

# A program to truncate the database
parser = argparse.ArgumentParser(
    description="Truncate all tables from the RECORD provenance database."
)

parser.add_argument(
    "--force",
    action="store_true",
    help="actually perform the truncation"
)

args = parser.parse_args()

if not args.force:
    sys.stderr.write(
        "Refusing to truncate the RECORD database.\n"
        "Use --force if you really want to truncate all tables.\n"
    )
    sys.exit(1)


if record.debug:
    sys.stderr.write("PYTHON: truncate-database.py: Entering...\n")

if record.db_type != "gremlin": 
    conn = record.connect_db()
    record.empty_tables(conn)
    record.disconnect_db(conn)
else:
    sys.stderr.write("PYTHON: truncate-database.py: Meaningless for a graph database, use delete-database.py\n")

if record.debug:
    sys.stderr.write("PYTHON: truncate-database.py: Exiting...\n")
