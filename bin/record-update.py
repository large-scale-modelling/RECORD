#!/usr/bin/env python3
"""A program to insert, or update values in the database, from the CLI
"""

__copyright__ = "Copyright 2016"
__license__ = "This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope thaGt it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
__version__ = "1.0.0"
__authors__ = "Doug Salt"
__credits__ = "Gary Polhill, Lorenzo Milazzo"
__modified__ = "2017-03-02"

import os, sys, getopt, re
from os.path import basename

sys.path.append("lib")
import record as record

table_parameter = re.compile(r'^--table=([A-Za-z0-9_]+)$')
column_parameter = re.compile(r'^([A-Za-z0-9\._-]+)(=(.*?))$', re.DOTALL)

ExistsException = None
if record.db_type == "gremlin":
    ExistsException = record.GremlinVertexExists
elif record.db_type == "sqlite3":
    import sqlite3
    ExistsException = sqlite3.IntegrityError 
else:
    import psycopg2
    ExistsException = psycopg2.errors.UniqueViolation
            
class IllegalArgumentError(ValueError):
    pass

def parameters(conn, argv):
    """ Variable parameters for updating the database.
    This will be of the form:

        --table=some_table_name
        [--column_name=some value]...

    It should be fairly evident that the parameters will change
    dependent upon the table.

    """

    table = None
    for arg in argv:
        if len(table_parameter.match(arg).groups()) != 0:
            table = table_parameter.match(arg).group(1)
            break

    
    if table == None:
        raise IllegalArgumentError("No --table argument supplied")
    tableClass = None
    try:    
        tableClass = getattr(record, table)    
    except:
        raise IllegalArgumentError("Invalid table name: " + table + "\n")

    columns = {}
    for arg in re.split(r' --',' '.join(argv)):
        if record.debug:
            sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Arg = " + arg + ".\n")
        if table_parameter.match(arg):
            pass
        elif (column_parameter.match(arg).group(1) != None and 
              column_parameter.match(arg).group(3) != None):
            col = column_parameter.match(arg).group(1).upper()
            col_argument = column_parameter.match(arg).group(3)
            instance = tableClass()
            if col in instance.__dict__:
                columns[col] = col_argument
            else:
                raise IllegalArgumentError("Invalid column: " + col + "\n")

    if len(columns.keys()) == 0:
        raise IllegalArgumentError("No valid columns supplied\n")
    return (table, columns)
        
if __name__ == "__main__":
    if record.debug:
        sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]) + ": Entering...\n")
    
    table = None
    colums = {}
    conn = record.connect_db()
    (table,columns) = parameters(conn,sys.argv[1:])

    tableClass = getattr(record, table)    

    # If this is the graphing database we do not need to worry about intermediate tables, we can form the link directly

    if (record.db_type == 'gremlin' or record.db_type == 'janusgraph') and tableClass.is_relation():
        result = record.gremlin_add_edge(conn, sys.argv[1:])
        print(result)
        sys.exit(0)
    
    # So we have a concurrency problem here. For the relational database
    # concurrency is desigin in. For a graph database you have to use a
    # particular backend to do this, so to mitigate this I am going to code
    # around it. We are going to read the entry and then work out if it
    # truly need updating.

        # 1. We need to extract the primary key and see if the record exists.
        # 2. If it exists we read it and populate the class.
        # 3. We then compare the class against what we have been provided as parameters
        # 4. If anything changes then we call the update - this nicely avoids
        #    the modified/modifier problem

    # This is a the logical place to do this, contrary to what you may think, Salt.

    existence = {}
    keyFound = False
    if record.debug:
        sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": columns = " + str(columns) + ".\n")
    for keyGroup in tableClass.primaryKeys():
        keyFound = True
        for key in keyGroup:
            if record.debug:
                sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": key = " + str(key) + ".\n")
            if not key in columns.keys():
                if record.debug:
                    sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": did not find key = " + str(key) + " in " + str(columns.keys()) + ".\n")
                keyFound = False 
        if keyFound == True:
            for key in keyGroup:
                existence[key] = columns[key]
            break

    if keyFound == False:
        raise  IllegalArgumentError("No primmary key supplied, got " + str(existence) + "\n")

    row = tableClass(existence)

    # So we have tried this using the exception route, so this is producing too
    # many errors in the log, so we need to go another route.

    if row.exists(conn) == True:
        if record.debug:
            sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Doing an update.\n")
        updateValues = {}
        row.query(conn)
        for key in columns:
            if getattr(row, key) != columns[key]:
                updateValues[key] = columns[key]
        if len(updateValues.keys()) > 0:
            if record.debug:
                sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Doing an update on " + str(table) + " with " + str(updateValues) + ".\n")
            row = tableClass(existence | updateValues)
            row.update(conn)
    else:
        row = tableClass(columns)
        row.add(conn)
#         try:
#        row.add(conn)
#        except GremlinServerError as e:
#            msg = str(e)
#            if e.status_code == 597:
#                if record.debug:
#                   sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Forcing an update.\n")
#                updateValues = {}
#                row.query(conn)
#                for key in columns:
#                    if getattr(row, key) != columns[key]:
#                        updateValues[key] = columns[key]
#                if len(updateValues.keys()) > 0:
#                    if record.debug:
#                       sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Doing a forced update on " + str(updateValues) + ".\n")
#                    row = tableClass(existence | updateValues)
#                    row.update(conn)
#            else:
#                raise
    record.disconnect_db(conn)
    result = re.sub(r' AND ',',', row.getPrimaryKeys())
    result = re.sub(r'^.* = ','',result)
    result = re.sub(r'[\'\"]','',result)
    if record.debug:
        sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + ": Result: " + str(result) + "\n")
    if record.debug:
        sys.stderr.write("PYTHON: " + basename(sys.argv[0]) + " " + " ".join(sys.argv[1:]) + ": ...Exiting.\n")
    print(result)
