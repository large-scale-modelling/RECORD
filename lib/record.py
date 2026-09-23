#!/usr/bin/env python3

# file name: ssrepi.py
# created: 20.04.15 - modified: 05.08.15

'''Social Simulation Repository Interface (SSRepI)'''

# ++ Social Simulations, Data Model (Metadata) ++

# J.G. Polhill et al. "Towards metadata standards for social
# simulation outputs" (in preparation)

# ++ metadata

__copyright__ = "Copyright 2015"
__license__ = "This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
__version__ = "3.0.0"
__authors__ = "Lorenzo Milazzo, J. Gary Polhill, Doug Salt"
__credits__ = ""

import os, sys, subprocess, re, mimetypes, rfc3987, os.path, datetime, magic
import graphviz, getpass
import inspect
import time
from pathlib import Path

#db_type = 'postgres'
#db_type = 'sqlite3'
#db_type = 'gremlin'
db_type = 'janusgraph'

debug = False
  
if 'RECORD_DBTYPE' in os.environ:
    db_type = os.environ['RECORD_DBTYPE']

if db_type == 'postgres':
    import psycopg2
    from psycopg2.extras import RealDictCursor
elif db_type == 'sqlite3':
    import sqlite3
elif db_type == 'gremlin' or db_type == 'janusgraph':
    from gremlin_python.driver.client import Client
    from gremlin_python.driver.protocol import GremlinServerError

    #from gremlin_python.driver.serializer import GraphBinarySerializersV1
    from gremlin_python.driver.serializer import GraphSONSerializersV3d0
    from typing import Optional
    
else:
    sys.stderr.write("LIB: Unknown database type %s \n" % db_type)
    raise

gremlin_request_options = None

db_file = os.path.join(os.getcwd(),'ssrep.db')
if 'RECORD_DBFILE' in os.environ:
    db_file = os.environ['RECORD_DBFILE']

db_user = "ds42723"
if 'RECORD_DBUSER' in os.environ:
    db_user = os.environ['RECORD_DBUSER']

db_name= "ssrepi"
if 'RECORD_DBNAME' in os.environ:
    db_name = os.environ['RECORD_DBNAME']

db_port = "5432"
if 'RECORD_POSTGRES_PORT' in os.environ:
    db_port = os.environ['RECORD_POSTGRES_PORT']

db_host = "localhost"
if 'RECORD_POSTGRES_HOST' in os.environ:
    db_host = os.environ['RECORD_POSTGRES_HOST']

db_passwd = "xxxx"
if 'RECORD_POSTGRES_PASSWORD' in os.environ:
    db_passwd = os.environ['RECORD_POSTGRES_PASSWORD']

gremlin_host = 'ws://localhost:8182/gremlin'
if 'RECORD_GREMLIN_HOST' in os.environ:
    gremlin_host = os.environ['RECORD_GREMLIN_HOST']

gremlin_timeout = 30000 
if 'RECORD_GREMLIN_TIMEOUT' in os.environ:
    gremlin_timeout = os.environ['RECORD_GREMLIN_TIMEOUT']

if 'RECORD_DEBUG' in os.environ:
    debug = True

#debug = True

mime = magic.Magic(mime=True)
encoding = magic.Magic(mime_encoding=True)

mimetypes_map = {} 

# Create a mimetype dictionary.
for (key, value) in iter(mimetypes.types_map.items()):
    mimetypes_map[value] = key

mimetypes_map["text/csv"] = ".csv"
mimetypes_map["text/x-perl"] = ".pl"
mimetypes_map["text/x-shellscript"] = ".sh"
mimetypes_map["application/x-directory"] = ""
mimetypes_map["application/x-executable"] = ""

# Regex for the LOCATOR field in Uses and Product
locator = re.compile('^(stdout|stderr|arg:[0-9]+|argid=.+|opt=.+|env=.+|in_file(=.+)?)$',re.IGNORECASE)

IPV6_or_IPV4_REGEX = re.compile(r"""
     # IPv6 RegEx
     (
          ([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|          # 1:2:3:4:5:6:7:8
          ([0-9a-fA-F]{1,4}:){1,7}:|                         # 1::                              1:2:3:4:5:6:7::
          ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|         # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
          ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|  # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
          ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|  # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
          ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|  # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
          ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|  # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
          [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|       # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8  
          :((:[0-9a-fA-F]{1,4}){1,7}|:)|                     # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::     
          fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|     # fe80::7:8%eth0   fe80::7:8%1     (link-local IPv6 addresses with zone index)
          ::(ffff(:0{1,4}){0,1}:){0,1}
          ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}
          (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|          # ::255.255.255.255   
                                                             # ::ffff:255.255.255.255  
                                                             # ::ffff:0:255.255.255.255  (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
          ([0-9a-fA-F]{1,4}:){1,4}:
          ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}
          (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])           # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
          )
     |
     # IPv4 RegEx
     (
          ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])
     )
""",re.VERBOSE)

# From https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
fqdn = re.compile(r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
#ip = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

tidySpace = re.compile(r'\s+')

ISO8601_REGEX = re.compile(
     r"""
     (?P<year>[0-9]{4})
     (
         (
             (-(?P<monthGdash>[0-9]{2}))
             |
             (?P<month>[0-9]{2})
             (?!$)  # Don't allow YYYYMM
         )
         (
             (
                 (-(?P<daydash>[0-9]{2}))
                 |
                 (?P<day>[0-9]{2})
             )
             (
                 (
                     (?P<separator>[T])
                     (?P<hour>[0-9]{2})
                     (:{0,1}(?P<minute>[0-9]{2})){0,1}
                     (
                         :{0,1}(?P<second>[0-9]{1,2})
                         ([.,](?P<second_fraction>[0-9]+)){0,1}
                     ){0,1}
                     (?P<timezone>
                         Z
                         |
                         (
                             (?P<tz_sign>[-+])
                             (?P<tz_hour>[0-9]{2})
                             :{0,1}
                             (?P<tz_minute>[0-9]{2}){0,1}
                         )
                     ){0,1}
                 ){0,1}
             )
         ){0,1}  # YYYY-MM
     ){0,1}  # YYYY only
     $
     """,re.VERBOSE)

gremlin_make_a_property = """
    mgmt = graph.openManagement()
    if (mgmt.getPropertyKey(name) == null) {
        mgmt.makePropertyKey(name).dataType(String.class).make()
    }
    mgmt.commit()
"""

gremlin_make_an_edge = """
    mgmt = graph.openManagement()
    if (mgmt.getEdgeLabel(name) == null) {
        mgmt.makeEdgeLabel(name).make()
    }
    mgmt.commit()
"""

gremlin_make_a_vertex = """
    mgmt = graph.openManagement()
    if (mgmt.getVertexLabel(name) == null) {
        mgmt.makeVertexLabel(name).make()
    }
    mgmt.commit()
"""

gremlin_make_an_id = """
    mgmt = graph.openManagement()
    if (mgmt.getPropertyKey(name) == null) {
        source = mgmt.makePropertyKey(name).dataType(String.class).make()
        mgmt.buildIndex(indexName, Vertex.class).addKey(source).unique().buildCompositeIndex()
        if (mgmt.getGraphIndex(indexName) == null) {
            idx = mgmt.buildIndex(indexName, Vertex.class).addKey(source).unique().buildCompositeIndex()
            mgmt.setConsistency(idx, ConsistencyModifier.LOCK)
        }
    }
    mgmt.commit()
"""

import rfc3987

def is_path(s: str) -> bool:
    return Path(s).exists()

def is_iri(s: str) -> bool:
    try:
        rfc3987.parse(s, rule='IRI')
        return True
    except ValueError:
        return False


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class InvalidEntity(Exception):
    pass

class GremlinDBError(Exception):
    pass

class GremlinVertexExists(Exception):
    pass

class Table:
    def __init__(self):
        self.DESCRIPTION = None
        self.NAME = None
        self.ABOUT = None
        self.CREATED = None
        self.CREATOR = None
        self.MODIFIER = None
        self.MODIFIED = None


    def getDict(self):
        return self.__dict__

    # The database is updated using the objects. There are 4 actions
    
    # exists - sees if the record is there
    # add - inserts a database row from the instance values
    # update - updates an existing row from the instance values
    # query - gets the values from the database and populates the instance

    # Originally the plan was to use the exception when you tried to add
    # something that was already there. This was causing too many log errors in
    # the database log on the cluster, which although not terminal may well
    # have masked a true error, so we have gone back to checking for existence
    # first. This is initially computationally more expensive, but stops
    # unnecessary writing to the database as it has been implemented
    # everywhere. Initially, admittedly I was trying to be clever and lazy - it
    # didn't work - sigh!

    def add(self, conn):
        cur = None
        if db_type == 'postgres' or db_type == 'sqlite3':
            cur = conn.cursor()    
        self.CREATOR = getpass.getuser()
        self.CREATED = datetime.datetime.now().isoformat()
        self.validate()
        matches = self.getPrimaryKeys()
        if matches == "":
            raise InvalidEntity(
                "ERROR: No primary key value provided on add for " 
                + self.__class__.__name__)

        fields = ""
        values = ""
        for key, value in self.__dict__.items():
            fields = fields + key + ","
            if value == None or value == (None,) or value == "":
                values = values + "null,"
            else:
                values = values + "'%s'," % value
        if db_type == 'postgres' or db_type == 'sqlite3':
            insertSQL = ('INSERT INTO ' + self.myTableName() + 
                     "(" + fields.strip(',') + ") VALUES (" + 
                    values.strip(',') + ')')
            if debug:
                sys.stderr.write("SQL add: " + insertSQL + '\n')
            cur.execute(insertSQL)
        else:
            query = ""
            vertex_id = ""
            localForeignKeys = []
            if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
                for foreignKey in self.foreignKeys():
                    localForeignKeys.append(foreignKey['sourceColumn'])
            for key, value in self.__dict__.items():
                if key in self.getPrimaryKeys() and value != None:
                    vertex_id = vertex_id + value + "_"
                elif self.__dict__[key.upper()] == None or self.__dict__[key.upper()] == '':
                    pass
                elif key in localForeignKeys:
                    pass 
                else:
                    query = query + ".property('" + key + "','" + gremlin_safe_string(str(value)) + "')" 
            if debug:
                sys.stderr.write("GREMLIN add: properties " + str(query) + "'\n")
            if vertex_id == "":
                raise GremlinDBError("No ID for an add")
            vertex_id = vertex_id.rstrip('_')
            if debug:
                sys.stderr.write("GREMLIN add: vertex = " + str(vertex_id) + "\n")
            if db_type == 'janusgraph':
                query = ("g.with('evaluationTimeout', " + 
                         str(gremlin_timeout) +
                         ").addV('" +
                         self.tableName() +
                         "').property('" +
                         str(self.primaryKeys()[0][0]) + 
                         "','" + 
                         vertex_id + 
                         "')" +
                         query
                )
            else:
                query = ("g.with('evaluationTimeout', " + 
                         str(gremlin_timeout) +
                         ").addV('" +
                         self.__class__.__name__ +
                         "').property(id, '" + 
                         vertex_id + 
                         "')" +
                         query
                )
            query += ".next()"
            result = gremlin_submit(conn, query, 'add')
            
            gremlin_wait_for_vertex(conn, vertex_id, key = self.primaryKeys()[0][0])
            # Now add the edges
            if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
                for foreignKey in self.foreignKeys():
                    if self.__dict__[foreignKey['sourceColumn']] != None and self.__dict__[foreignKey['sourceColumn']] != '':
                        method = getattr(Table, foreignKey['targetTable'])
                        if db_type == 'janusgraph':
                            query = ("g.with('evaluationTimeout', " + 
                                     str(gremlin_timeout) +
                                     ").V().has('" +
                                     str(foreignKey['targetColumn']) +
                                     "','" + 
                                     self.__dict__[foreignKey['sourceColumn']] + 
                                     "').addE('" + 
                                     method() + 
                                     "').to(__.V().has('" + 
                                     str(self.primaryKeys()[0][0]) + 
                                     "','" + 
                                     vertex_id + 
                                     "'))"
                            )
                        else:
                            query = ("g.with('evaluationTimeout', " + 
                                     str(gremlin_timeout) +
                                     ").V('" +
                                     self.__dict__[foreignKey['sourceColumn']] + 
                                     "').addE('" + 
                                     method() + 
                                     "').to(__.V('" + 
                                     vertex_id + 
                                     "'))"
                            )
                        query += ".next()"
                        edge = gremlin_submit(conn, query, 'edge')
            return result
        
    def exists(self,conn):

        if db_type == 'postgres' or db_type == 'sqlite3':
            cur = conn.cursor()
            matches = self.getPrimaryKeys()
            if matches == "":
                raise InvalidEntity(
                    "ERROR: SQL: No primary key value provided on exists for " 
                    + self.__class__.__name__)
            getSQL = ("SELECT *" +
                " FROM " + self.myTableName() +
                " WHERE " + matches)
            if debug:
                sys.stderr.write("SQL exists: " + getSQL + '\n')
            result = cur.execute(getSQL)
            row = cur.fetchone()
            if debug:
                sys.stderr.write("SQL exists: result contains " + str(row) + ".\n")
            if row == None:
                return False
            return True
        else:
            vertex_id = ""
            for key, value in self.__dict__.items():
                if debug:
                    sys.stderr.write("GREMLIN exists: key " + str(key) + " = " + str(value) + "\n")
                if key in self.getPrimaryKeys() and value != None and value != '':
                    vertex_id = vertex_id + value + "_"
            if vertex_id == "":
                raise GremlinDBError("GREMLIN exists: no ID for an add")
            vertex_id = vertex_id.strip("_")
            if debug:
                sys.stderr.write("GREMLIN exists: Primary key is " + str(vertex_id) + "\n")
            if db_type == 'janusgraph':
                query = ("g.with('evaluationTimeout', " + 
                        str(gremlin_timeout) + 
                        ").V().has('" +
                        str(self.primaryKeys()[0][0])  +
                        "','" + 
                        vertex_id + 
                        "')")
            else:
                query = ("g.with('evaluationTimeout', " + 
                        str(gremlin_timeout) + 
                        ").V('" + vertex_id + 
                        "').hasLabel('" + 
                        self.__class__.__name__ + 
                        "')")
            query += ".valueMap()"
            result = gremlin_submit(conn, query, 'exists')
            if len(result) == 0 or result[0] == 0:
                if debug:
                    sys.stderr.write("GREMLIN exists: FALSE\n")
                return False
            if debug:
                sys.stderr.write("GREMLIN exists: TRUE\n")
            return True
            
    def query(self,conn):
        matches = self.getPrimaryKeys()
        if matches == "":
            raise InvalidEntity(
                "ERROR: No primary key value provided on update for " 
                + self.__class__.__name__ + '\n')
        
        if db_type == 'postgres' or db_type == 'sqlite3':
            cur = conn.cursor()
            getSQL = ("SELECT *" +
                " FROM " + self.myTableName() +
                " WHERE " + matches)
            if debug:
                sys.stderr.write("SQL query: " + getSQL + '\n')
            curry = cur.execute(getSQL)
            row = cur.fetchone()
            if debug:
                sys.stderr.write("SQL query: keys " + str(row.keys()) + '\n')
            for key in row:
                if debug:
                    sys.stderr.write("SQL query: " + str(key.upper()) + " = " + str(row[key]) + '\n')
                self.__dict__[key.upper()] = row[key]
        else:
            vertex_id = ""
            localForeignKeys = []
            if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
                for foreignKey in self.foreignKeys():
                    localForeignKeys.append(foreignKey['sourceColumn'])
                if debug:
                    sys.stderr.write("GREMLIN query: Foreign key = " + str(localForeignKeys) + "\n")
            if debug:
                sys.stderr.write("GREMLIN query: Primary keys = " + str(self.getPrimaryKeys()) + "\n")
            vertex_id = ""
            for key, value in self.__dict__.items():
                if value != None:
                    if debug:
                        sys.stderr.write("GREMLIN query self: " + str(key) + " = " + str(value) + "\n")
                    if key in self.getPrimaryKeys():
                        if debug:
                            sys.stderr.write("GREMLIN query key: " + str(key) + " = " + str(value) + "\n")
                        vertex_id = vertex_id + value + "_"
            if vertex_id == "":
                raise GremlinDBError("GREMLIN query: No ID for an add")
            vertex_id = vertex_id.strip("_")
            if debug:
                sys.stderr.write("GREMLIN query: Primary key is " + str(vertex_id) + "\n")
            if db_type == 'janusgraph':
                query = ("g.with('evaluationTimeout', " +  
                        str(gremlin_timeout) + 
                        ").V().has('" + 
                        str(self.primaryKeys()[0][0]) +
                        "','" +
                        vertex_id + 
                        "')")
            else:
                query = ("g.with('evaluationTimeout', " +  
                        str(gremlin_timeout) + 
                        ").V('" + 
                        vertex_id + 
                        "')")
            query += ".valueMap()"
            result = gremlin_submit(conn, query, 'query')
            if len(result) > 0:
                for key in result[0].keys():
                    if result[0][key][0] == "None":
                        self.__dict__[key.upper()] = None
                    else:
                        self.__dict__[key.upper()] = result[0][key][0]

            # Now deal with edges        
            if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
                for key in self.foreignKeys():
                    method = getattr(Table, key['targetTable'])
                    if db_type == 'janusgraph':
                        query = ("g.with('evaluationTimeout', " +  
                                str(gremlin_timeout) + 
                                ").V().has('" +
                                str(self.primaryKeys()[0][0]) +
                                "','" +
                                vertex_id + 
                                "').inE('" + 
                                method() +
                                "').outV()" 
                        )
                    else:
                        query = ("g.with('evaluationTimeout', " +  
                                str(gremlin_timeout) + 
                                ").V('" +
                                vertex_id + 
                                "').inE('" + 
                                method() +
                                "').outV()" 
                        )
                    query += ".toList()"
                    edge = gremlin_submit(conn, query, 'edge')
                    if len(edge) == 0:
                        self.__dict__[key['sourceColumn'].upper()] = None
                    else:
                        if db_type == 'janusgraph':
                            query = "g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V(" + str(edge[0].id) + ").values('" + key['targetColumn'] + "').next()"
                            value = gremlin_submit(conn, query, 'value')
                            self.__dict__[key['sourceColumn'].upper()] = value[0]
                        else:
                            self.__dict__[key['sourceColumn'].upper()] = edge[0].id

    def search(self,conn,equals):
        """
        """
        keys = None

        match = ""
        for column, value in equals.items():
            if db_type == "gremlin":

                if column.lower().startswith('id_'):
                    match = match + ".hasId('" + value + "')"
                else:
                    match = match + ".has('" + column + "','" + value + "')"
            else:
                if match == "":
                    if any(ch in "%_{}[]^" for ch in value):
                        match = column + " LIKE '" + str(value) + "'"
                    else:
                        match = column + " = '" + str(value) + "'"
                else:
                    if debug:
                        sys.stderr.write("SQL: search value " + str(value) + "\n")
                    if any(ch in "%_{}[]^" for ch in value):
                        match = match + " AND " + column + " LIKE '" + str(value) + "'"
                    else:
                        match = match + " AND " + column + " = '" + str(value) + "'"

        if db_type != "gremlin":

            cur = conn.cursor()

            for keyset in self.myPrimaryKeys():
                for column in keyset:
                    keys = column + ','

            searchSQL = ("SELECT " + keys.strip(',') +
                " FROM " + self.myTableName() +
                " WHERE " + match)
            if debug:
                sys.stderr.write(searchSQL + '\n')
            curry = cur.execute(searchSQL)
            return cur.fetchall()
        else:
            query = ("g.with('evaluationTimeout', " +
                    str(gremlin_timeout) +
                    ").V().hasLabel('" +
                    self.__class__.__name__ +
                    "')" + match +
                    '.id().iterate()')
            result = gremlin_submit(conn, query, 'search')
            return result

    def update(self,conn):
        self.MODIFIER = getpass.getuser()
        self.MODIFIED = datetime.datetime.now().isoformat()
        self.validate(True)
        set_values = ""
        vertex_id = ""
        row = self.getDict()
        localForeignKeys = []
        if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
            for foreignKey in self.foreignKeys():
                localForeignKeys.append(foreignKey['sourceColumn'])
        for key in row.keys():
            if db_type == 'postgres' or db_type == 'sqlite3':
                if self.__dict__[key.upper()] == None or self.__dict__[key.upper()] == '':
                    pass
                    #set_values = (set_values + key + "=null,")
                elif (self.__dict__[key.upper()] != None and 
                    isinstance(self.__dict__[key.upper()], int)):
                    set_values = (set_values + key + "=" + 
                        str(self.__dict__[key.upper()]) + ",")
                elif (self.__dict__[key.upper()] != None and 
                    isinstance(self.__dict__[key.upper()], datetime.date)):
                    set_values = (set_values + key + "='" + 
                        str(self.__dict__[key.upper()]) + "',")
                else:
                    set_values = (set_values + key + "='" + 
                        self.__dict__[key.upper()] + "',")
            else:
                if self.__dict__[key.upper()] == None or self.__dict__[key.upper()] == '':
                    pass
                elif key in self.getPrimaryKeys():
                    vertex_id = vertex_id + self.__dict__[key.upper()] + "_"
                elif key.upper() not in localForeignKeys:
                    set_values = (set_values + ".property('" + 
                             key.upper() +
                             "','" +
                             gremlin_safe_string(str(self.__dict__[key.upper()])) +
                             "')" )
        set_values = set_values.strip(',')
        if debug:
            sys.stderr.write("set_values = " + str(set_values) + " and vertex_id = " + str(vertex_id) + "\n")

        if db_type == 'postgres' or db_type == 'sqlite3':
            cur = conn.cursor()
            matches = self.getPrimaryKeys()
            if matches == "":
                raise InvalidEntity(
                    "ERROR: No primary key value provided on update for " 
                    + self.__class__.__name__)
            updateSQL = ('UPDATE ' + self.myTableName() + 
                 ' SET ' + set_values + 
                 ' WHERE ' + matches)
            if debug:
                sys.stderr.write("SQL update: " + updateSQL + '\n')
            try:
                cur.execute(updateSQL)
            except:
                sys.stderr.write("SQL update: Class: " + self.__class__.__name__ +
                      "Key: " + matches + ": Unable to update\n")
                raise
        else:
            vertex_id = vertex_id.strip('_')
            if vertex_id == "":
                raise GremlinDBError("GREMLIN update: No ID for an add")
            if db_type == 'janusgraph':
                query = ("g.with('evaluationTimeout', " + 
                        str(gremlin_timeout) +
                        ").V().has('" + 
                        str(self.primaryKeys()[0][0]) +
                        "','" + 
                        vertex_id + 
                        "')" +
                        set_values )
            else:
                query = ("g.with('evaluationTimeout', " + 
                        str(gremlin_timeout) +
                        ").V('" + 
                        vertex_id + 
                        "')" +
                        set_values )
            query = re.sub(r'\\', '', query)
            query += ".next()"
            result = gremlin_submit(conn, query, 'update')
            # Now deal with edges
            if hasattr(self, 'foreignKeys') and callable(getattr(self, 'foreignKeys')):
                for key in self.foreignKeys():
                    if self.__dict__[key['sourceColumn']] != None and self.__dict__[key['sourceColumn']] != '':
                        if db_type == 'janusgraph':
                            query = ("g.with('evaluationTimeout', " +  
                                    str(gremlin_timeout) + 
                                    ").V().has('" + 
                                    str(key['targetColumn']) +
                                    "','" +
                                    vertex_id +
                                    "').inE('" +
                                    str(key['targetTable']).upper() +
                                    "').property('name', '" + 
                                    self.__dict__[key['sourceColumn']] +
                                    "')" )
                        else:
                            query = ("g.with('evaluationTimeout', " +  
                                    str(gremlin_timeout) + 
                                    ").V('" + 
                                    vertex_id +
                                    "').inE('" +
                                    str(key['targetTable']).upper() +
                                    "').property('name', '" + 
                                    self.__dict__[key['sourceColumn']] +
                                    "')" )
                        query += ".iterate()"
                        edge = gremlin_submit(conn, query, 'edge')
            self.query(conn)
            return result

    def getPrimaryKeys(self):
        for keyset in self.myPrimaryKeys():
            matches = ""
            incomplete = False
            for column in keyset:
                
                if self.__dict__[column] == None:
                    incomplete = True
                    break
                elif (matches != "" and
                    self.__dict__[column] != None and 
                    isinstance(self.__dict__[column], int)):
                    matches = (matches + " AND " + 
                            column + " = " + 
                        str(self.__dict__[column]))

                elif matches != "":
                    matches = (matches + " AND " + 
                        column + " = '" + 
                        self.__dict__[column] + "'")
                elif (self.__dict__[column] != None and 
                    isinstance(self.__dict__[column], int)):
                    matches = (column + " = " + 
                        str(self.__dict__[column]))

                else:
                    matches = (column + " = '" + 
                        self.__dict__[column] + "'")
            if incomplete == False:
                break;
            
        # Error condition is the an empty matches
        return matches
    @classmethod
    def count(cls, conn):
        cur = conn.cursor()
        someSQL = ("SELECT COUNT(*) " +
            " FROM " + cls.tableName())
        if debug:
            sys.stderr.write("SQL count: " + someSQL + '\n')
        curry = cur.execute(someSQL)
        row = cur.fetchone()
        count = 0
        for key in row:
            count = row[key]
        return count


    @classmethod
    def getAttributes(cls):
        someObj = cls()
        return someObj.getDict().keys()

    @classmethod 
    def markdown(cls):
        markdown = "# " + str(cls.__name__) + "\n\n"
        if cls.is_relation():
            markdown = markdown + "This is reification. In the graph database, this will appear as an edge between two entites. In a relational database, this will be a relation which allows the enumeration of the many-to-many linkage.\n\n"

        for k,v in cls.documentation().items():
            markdown = markdown + "## " + str(k) + "\n\n"
            markdown = markdown + str(v) + "\n\n"

        localForeignKeys = []
        if hasattr(cls, 'foreignKeys') and callable(getattr(cls, 'foreignKeys')):
            for foreignKey in cls.foreignKeys():
                localForeignKeys.append(foreignKey['sourceColumn'])
        if len(cls.columns()) - len(localForeignKeys) > 0:
            markdown = markdown + "\n##  Attributes\n\n"
            markdown = markdown + ("| Field    |Property| Value                   |\n" +
                                   "|----------|--------|-------------------------|\n")
            for entity in cls.columns():
                for attribute, valuePairs in entity.items():
                    if not attribute in localForeignKeys:
                        firstLine = True
                        for k,v in valuePairs.items():
                            if firstLine:
                                firstLine = False
                                if len(attribute) > 14:
                                    markdown = markdown + "| " + attribute + " |  | |\n" + "|  | " + str(k) + " | " + str(v) + "|\n"
                                else:
                                    markdown = markdown + "| " + attribute + " | " + str(k) + " | " + str(v) + "|\n"
                            else:
                                markdown = markdown + "|  | " + str(k) + " | " + str(v) + "|\n"
            markdown += "\n"
        if len(localForeignKeys) > 0:
            markdown = markdown + "##  Relationships\n\n"
            markdown = markdown + ("| Field    |Property| Value                   |\n" +
                                   "|----------|--------|-------------------------|\n")
            for entity in cls.columns():
                for attribute, valuePairs in entity.items():
                    if attribute in localForeignKeys:
                        firstLine = True
                        for k,v in valuePairs.items():
                            if firstLine:
                                firstLine = False
                                if len(attribute) > 14:
                                    markdown = markdown + "| " + attribute + " |  | |\n" + "|  | " + str(k) + " | " + str(v) + "|\n"
                                else:
                                    markdown = markdown + "| " + attribute + " | " + str(k) + " | " + str(v) + "|\n"
                            else:
                                markdown = markdown + "|  | " + str(k) + " | " + str(v) + "|\n"
            markdown += "\n"
        return markdown
    @classmethod
    def is_relation(cls):
        return False
   
    def set_values(self, values = None):
        if values != None:
            for key in values:
                if key.upper() in self.getDict():
                    self.__dict__[key.upper()] = values[key]
                else:
                    raise InvalidEntity("ERROR: Class: " + 
                        self.__class__.__name__ + 
                        ": Invalid column: " + 
                        key +
                        '\n') 


    def validate(self, update=False):
        id_name = None 
        id_value = ""
        try:
            id_name, id_value = next( (k, v) for k, v in self.__dict__.items() if k.startswith("ID_"))
        except Exception:
            pass
        if id_name != None:
            id_name_part = id_name[len("id_"):].lower()   
            if id_name_part not in id_value.lower():
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Invalid column: SELF.' +
                    id_name + 
                    ' = ' +
                    id_value +
                    '\n')
        if (self.ABOUT != None and 
        not rfc3987.match(self.ABOUT, "Absolute_IRI") and
        not rfc3987.match(self.ABOUT, "Absolute_URI")):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: ABOUT = ' +
                str(self.ABOUT) +
                '\n')
        if ( self.CREATED != None and
        not iso8601(str(self.CREATED))):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: CREATED = ' +
                str(self.CREATED) +
                '\n')
        if (self.MODIFIED != None and 
            not iso8601(self.MODIFIED)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: MODIFIED = ' +
                str(self.MODIFIED) +
                '\n')


    def myPrimaryKeys(self):
        return self.__class__.primaryKeys()

    def myTableName(self):
        return self.__class__.tableName()

    def commonFields():
        return [
            {
                "CREATED" : {
                    "Type"          : "DATE",
                    "Constraint"    : "NOT NULL",
                    "Description"   : "Creation datetime",
                    "Standards"     : "dc:created, ISO8601",
                    "Validation"    : "Logical datetime",
                    "Automation"    : "Auto"
                }
            },
            {
                "CREATOR" : {
                    "Type"          : "TEXT",
                    "Constraint"    : "NOT NULL",
                    "Description"   : "Who created this relation",
                    "Standards"     : "dc:creator",
                    "Validation"    : "String",
                    "Automation"    : "Auto by system user"
                }
            },
            {
                "MODIFIED": {
                    "Type"          : "DATE",
                    "Description"   : "Modification datetime",
                    "Standards"     : "dc:modified, ISO8601",
                    "Validation"    : "Must be after created",
                    "Automation"    : "Auto"
                }
            },
            {
                "MODIFIER": {
                    "Type"          : "TEXT",
                    "Description"   : "Who modified this relation",
                    "Standards"     : "dc:creator",
                    "Validation"    : "String",
                    "Automation"    : "Auto"
                }
            },
            {
                "DESCRIPTION": {
                    "Type"          : "TEXT",
                    "Description"   : "Short text to use to summarise what the argument is",
                    "Standards"     : "None",
                    "Validation"    : "String",
                    "Automation"    : "None"
                }
            },
            {
                "NAME": {
                    "Type"          : "TEXT",
                    "Description"   : "A documentary name for the relation",
                    "Standards"     : "None",
                    "Validation"    : "None. May or may not be present",
                    "Automation"    : "None"
                }
            },
            {
                "ABOUT": {
                    "Type"          : "TEXT",
                    "Description"   : "A unique resource identifier allowing inward linking",
                    "Standards"     : "RFC 3987, RFC 4622",
                    "Validation"    : "IRI",
                    "Automation"    : "None"
                }
            }
        ]

    @classmethod
    def schema(cls):
        schema = "CREATE TABLE IF NOT EXISTS " + cls.tableName() + " ("
        keysUsed = []
        for fieldDefinition in Table.commonFields():
            for field, properties in fieldDefinition.items():
                schema = schema + field + " " + properties['Type'] 
                if 'Constraint'  in properties:
                    schema = schema + " " + properties['Constraint']
                schema = schema + ","
                keysUsed.append(field)
        simplePrimaryKey = False
        primaryKeySchema = ""
        if hasattr(cls, 'primaryKeys') and callable(getattr(cls, "primaryKeys")):
            primaryKeys = cls.primaryKeys()
            if len(primaryKeys) == 1 and len(primaryKeys[0]) == 1:
                simplePrimaryKey = True
            elif len(primaryKeys) == 1:
                primaryKeySchema = "PRIMARY KEY (" + ",".join(primaryKeys[0]) + "),"
            else:
                for uniqueValue in primaryKeys:
                    primaryKeySchema = primaryKeySchema + " CONSTRAINT For_" + "_".join(uniqueValue) + " UNIQUE(" + ",".join(uniqueValue) + "),"
        for fieldDefinition in cls.columns():
            for field, properties in fieldDefinition.items():
                if not field in keysUsed:
                    schema = schema + field + " " + properties['Type'] 
                    if simplePrimaryKey == True and field == primaryKeys[0][0]:
                        schema = schema + " PRIMARY KEY "
                    elif 'Constraint'  in properties:
                        schema = schema + " " + properties['Constraint']
                    schema = schema + ","
                    keysUsed.append(field)
        if simplePrimaryKey == False:
            schema = schema + primaryKeySchema
        schema = schema[:-1] + ")"
        return schema

    @classmethod
    def create_table(cls, conn):
        if db_type == 'gremlin':
            sys.stderr.write("GREMLIN create_table: meaningless in a tinkerpop graph database.\n")
            raise
        elif db_type == 'janusgraph':
            foreignKeys = []
            if hasattr(cls, 'foreignKeys') and callable(getattr(cls, "foreignKeys")):
                for keyset in cls.foreignKeys():
                    bindings = { "name": str(keyset['targetTable']) }
                    foreignKeys.append(str(keyset['sourceColumn']))
                    if debug:
                        sys.stderr.write("JANUSGRAPH: create_table: foreign edge " + gremlin_make_an_edge+ " with bindings " + str(bindings) + ".\n")
                    conn.submit(gremlin_make_an_edge, bindings = bindings).all().result()
            if cls.is_relation():
                bindings = { "name": str(cls.tableName()) }
                if debug:
                    sys.stderr.write("JANUSGRAPH: create_table: edge: " + gremlin_make_an_edge + " with bindings " + str(bindings) + ".\n")
                conn.submit(gremlin_make_an_edge, bindings = bindings).all().result()
                # Poopy-doop, no properties
                for entity in cls.columns():
                    for attribute, valuePairs in entity.items():
                        if attribute in foreignKeys:
                            pass
                        elif hasattr(cls, 'primaryKeys') and callable(getattr(cls, "primaryKeys")) and cls.primaryKeys()[0][0] == attribute:
                            pass
                        else:
                            bindings = { "name": attribute }
                            if debug:
                                sys.stderr.write("JANUSGRAPH: create_table: edge property " + gremlin_make_a_property + " with bindings " + str(bindings) + ".\n")
                            conn.submit(gremlin_make_a_property, bindings = bindings).all().result()
            else:
                # Lets do vertex first
                bindings = { "name": str(cls.__name__) }
                if debug:
                    sys.stderr.write("JANUSGRAPH: create_table: vertex " + gremlin_make_a_vertex + " with bindings " + str(bindings) + ".\n")
                conn.submit(gremlin_make_a_vertex, bindings = bindings).all().result()
                # Finally the relationships
                # Now the properties
                for entity in cls.columns():
                    for attribute, valuePairs in entity.items():
                        if attribute in foreignKeys:
                            pass
                        elif cls.primaryKeys()[0][0] == attribute:
                            bindings = { "name" : cls.primaryKeys()[0][0] , "indexName" : "by" + cls.primaryKeys()[0][0] }
                            if debug:
                                sys.stderr.write("JANUSGRAPH: create_table: id " + gremlin_make_an_id + " with bindings " + str(bindings) + ".\n")
                            conn.submit(gremlin_make_an_id, bindings = bindings).all().result()
                        else:
                            bindings = { "name": attribute }
                            if debug:
                                sys.stderr.write("JANUSGRAPH: create_table: property " + gremlin_make_a_property + " with bindings " + str(bindings) + ".\n")
                            conn.submit(gremlin_make_a_property, bindings = bindings).all().result()
        else:
            cur = conn.cursor()
            schema = cls.schema()
            if debug:
                sys.stderr.write("SQL create_table: " + schema + '\n')
            cur.execute(schema)
            conn.commit()


    @classmethod
    def alter_table(cls, conn):
        with conn:
            if db_type == "gremlin":
                sys.stderr.write("GREMLIN alter_table: meaningless in a tinkerpop graph database.\n")
                raise
            cur = conn.cursor()
            sql = ""
            for key in cls.foreignKeys():
                sql = (sql + 
                       "ALTER TABLE " + 
                       key['sourceTable'] + 
                       ' ADD CONSTRAINT fk_' + 
                       key['sourceColumn'].lower() + 
                       '_' +
                       key['targetColumn'].lower() + 
                       ' FOREIGN KEY (' + 
                       key['sourceColumn'] +
                       ') REFERENCES ' + 
                       key['targetTable'] +
                       '(' +
                       key['targetColumn'] +
                       ')  DEFERRABLE INITIALLY DEFERRED;\n'
            )
            if debug:
                sys.stderr.write("SQL alter_table: " + sql + "\n")
            cur.execute(sql)
            conn.commit()
            for fieldDefinition in cls.columns():
                for field, values in fieldDefinition.items():
                    if 'Nullable' in values.keys():
                        if values["Nullable"] == True:
                            sql = "ALTER TABLE " + cls.tableName() + " ALTER COLUMN " + str(field) + " DROP NOT NULL"
                            if debug:
                                sys.stderr.write("SQL alter_table: " + sql + "\n")
                            cur.execute(sql)
                            conn.commit()
            
            

    @classmethod
    def truncate_table(cls, conn):
        if db_type == 'sqlite3' or db_type == 'postgres':
                cur = conn.cursor()
                query = "truncate table " + cls.tableName() + " cascade"
                if debug:
                    sys.stderr.write("SQL truncate_table: " + query + '\n')
                cur.execute(query)
                conn.commit()
        else:
            raise Exception(f"Trying to truncate an unsuitable database {db_type}.\n")

    @classmethod
    def dropTable(cls,conn):
        with conn:
            if db_type == "gremlin":
                sys.stderr.write("GREMLIN dropTable: " + str(cls) + " is meaningless in a tinkerpop graph database.\n")
                raise
            cur = conn.cursor()
            query = "drop table " + cls.tableName() + " cascade"
            if debug:
                sys.stderr.write("SQL dropTable: " + query + '\n')
            cur.execute(query)
            conn.commit()


    @staticmethod
    def Applications():
        return "Application"
    @staticmethod
    def Arguments():
        return "Argument"
    @staticmethod
    def ArgumentValues():
        return "ArgumentValue"
    @staticmethod
    def Assumes():
        return "Assumes"
    @staticmethod
    def Assumptions():
        return "Assumption"
    @staticmethod
    def Computers():
        return "Computer"
    @staticmethod
    def Boxes():
        return "Box"
    @staticmethod
    def BoxTypes():
        return "BoxType"
    @staticmethod
    def Contents():
        return "Content"
    @staticmethod
    def Contexts():
        return "Context"
    @staticmethod
    def Contributors():
        return "Contributor"
    @staticmethod
    def Dependencies():
        return "Dependency"
    @staticmethod
    def Documentation():
        return "Documentation"
    @staticmethod
    def Employs():
        return "Employs"
    @staticmethod
    def Entailments():
        return "Entailment"
    @staticmethod
    def Implements():
        return "Implements"
    @staticmethod
    def Inputs():
        return "Input"
    @staticmethod
    def Involvements():
        return "Involvement"
    @staticmethod
    def Meets():
        return "Meets"
    @staticmethod
    def Models():
        return "Model"
    @staticmethod
    def Parameters():
        return "Parameter"
    @staticmethod
    def Persons():
        return "Person"
    @staticmethod
    def PersonalData():
        return "PersonalData"
    @staticmethod
    def Pipelines():
        return "Pipeline"
    @staticmethod
    def Processes():
        return "Process"
    @staticmethod
    def Products():
        return "Product"
    @staticmethod
    def Projects():
        return "Project"
    @staticmethod
    def Requirements():
        return "Requirement"
    @staticmethod
    def Specifications():
        return "Specification"
    @staticmethod
    def StatisticalInputs():
        return "StatisticalInput"
    @staticmethod
    def StatisticalMethods():
        return "StatisticalMethod"
    @staticmethod
    def StatisticalVariables():
        return "StatisticalVariable"
    @staticmethod
    def Statistics():
        return "Statistics"
    @staticmethod
    def Studies():
        return "Study"
    @staticmethod
    def Tags():
        return "Tag"
    @staticmethod
    def TagMaps():
        return "TagMap"
    @staticmethod
    def Users():
        return "User"
    @staticmethod
    def Uses():
        return "Uses"
    @staticmethod
    def Value():
        return "Value"
    @staticmethod
    def Variables():
        return "Variable"
    @staticmethod
    def Visualisations():
        return "Visualisation"
    @staticmethod
    def VisualisationMethods():
        return "VisualisationMethod"
    @staticmethod
    def VisualisationValues():
        return "VisualisationValue"

# Specialisation of PROV:Entity
class Application(Table):
    @classmethod
    def documentation(cls):
        return { 
            "Description" : "An `Application` is something that can be run by the user to generate or analyse simulation output.",
            "Standards"  : """`PROV:Entity`. Note the potential confusion. An `Application` is something that has the potential to be an activity (in the PROV sense) in the form of a `Process`. However, PROV only deals with the past, not with potential. The `Application` is a file somewhere, and hence an entity.""",
            "Automation": "Most of this table is expected to be populated by the user."
        }
    @classmethod
    def columns(cls):
        return [ 
            { "ID_APPLICATION": 
                { "Type"        : "TEXT", 
                  "Description" : "Unique key",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instatiating framework" 
                } 
            },
            { "PURPOSE":
                { "Type"        : "TEXT", 
                  "Description" : "Description of the purpose of the application",
                  "Standards"   : "?",
                  "Validation"  : "Free text",
                  "Automation"  : "None" 
                }
            },
            { "VERSION":
                { "Type"        : "TEXT", 
                  "Description" : "Version ID for the application",
                  "Standards"   : "dc:?",
                  "Validation"  : "String (e.g. CHAR(32))",
                  "Automation"  : "None"
                }
            },
            { "LICENCE" :
                { "Type"        : "TEXT",
                  "Description" : "Software licence for the application",
                  "Standards"   : "dc:license",
                  "Validation"  : "Free text with the option to select from other entries",
                  "Automation"  : "None"
                }
            },
			{ "LANGUAGE" : 
                { "Type"        : "TEXT",
                  "Description" : "Programming language the application was written in",
                  "Standards"   : "?",
                  "Validation"  : "Free text with the option to select from other entries",
                  "Automation"  : "None"
                }
            },
            { "ENVS" :
                { "Type"        : "TEXT",
                  "Description" : "The environment variables that should be recorded when the application is run",
                  "Standards"   : "None",
                  "Validation"  : "List of strings",
                  "Automation"  : "None"
                }
            },
            { "SEPARATOR" :
                { "Type"        : "TEXT",
                  "Description" : "Separator used when supplying arguments to the application",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
			{ "REVISION" : 
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of `Application` this `Application` is a revision of, if any.",
                  "Standards"   : "`PROV:wasDerivedFrom`; `dc:isVersionOF`",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "If not a revision of anoth `Application`.",
                  "Automation"  : "None"
                }
            },
			{ "MODEL" : 
                { "Type"        : "TEXT",
                  "Description" : "ID in `Model` table this `Application` is, if it is a `Model`.",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID in `Model`.",
                  "Null"        : "If this `Application` is not a model.",
                  "Automation"  : "None"
                }
            },
			{ "LOCATION" : 
                { "Type"        : "TEXT", 
                  "Description" : "ID_BOX in the `Box` table to use to find this `Application`.",
                  "Standards"   : "?",
                  "Validation"  : "Must be ID_BOX of a `Box`.",
                  "Null"        : "If the search for a `Box` for this `Application` has not been done.",
                  "Automation"  : """This should be populated automatically the first time the `Application` is requested on a host by finding the most local `Box` that references it, and storing that here.

If the most local `Box` is not on the current host, then the `Application` should be downloaded to the current host, and a new `Box` created for the location.

If the Box ID is no longer present, then the search should be repeated in the `Box` table.
                  """
                }
            }
       ]
    @classmethod
    def foreignKeys(cls):
        return [ { 'sourceTable' : 'Applications', 'sourceColumn' : 'LOCATION', 'targetTable' : 'Boxes',        'targetColumn' : 'ID_BOX', },
                 { 'sourceTable' : 'Applications', 'sourceColumn' : 'MODEL',    'targetTable' : 'Models',       'targetColumn' : 'ID_MODEL', },
                 { 'sourceTable' : 'Applications', 'sourceColumn' : 'REVISION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION', } ]

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_APPLICATION" ] ]

    def __init__(self, values = None):

        Table.__init__(self)
        self.ID_APPLICATION = None
        self.PURPOSE = None
        self.VERSION = None
        self.LICENCE = None
        self.LANGUAGE = None
        self.SEPARATOR = None
        self.ENVS = None
        self.REVISION = None # Foreign key in table Applications
        self.MODEL =    None # Foreign key in table Models
        self.LOCATION = None # Foreign key in table Boxes
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Applications"

    def validate(self, update=False):
        Table.validate(self)
        # TODO
        # language: dc:language
        # envs: regex based on:
        # for Unix:
        #      ENV_VAR1=some_value ENV_VAR2=some_other_value exectuable
        # or for Windows
        #      cmd /C "set ENV_VAR1=some_value && ENV_VAR2=some_other_value exectuable
        pass

class Argument(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description"   : """A command-line argument accepted by an `Application`. Commands vary hugely in how they parse arguments on the command line, and this table needs to make clear how to build a command line that the `Application` can use. To be clear, a command line is a string of text that is given to a shell (DOS, bash, etc.) to initiate a batch job.""",
            "Standards"     : """POSIX.1-2008 and equivalently IEEE Std 1003.1-2008/Cor 1-2013 are normative for Unix environments, but cannot be assumed even for Unix environments. Cross-platform support is in any case needed.""",
            "Automation"    : """When building up a command-line for an `Application` with arguments during invocation of a `Process`, the system should do the following:
- Let M be a map from integer to list of string.
- For each flag, check with the user to see whether it should be set or cleared; if set, add the flag name to M, using the order as the key, or -1 if the order is null. Create an entry in ArgumentValue using ‘true’ or ‘false’ as the value according to whether or not the flag is set.
- For each option, check with the user to see whether it should be used, and if so, provide an appropriate argument or arguments in accordance with the arity. Build a string for the option including its name and arguments, bearing in mind the separator and argsep values. Add the resulting string to M.
- For each required argument, request a value or values from the user in accordance with the arity. Build a string accordingly and add to M.
- Let K be a sorted list of keys of M.
- Let C be a string.
- For each key, join its list of strings with space and concatenate to C.
- C contains the command-line argument string."""
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_ARGUMENT":
                { "Type"        : "TEXT",
                  "Description" : "Unique key",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "TYPE":
                { "Type": "TEXT",
                  "Description" : "The kind of command line argument this is. Required arguments must be provided, typically don’t have a name, and are identified by their number. Options typically have a name, which if given stipulates some sort of value must be provided. Flags are options with arity 0.",
                  "Standards"   : "None",
                  "Validation"  : "One of “required”, “option”, or “flag”",
                  "Automation"  : "None"
                }
            },
            { "ORDER_VALUE":
                { "Type"        : "INTEGER",
                  "Description" : "A number used to indicate any order in which this `Argument` should appear in relation to other `Argument`s the `Application` accepts.",
                  "Standards"   : "None",
                  "Validation"  : "Non-negative integer or null if the order is unimportant.",
                  "Automation"  : "None"
                }
            },
            { "ASSIGNMENT_OPERATOR":
                { "Type"        : "TEXT",
                  "Description" : "Separator to use between argument name and value.",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "NAME":
                { "Type"        : "TEXT",
                  "Description" : "The name of the argument, including any grammar to indicate on the command-line that it is an argument (such as –– or – or /).",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "SEPARATOR":
                { "Type"        : "TEXT",
                  "Description" : "This is the character that indicates the argument name (e.g. --input, -input, /input).",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "SHORT_NAME":
                { "Type"        : "TEXT",
                  "Description" : "The short name of the argument, including any grammar to indicate on the command-line that it is an argument (such as –– or – or /). For example in *nix system -h and --help are the same parameter.",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "SHORT_SEPARATOR":
                { "Type"        : "TEXT",
                  "Description" : "This is the character that indicates the argument name (e.g. --input, -input, /input). for example in *nix system -h and --help are the same parameter.",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
           },
           { "DESCRIPTION":
                { "Type"        : "TEXT",
                  "Description" : "Short text to use to summarise what the argument is",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
           },
           { "ARITY":
               { "Type"        : "TEXT",
                  "Description" : "Number of arguments expected. Can be integer, ?, + or *.",
                  "Standards"   : "None",
                  "Validation"  : "?, + or *, or integer string. Constraints apply.",
                  "Automation"  : "None"
                }
            },
            { "ARGSEP":
                { "Type"        : "TEXT",
                  "Description" : "Separator to use between arguments if arity > 1",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "RANGE":
                { "Type"        : "TEXT",
                  "Description" : "Description of the range of any value to be supplied by the user",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "The application this argument applies to.",
                  "Standards"   : "None",
                  "Validation"  : "ID in the `Application` table.",
                  "Null"        : "Null if not an argument for an `Application`",
                  "Automation"  : "None"
                }
             },
             { "VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "The variable this argument relates to.",
                  "Standards"   : "None",
                  "Validation"  : "ID in the `Variable`s table.",
                  "Null"        : "Null if not about a variable",
                  "Automation"  : "None"
                }
             },
             { "BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "The `BoxType` this argument might be, if it is a file or somesuch.",
                  "Standards"   : "None",
                  "Validation"  : "ID in the `BoxType`s table.",
                  "Null"        : "Null if this does not have a `BoxType` associated iwth it.",
                  "Automation"  : "None"
                }
             }
         ]
    @classmethod
    def foreignKeys(cls):
            return [{ 'sourceTable' : 'Arguments', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION'},
                    { 'sourceTable' : 'Arguments', 'sourceColumn' : 'VARIABLE',    'targetTable' : 'Variables',    'targetColumn' : 'ID_VARIABLE' }, 
                    { 'sourceTable' : 'Arguments', 'sourceColumn' : 'BOX_TYPE',    'targetTable' : 'BoxTypes',     'targetColumn' : 'ID_BOX_TYPE' }]

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_ARGUMENT" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_ARGUMENT = None
        self.TYPE = None
        self.ORDER_VALUE = None
        self.ASSIGNMENT_OPERATOR = None
        self.SEPARATOR = None
        self.SHORT_NAME = None
        self.SHORT_SEPARATOR = None
        self.ARITY = None
        self.ARGSEP = None
        self.RANGE = None
        self.VARIABLE = None # Foreing key in table Variables
        self.BOX_TYPE = None # Foreign key in table BoxTypes 
        self.APPLICATION = None # Foreign key in table Applications
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Arguments"

    def validate(self, update=False):
        Table.validate(self)
        if (update == True and self.TYPE == None):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: TYPE: ' +
                str(self.TYPE))
        if (update == False and 
            self.TYPE.lower() != 'required' and    
            self.TYPE.lower() != 'option' and 
            self.TYPE.lower() != 'flag'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: TYPE: ' +
                str(self.TYPE))
        if (self.ORDER_VALUE != None and
            not is_positive_int(self.ORDER_VALUE)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: ORDER_VALUE: ' +
                str(self.ORDER_VALUE))
        if (self.SHORT_SEPARATOR != None and
            self.SHORT_SEPARATOR != '/' and
            self.SHORT_SEPARATOR != '-'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: SHORT_SEPARATOR: ' +
                str(self.SHORT_SEPARATOR))
        if (self.SEPARATOR != None and
            self.SEPARATOR != '--' and
            self.SEPARATOR != '/' and
            self.SEPARATOR != '-'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: SEPARATOR: ' +
                str(self.SEPARATOR))
        if (self.ARITY != None and 
            not is_positive_int(self.ARITY) and
            self.ARITY != '?' and
            self.ARITY != '+' and
            self.ARITY != '*' and
            not re.search(r'\d+', self.ARITY)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: ARITY: ' + 
                str(self.ARITY))
        if (self.ARITY != None and
            is_positive_int(self.ARITY) and
            int(self.ARITY) > 1 and
            self.ARGSEP == None):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Missing column: ARGSEP')
        
        # I have now decided that we are going to validate the
        # ArgumentValues.HAS_VALUE using a Perl regex, which will
        # found in RANGE in this table, so we need to validate that
        # this is a valid regex.

        if self.RANGE != None:
            try:
                    re.compile(self.RANGE)
            except re.error:

                if (self.RANGE.lower() != "table" and
                    self.RANGE != "IRI" and
                    self.RANGE != "absolute_IRI" and
                    self.RANGE != "URI" and
                    self.RANGE != "absolute_URI" and
                    self.RANGE != "path" and
                    self.RANGE != "absolute_path"):

                    raise InvalidEntity('ERROR: Class: ' + 
                        self.__class__.__name__ + 
                        ': Invalid column: RANGE: ' +
                        str(self.RANGE))
         # TODO validate the arity against separator and make
        # sure there is at least a short name or long name for
        # option or flag.
    
# Automatic population?
class ArgumentValue(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description"   : "A value supplied for a command-line argument in a run of an `Application`.",
            "Standards"     : "None",
            "Automation"    : "Populated automatically when a `Process` is invoked."
        }

    @classmethod
    def columns(cls):
        return [
            { "HAS_VALUE":
                { "Type"        : "TEXT",
                  "Description" : "Value supplied, or true/false for flags",
                  "Standards"   : "None",
                  "Validation"  : "None",
                  "Automation"  : "Populated when the `Process` is invoked"
                }
            },
            { "FOR_PROCESS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Process` table of the `Process` this `ArgumentValue` applies to",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Process`",
                  "Null"        : "Not null",
                  "Automation"  : "Populated automatically when the `Process` is created"
                }
            },
            { "FOR_ARGUMENT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Argument` table of the `Argument` this value is for",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Argument`",
                  "Null"        : "Not null",
                  "Automation"  : "Populated automatically when the `Process` is created"
                }
            },
            { "BOX":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table of the box this value can be for",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Not null",
                  "Automation"  : "Populated automatically when the `Process` is created"
                }
            }
        ]

    @classmethod
    def primaryKeys(cls):
        return [ [ "FOR_PROCESS", "FOR_ARGUMENT", "HAS_VALUE" ],
                 [ "FOR_PROCESS", "FOR_ARGUMENT", "BOX" ] ]

        
    def __init__(self, values = None):
        Table.__init__(self)
        self.HAS_VALUE = None 
        self.FOR_PROCESS = None # Foreign key in table Processes
        self.FOR_ARGUMENT = None # Foreign key in table Arguments
        self.BOX = None # Foreign key in table Boxes
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "ArgumentValues"

    def validate(self, update=False):
        Table.validate(self)
        if self.FOR_ARGUMENT == None:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: FOR_ARGUMENT' +
                self.FOR_ARGUMENT)
        if self.FOR_PROCESS == None:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: FOR_PROCESS' +
                self.FOR_PROCESS)
        if ((self.HAS_VALUE == None and
             self.BOX == None ) or
            (self.HAS_VALUE != None and
             self.BOX != None )):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid columns: HAS_VALUE, BOX;' +
                ' HAS_VALUE: ' + 
                self.HAS_VALUE +
                ', BOX: ' +
                self.BOX)
# Automatic population?
# Many-to-many
class Assumes(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Standards" : "None",
            "Automation": "This relationship may be inferred automatically from the use of `StatisticalMethod` or `VisualisationMethod`."
        }

    @classmethod
    def columns(cls):
        return [
            { "PERSON":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of the `Person` making the assumption",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "STATISTICS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Statistics` table if assumption applies to a statistical computation",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Statistics`",
                  "Null"        : "Null if `Visualisation` is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Visualisation` table if assumption applies to a `Visualisation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Visualisation`",
                  "Null"        : "Null if `Statistics` is not null",
                  "Automation"  : "None"
                }
            },
            { "VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Variable` table of the variable to which the assumption applies",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Variable`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "ASSUMPTION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Assumption` table of the `Assumption` being made",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Assumption`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Assumes', 'sourceColumn' : 'PERSON', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' },
                { 'sourceTable' : 'Assumes', 'sourceColumn' : 'STATISTICS', 'targetTable' : 'Statistics', 'targetColumn' : 'ID_STATISTICS' },
                { 'sourceTable' : 'Assumes', 'sourceColumn' : 'VISUALISATION', 'targetTable' : 'Visualisations', 'targetColumn' : 'ID_VISUALISATION' },
                { 'sourceTable' : 'Assumes', 'sourceColumn' : 'VARIABLE', 'targetTable' : 'Variables', 'targetColumn' : 'ID_VARIABLE' },
                { 'sourceTable' : 'Assumes', 'sourceColumn' : 'ASSUMPTION', 'targetTable' : 'Assumptions', 'targetColumn' : 'ID_ASSUMPTION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ASSUMPTION", "VARIABLE" ], 
             [ "ASSUMPTION", "PERSON" ],
             [ "ASSUMPTION", "STATISTICS" ],
             [ "ASSUMPTION", "VISUALISATION" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.PERSON = None # Foreign key in table Persons
        self.STATISTICS = None # Foreign key in table Statistics
        self.VISUALISATION = None # Foreign key in table Visualisation
        self.VARIABLE = None # Foreign key in Variables
        self.ASSUMPTION = None # Foreign key in Assumptions
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "Assumes"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.PERSON != None:
            notNones += 1
        if self.STATISTICS != None:
            notNones += 1
        if self.VISUALISATION != None:
            notNones += 1
        if self.VARIABLE != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': violation of the primary key: ' +
                ' PERSON: ' +
                str(self.PERSON) +
                ' STATISTICS: ' + 
                str(self.STATISTICS) +
                'VISUALISATION: ' +
                str(self.VISUALISATION) +
                'VARIABLE: ' +
                str(self.VARIABLE))

class Assumption(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description"   : "An `Assumption` is a condition applied to a `Variable` for its proper application to a `Statistic`. (That `Statistic` being realised as an aggregation of the `Variable` to which the `Assumption` applies.) A `Person` makes an `Assumption` about a `Variable` (in the `Assumes` table), explicitly or implicitly, every time they compute the `Statistic` on it.",
            "Standards"     : "None",
            "Automation"    : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_ASSUMPTION":
                { "Type"        : "TEXT",
                  "Description" : "Short name for the assumption",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_ASSUMPTION" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_ASSUMPTION = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Assumptions"

# Specialisation of PROV:Entity        
# Automatic population?
class Box(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "A `Box` is any data container (file, database, URI, etc.) used to store or reference data within the system.",
            "Standards"  : "`PROV:Entity`",
            "Automation" : """A `Box` should be created automatically whenever data is accessed or generated by a `Process`.
Metadata such as size, encoding, timestamps, and hash may be populated automatically using system tools (e.g. OS calls, HTTP headers, checksum utilities)."""
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_BOX":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Box`",
                  "Standards"   : "None",
                  "Validation"  : "Primary key",
                  "Automation"  : "Generated automatically"
                }
            },
            { "LOCATION_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "Type of resource the `Box` refers to (e.g. file, URI, database)",
                  "Standards"   : "?",
                  "Validation"  : "String describing access type",
                  "Automation"  : "Requires appropriate software depending on type"
                }
            },
            { "LOCATION_VALUE":
                { "Type"        : "TEXT",
                  "Description" : "The means of accessing the resource (path, URI, connection string, etc.)",
                  "Standards"   : "URI/IRI",
                  "Validation"  : "Depends on LOCATION-TYPE",
                  "Automation"  : "Parsed and used by system handlers"
                }
            },
            { "SIZE":
                { "Type"        : "INTEGER",
                  "Description" : "Size of the resource in bytes",
                  "Standards"   : "ISO/IEC 80000-13",
                  "Validation"  : "Non-negative integer or null",
                  "Automation"  : "Retrieved via OS or HTTP headers"
                }
            },
            { "ENCODING":
                { "Type"        : "TEXT",
                  "Description" : "Encoding of the resource",
                  "Standards"   : "MIME",
                  "Validation"  : "Valid MIME type or null",
                  "Automation"  : "Detected using system tools (e.g. file -I, HTTP headers)"
                }
            },
            { "CREATION_TIME":
                { "Type"        : "TEXT",
                  "Description" : "Time the resource was created",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Retrieved via OS stat or equivalent"
                }
            },
            { "MODIFICATION_TIME":
                { "Type"        : "TEXT",
                  "Description" : "Last modification time of the resource",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Retrieved via OS stat or HTTP headers"
                }
            },
            { "UPDATE_TIME":
                { "Type"        : "TEXT",
                  "Description" : "Time the metadata for this `Box` was last updated",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "System maintained"
                }
            },
            { "HASH":
                { "Type"        : "TEXT",
                  "Description" : "Hash of the resource content",
                  "Standards"   : "None",
                  "Validation"  : "Format: algorithm:encoding:value",
                  "Automation"  : "Generated using hashing tools (e.g. md5sum, sha256sum)"
                }
            },
            { "INSTANCE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table describing the type of `Box`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "LOCATION_APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table if this `Box` refers to an `Application`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`.",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "LOCATION_DOCUMENTATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Documentation` table if this `Box` refers to `Documentation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of `Documentation`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "GENERATED_BY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table of the `Study` that generated this `Box`",
                  "Standards"   : "`PROV:wasGeneratedBy`",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Null if not generated by a `Study`",
                  "Automation"  : "Set when `Process` produces output"
                }
            },
            { "REPOSITORY_OF":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table of `Study` this `Box` is a repository for",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            },
            { "HELD_BY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of person holding the `Box`",
                  "Standards"   : "`PROV:wasAttributedTo`",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            },
            { "SOURCED_FROM":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of source of the `Box`",
                  "Standards"   : "`PROV:wasAttributedTo`",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            },
            { "OUTPUT_OF":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Process` table of the `Process` that produced this `Box`",
                  "Standards"   : "`PROV:wasGeneratedBy`",
                  "Validation"  : "Must be an ID of a `Process`",
                  "Null"        : "Null if not produced by a `Process`",
                  "Automation"  : "Automatically set during `Process` execution"
                }
            },
            { "COLLECTION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table if this `Box` is part of another `Box`",
                  "Standards"   : "PROV:hadMember",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Null if not part of a collection",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [ { 'sourceTable' : 'Boxes', 'sourceColumn' : 'LOCATION_APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'LOCATION_DOCUMENTATION', 'targetTable' : 'Documentation', 'targetColumn' : 'ID_DOCUMENTATION' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'GENERATED_BY', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'REPOSITORY_OF', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'HELD_BY', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'SOURCED_FROM', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'OUTPUT_OF', 'targetTable' : 'Processes', 'targetColumn' : 'ID_PROCESS' },
                 { 'sourceTable' : 'Boxes', 'sourceColumn' : 'COLLECTION', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' } ]

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_BOX" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_BOX = None
        self.LOCATION_VALUE = None
        self.LOCATION_TYPE = None
        self.SIZE = None
        self.ENCODING= None
        self.CREATION_TIME = None
        self.MODIFICATION_TIME = None
        self.UPDATE_TIME = None
        self.HASH = None
        self.INSTANCE =    None # Foreign key in table BoxTypes
        self.LOCATION_APPLICATION = None # Foreign key in table Applications
        self.LOCATION_DOCUMENTATION = None # Foreign key in table Documentations
        self.GENERATED_BY = None # Foreign key in table Studies
        self.REPOSITORY_OF = None # Foreign key in table Studies
        self.HELD_BY = None # Foreign key in table Persons
        self.SOURCED_FROM = None # Foreign key in table Persons
        self.OUTPUT_OF = None # Foreign key in the Processes table
        self.COLLECTION = None # Foreign key in the Boxes table
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Boxes"

    def validate(self, update=False):
        Table.validate(self)
        # TODO
        # location_type: file, URI, IRI, remote file, table, ...
        # location_value: the value of location_type
        # hash: hashing-algo:hash
        if (self.LOCATION_TYPE != None and
            self.LOCATION_TYPE != "local" and
            self.LOCATION_TYPE != "IRI" ):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: LOCATION_TYPE = ' +
                str(self.LOCATION_TYPE))
        if (self.LOCATION_TYPE != None and
            not is_path(self.LOCATION_VALUE) and
            not is_iri(self.LOCATION_VALUE)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: LOCATION_VALUE = ' +
                str(self.LOCATION_VALUE))
        validsize = re.compile(r'^[0-9]+(\.[0-9]+)?(K|M|G|T|Ki|Mi|Gi|Ti)?$')
        if (self.SIZE != None and
            not validsize.match(str(self.SIZE))):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: SIZE = ' +
                self.SIZE)
        if (self.CREATION_TIME != None and 
            not iso8601(self.CREATION_TIME)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: CREATION_TIME = ' +
                self.CREATION_TIME)
        if (self.MODIFICATION_TIME != None and 
            not iso8601(self.MODIFICATION_TIME)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: MODIFICATION_TIME = ' +
                self.MODIFICATION_TIME)
        if (self.UPDATE_TIME != None and 
            not iso8601(self.UPDATE_TIME)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: UPDATE_TIME = ' +
                self.UPDATE_TIME)
        # I have left this commented out. You would think that
        # modification and update time would be subsequent to
        # creation time, but this is not always the case in
        # Unix, a file can be created (say by output) after an
        # earlier version was modified.

         # if (self.CREATION_TIME != None and
        #     self.MODIFICATION_TIME != None and
        #     self.MODIFICATION_TIME < self.CREATION_TIME):
        #     raise InvalidEntity('ERROR: Class: ' + self.__class__.__name__ + ': Invalid column: CREATION_TIME,MODIFICATION_TIME')
        # if (self.CREATION_TIME != None and
        #     self.UPDATE_TIME != None and
        #     self.UPDATE_TIME < self.CREATION_TIME):
        #     raise InvalidEntity('ERROR: Class: ' + self.__class__.__name__ + ': Invalid column: CREATION_TIME,UPDATE_TIME')
        if self.INSTANCE != None:
            # TODO
            # Eventually do an enquiry to make sure this
            # is of the correct encoding type, since we
            # have an active cursor.
            pass
            

    def stat(self):
        st = os.stat(self.LOCATION_VALUE)
        self.CREATION_TIME = datetime.datetime.fromtimestamp(st.st_ctime).isoformat()
        self.MODIFICATION_TIME =  datetime.datetime.fromtimestamp(st.st_mtime).isoformat()
        self.UPDATE_TIME =  datetime.datetime.fromtimestamp(st.st_atime).isoformat()
        self.SIZE = st.st_size
        self.ENCODING = encoding.from_file(self.LOCATION_VALUE)
        

# Possible specialisation of PROV:Entity
class BoxType(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "A `BoxType` defines the format and identification rules for Boxes, describing how their contents should be interpreted.",
            "Standards"  : "None",
            "Automation" : "`BoxType`s are expected to be defined by the user; identification rules may be applied automatically when inspecting `Box` contents."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `BoxType`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "FORMAT":
                { "Type"        : "TEXT",
                  "Description" : "Format of the `Box` contents",
                  "Standards"   : "MIME",
                  "Validation"  : "Valid MIME type",
                  "Automation"  : "None"
                }
            },
            { "IDENTIFIER":
                { "Type"        : "TEXT",
                  "Description" : "Rule used to identify whether a `Box` conforms to this `BoxType` (e.g. magic bytes, filename pattern)",
                  "Standards"   : "None",
                  "Validation"  : "Structured rule string",
                  "Automation"  : "None"
                }
            }
        ]
    # This should probably be a static method as well, as it doesn't change
    # per instance.        

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_BOX_TYPE" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_BOX_TYPE = None
        self.FORMAT = None
        self.IDENTIFIER = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "BoxTypes"

    def validate(self, update=False):
        Table.validate(self)
        if (self.FORMAT != None and
            not mimetype(self.FORMAT)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: FORMAT: ' +
                self.FORMAT)
        identifier_regex = re.compile(r'(magic|name)\:(.*)(\;(magic|name)\:(.*))*')
        if (self.IDENTIFIER != None and
            not identifier_regex.match(self.IDENTIFIER)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: IDENTIFIER :' +
                self.IDENTIFIER)

# Specialisation of PROV:Agent
# Automatic population?
class Computer(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "A `Computer` represents a machine on which a `Process` is executed.",
            "Standards"  : "PROV:Agent",
            "Automation" : "Most values are expected to be automatically obtained from the operating system and network interfaces."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_COMPUTER":
                { "Type"        : "TEXT",
                  "Description" : "Unique key",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "HOST_ID":
                { "Type"        : "TEXT",
                  "Description" : "Identifier for the host machine",
                  "Standards"   : "?",
                  "Validation"  : "String",
                  "Automation"  : "Retrieved from the operating system"
                }
            },
            { "IP_ADDRESS":
                { "Type"        : "TEXT",
                  "Description" : "IP address of the machine",
                  "Standards"   : "?",
                  "Validation"  : "Valid IP address string",
                  "Automation"  : "Retrieved from the network interface"
                }
            },
            { "MAC_ADDRESS":
                { "Type"        : "TEXT",
                  "Description" : "MAC address of the machine",
                  "Standards"   : "?",
                  "Validation"  : "Valid MAC address string",
                  "Automation"  : "Retrieved from the network interface"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_COMPUTER" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_COMPUTER = None
        self.HOST_ID = None
        self.IP_ADDRESS = None
        self.MAC_ADDRESS = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Computers"

    def validate(self, update=False):
        Table.validate(self)
        if update == False and not fqdn.match(self.HOST_ID):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: HOST_ID = ' +
                self.HOST_ID)
        if (self.IP_ADDRESS != None and
            not ip(self.IP_ADDRESS)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: IP_ADDRESS = ' +
                self.IP_ADDRESS)
        # From https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address
        mac_address = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if (self.MAC_ADDRESS != None and
            not mac_address.match(self.MAC_ADDRESS)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: MAC_ADDRESS = ' +
                self.MAC_ADDRESS)

# Many-to-many
class Content(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Content` table describes how a `Variable` (or `StatisticalVariable`) is located within a `Box`.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "OPTIONALITY":
                { "Type"        : "TEXT",
                  "Description" : "Whether the `Variable` always appears or only appears depending on some condition",
                  "Standards"   : "None",
                  "Validation"  : "One of 'always' or 'depends'",
                  "Automation"  : "None"
                }
            },
            { "LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "How to locate the `Variable` value within the `Box` (e.g. row:X, column:Y, field:Z)",
                 "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            },
            { "TIME_LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "How to locate the temporal context (e.g. timestamps)",
                  "Standards"   : "None",
                  "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            },
            { "LINK_LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "How to locate link identifiers (for relational data)",
                  "Standards"   : "None",
                  "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            },
            { "AGENT_LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "How to locate agent identifiers",
                  "Standards"   : "None",
                  "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            },
            { "BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table of the `BoxType` this `Content` applies to",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Variable` table if this `Content` refers to a `Variable`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Variable`",
                  "Null"        : "Null if STATISTICAL_VARIABLE is not null",
                  "Automation"  : "None"
                }
            },
            { "STATISTICAL_VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalVariable` table if this `Content` refers to a `StatisticalVariable`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalVariable`",
                  "Null"        : "Null if VARIABLE is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if this `Content` is used for visualisation",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{'sourceTable' : 'Contents', 'sourceColumn' : 'BOX_TYPE', 'targetTable' : 'BoxTypes', 'targetColumn' : 'ID_BOX_TYPE' },
                {'sourceTable' : 'Contents', 'sourceColumn' : 'VARIABLE', 'targetTable' : 'Variables', 'targetColumn' : 'ID_VARIABLE' },
                {'sourceTable' : 'Contents', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "BOX_TYPE", "VARIABLE" ],
             [ "BOX_TYPE", "VISUALISATION_METHOD" ],
             [ "BOX_TYPE", "STATISTICAL_VARIABLE" ]]

    def __init__(self, values = None):
        Table.__init__(self)
        self.OPTIONALITY = None
        self.LOCATOR = None
        self.SPACE_LOCATOR = None
        self.TIME_LOCATOR = None
        self.LINK_LOCATOR = None
        self.AGENT_LOCATOR = None
        self.BOX_TYPE = None # Foreign key in table BoxTypes
        self.VARIABLE = None # Foreign key in table Variables
        self.STATISTICAL_VARIABLE = None # Foreign key in table StatisticalVariables
        self.VISUALISATION_METHOD = None # Foreign key in table VisualisationMethods
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Contents"

    def validate(self, update=False):
        Table.validate(self)
        # TODO
        # locator: table or csv file for now.
        # space_locator: variable.is_space then GIS format rule for obtaining spatial value
        # time_locator: variable.is_time then format rule for obtaining timestamp value.
        # link_locator: variable.is_time then format rule for obtaining link id value.
        # agent_locator: variable.is_time then format rule for obtaining agent ID value.
        if (self.OPTIONALITY != None and
            self.OPTIONALITY.lower() != 'always' and
            self.OPTIONALITY.lower() != 'depends'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: OPTIONALITY: ' +
                self.OPTIONALITY)

# Automatic population?
class Context(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Context` table provides contextual values such as time, space, agent, or link, which can be associated with `Values`.",
            "Standards"  : "None",
            "Automation" : "`Context` entries may be created automatically when extracting or interpreting data from `Box`es."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_CONTEXT":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Context`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "VALUE":
                { "Type"        : "TEXT",
                  "Description" : "`Value` of the context (e.g. time, space, agent, or link identifier)",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "Derived from `Content` locators or data extraction"
                }
            },
            { "PART":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Context` table indicating that this `Context` is part of another `Context`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Context`",
                  "Null"        : "Null if this `Context` is not part of another",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{'sourceTable' : 'Contexts', 'sourceColumn' : 'PART', 'targetTable' : 'Contexts', 'targetColumn' : 'ID_CONTEXT' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_CONTEXT" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_CONTEXT = None
        self.VALUE = None 
        self.PART = None # Foreign key in this table, Context
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Contexts"

# dc:contributor
# PROV:was-attributed-to
# Many-to-many
class Contributor(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Contributor` table records people who have contributed to `Application`s or `Documentation`, including how they are credited.",
            "Standards"  : "dc:contributor",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "CONTRIBUTION":
                { "Type"        : "TEXT",
                  "Description" : "Nature of the contribution made by the person",
                  "Standards"   : "dc:contributor",
                  "Validation"  : "String describing contribution type",
                  "Automation"  : "None"
                }
            },
            { "ALIAS":
                { "Type"        : "TEXT",
                  "Description" : "Name or alias used for the contributor in the context of the `Application` or `Documentation`",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "CONTRIBUTOR":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of the contributor",
                  "Standards"   : "dc:contributor",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "DOCUMENTATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Documentation` table if the contribution relates to `Documentation`",
                  "Standards"   : "dc:relation",
                  "Validation"  : "Must be an ID of `Documentation`",
                  "Null"        : "Null if APPLICATION is not null",
                  "Automation"  : "None"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table if the contribution relates to an `Application`",
                  "Standards"   : "dc:relation",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Null if DOCUMENTATION is not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Contributors', 'sourceColumn' : 'CONTRIBUTOR',   'targetTable' : 'Persons',       'targetColumn' : 'ID_PERSON' },
                { 'sourceTable' : 'Contributors', 'sourceColumn' : 'DOCUMENTATION', 'targetTable' : 'Documentation', 'targetColumn' : 'ID_DOCUMENTATION' },
                { 'sourceTable' : 'Contributors', 'sourceColumn' : 'APPLICATION',   'targetTable' : 'Applications',  'targetColumn' : 'ID_APPLICATION' }]

    # The problem is that this is an either/or situation. Either there is
    # foreign key that is an application or there is a foreign key that is
    # documentation. I need some kind of constraint. Will check out
    # CHECK and CONSTRAINT to do this.

    @classmethod
    def primaryKeys(cls):
        return [[ "CONTRIBUTOR", "APPLICATION" ],
                [ "CONTRIBUTOR", "DOCUMENTATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.CONTRIBUTOR = None
        self.CONTRIBUTION = None
        self.ALIAS = None
        self.CONTRIBUTOR = None # Foreign key in table Persons
        self.DOCUMENTATION = None # Foreign key in table Documentation
        self.APPLICATION = None # Foreign key in table Applications
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Contributors"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.DOCUMENTATION != None:
            notNones += 1
        if self.APPLICATION != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Ambiguous primary key: ' + 
                self.__class__.__name__ + 
                ': Invalid column: DOCUMENTATION: ' +
                str(self.DOCUMENTATION) + 
                ', APPLICATION: ' +
                str(self.APPLICATION))

        
# Automatic population?
# Many-to-many
class Dependency(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Dependency` table records that one `Application` depends on another, optionally under certain conditions.",
            "Standards"  : "None",
            "Automation" : "A `Dependency` may be inferred automatically in some cases, but are generally provided by the user."
        }

    @classmethod
    def columns(cls):
        return [
            { "OPTIONALITY":
                { "Type"        : "TEXT",
                  "Description" : "Whether the dependency is required, optional, or conditional",
                  "Standards"   : "None",
                  "Validation"  : "One of 'required', 'optional', or a condition string",
                  "Automation"  : "None"
                }
            },
            { "DEPENDANT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` that depends on another",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "DEPENDENCY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` being depended upon",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Dependencies', 'sourceColumn' : 'DEPENDANT',  'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'Dependencies', 'sourceColumn' : 'DEPENDENCY', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "DEPENDANT", "DEPENDENCY" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.OPTIONALITY = None
        self.DEPENDANT = None # Foreign key in the table Applications
        self.DEPENDENCY = None # Foreign key in the table Applications
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "Dependencies"
 
    def validation(self):
        # TODO
        # optionality: 'required', 'optional' or condition, e.g arg3 == /\.png$/
        pass

# Specialisation of PROV:Entity
class Documentation(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Documentation` table records documents that describe `Application`s or Studies.",
            "Standards"  : "dc:title; dc:created",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_DOCUMENTATION":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Documentation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "TITLE":
                { "Type"        : "TEXT",
                  "Description" : "Title of the documentation",
                  "Standards"   : "dc:title",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "DATE":
                { "Type"        : "TEXT",
                  "Description" : "Date the documentation was created",
                  "Standards"   : "dc:created; ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "None"
                }
            },
            { "DOCUMENTS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` this `Documentation` describes",
                  "Standards"   : "dc:relation",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Null if REFERENCES is not null",
                  "Automation"  : "None"
                }
            },
            { "DESCRIBES":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table of the `Study` this `Documentation` references",
                  "Standards"   : "dc:relation",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Null if DOCUMENTS is not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Documentation', 'sourceColumn' : 'DOCUMENTS', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'Documentation', 'sourceColumn' : 'DESCRIBES', 'targetTable' : 'Studies',      'targetColumn' : 'ID_STUDY' }]

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_DOCUMENTATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_DOCUMENTATION = None
        self.TITLE = None
        self.DATE = None
        self.DOCUMENTS = None # Foreign key in table Applications
        self.DESCRIBES = None # Foreign key in table Studies
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "Documentation"

    def validate(self, update=False):
        Table.validate(self)
        # title: dc:title
        notNones = 0
        if self.DOCUMENTS != None:
            notNones += 1
        if self.DESCRIBES != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: ABOUT,DESCRIBES')
        if (self.DATE != None and
            not iso8601(self.DATE)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: DATE: ' +
                self.DATE)
            


# Many-to-many
class Employs(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Employs` table records that a `StatisticalMethod` or `VisualisationMethod` employs a `StatisticalVariable`.",
            "Standards"  : "None",
            "Automation" : "This relationship may be inferred automatically from the definitions of methods and variables."
        }

    @classmethod
    def columns(cls):
        return [
            { "STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table if the relationship involves a statistical method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Null if VISUALISATION_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if the relationship involves a visualisation method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Null if STATISTICAL_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "STATISTICAL_VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalVariable` table of the variable being employed",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalVariable`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Employs', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' },
                { 'sourceTable' : 'Employs', 'sourceColumn' : 'STATISTICAL_VARIABLE', 'targetTable' : 'StatisticalVariables', 'targetColumn' : 'ID_STATISTICAL_VARIABLE' },
                { 'sourceTable' : 'Employs', 'sourceColumn' : 'STATISTICAL_METHOD',   'targetTable' : 'StatisticalMethods',   'targetColumn' : 'ID_STATISTICAL_METHOD' }]
    @classmethod
    def primaryKeys(cls):
        return [[ "STATISTICAL_VARIABLE", "STATISTICAL_METHOD" ],
                [ "STATISTICAL_VARIABLE", "VISUALISATION_METHOD" ] ]


    def __init__(self, values = None):
        Table.__init__(self)
        self.STATISTICAL_METHOD = None # Foreign key in table StatisticalMethods
        self.VISUALISATION_METHOD = None # Foreign key in table VisualisationMethods
        self.STATISTICAL_VARIABLE = None # Foreign key in table StatisticalVariables
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Employs"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.STATISTICAL_METHOD != None:
            notNones += 1
        if self.VISUALISATION_METHOD != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Ambiguous primary key: ' + 
                self.__class__.__name__ + 
                ': STATISTICAL_METHOD: ' +
                self.STATISTICAL_METHOD +
                ', VISUALISATION_METHOD: ' +
                self.VISUALISATION)

# Many-to-many
class Entailment(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Entailment` table records that a `StatisticalMethod` or `VisualisationMethod` entails an `Assumption`.",
            "Standards"  : "None",
            "Automation" : "This relationship may be inferred automatically from the definitions of methods and assumptions."
        }

    @classmethod
    def columns(cls):
        return [
            { "STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table if the relationship involves a statistical method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Null if VISUALISATION_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if the relationship involves a visualisation method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Null if STATISTICAL_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "ASSUMPTION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Assumption` table of the `Assumption` that is entailed",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Assumption`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable': 'Entailments', 'sourceColumn' :'STATISTICAL_METHOD',   'targetTable': 'StatisticalMethods',   'targetColumn': 'ID_STATISTICAL_METHOD' },
                { 'sourceTable': 'Entailments', 'sourceColumn' :'VISUALISATION_METHOD', 'targetTable': 'VisualisationMethods', 'targetColumn': 'ID_VISUALISATION_METHOD' },
                { 'sourceTable': 'Entailments', 'sourceColumn' :'ASSUMPTION',           'targetTable': 'Assumptions',          'targetColumn': 'ID_ASSUMPTION' }]
    @classmethod
    def primaryKeys(cls):
        return [[ "ASSUMPTION", "STATISTICAL_METHOD" ],
                [ "ASSUMPTION", "VISUALISATION_METHOD" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.STATISTICAL_METHOD = None # Foreign key in table StatisticalMethods
        self.VISUALISATION_METHOD = None # Foreign key in table VisualisationMethods
        self.ASSUMPTION = None # Foreign key in table Assumptions
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "Entailments"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.STATISTICAL_METHOD != None:
            notNones += 1
        if self.VISUALISATION_METHOD != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Ambiguous primary key: ' + 
                self.__class__.__name__ + 
                ': STATISTICAL_METHOD: ' +
                self.STATISTICAL_METHOD +
                ', VISUALISATION_METHOD: ' +
                self.VISUALISATION)

# Many-to-many
class Implements(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Implements` table records that an `Application` implements a `StatisticalMethod` or `VisualisationMethod`.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "FUNCTION":
                { "Type"        : "TEXT",
                  "Description" : "Name of the function within the `Application` that implements the method",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "LIBRARY":
                { "Type"        : "TEXT",
                  "Description" : "Name of the library within which the function is found",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table if the implementation is for a statistical method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Null if VISUALISATION_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if the implementation is for a visualisation method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Null if STATISTICAL_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` implementing the method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Implements', 'sourceColumn' : 'STATISTICAL_METHOD',   'targetTable' : 'StatisticalMethods',   'targetColumn' : 'ID_STATISTICAL_METHOD' },
                { 'sourceTable' : 'Implements', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' },
                { 'sourceTable' : 'Implements', 'sourceColumn' : 'APPLICATION',          'targetTable' : 'Applications',         'targetColumn' : 'ID_APPLICATION' }]
    @classmethod
    def primaryKeys(cls):
        return [[ "APPLICATION", "STATISTICAL_METHOD" ],
                [ "APPLICATION", "VISUALISATION_METHOD" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.FUNCTION = None
        self.LIBRARY = None 
        self.STATISTICAL_METHOD = None # Foreign key in table StatisticalMethods
        self.VISUALISATION_METHOD = None # Foreign key in table VisualisationMethods
        self.APPLICATION = None # Foreign key in table Applications
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "Implements"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.STATISTICAL_METHOD != None:
            notNones += 1
        if self.VISUALISATION_METHOD != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Ambiguous primary key: ' + 
                self.__class__.__name__ + 
                ': STATISTICAL_METHOD: ' +
                str(self.STATISTICAL_METHOD) +
                ', VISUALISATION_METHOD: ' +
                str(self.VISUALISATION_METHOD))

# Automatic population?
# Many-to-many
class Input(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Input` table records the `Box`es that are used as input to a `Process`, including how they are used.",
            "Standards"  : "PROV:used",
            "Automation" : "Populated automatically when a `Process` is invoked and its inputs are identified."
        }

    @classmethod
    def columns(cls):
        return [
            { "USAGE":
                { "Type"        : "TEXT",
                  "Description" : "Indicates how the input is used by the `Process`",
                  "Standards"   : "None",
                  "Validation"  : "One of 'dependency' or 'data'",
                  "Automation"  : "Set automatically based on the role of the input"
                }
            },
            { "PROCESS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Process` table of the `Process` using the input",
                  "Standards"   : "PROV:used",
                  "Validation"  : "Must be an ID of a `Process`",
                  "Null"        : "Not null",
                  "Automation"  : "Populated automatically when the `Process` is created"
                }
            },
            { "BOX":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table of the `Box` being used as input",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Not null",
                  "Automation"  : "Populated automatically when inputs are resolved"
                }
            }
        ]
   
    @classmethod
    def foreignKeys(cls):
        return [{'sourceTable' : 'Inputs', 'sourceColumn' : 'PROCESS', 'targetTable' : 'Processes', 'targetColumn' : 'ID_PROCESS' },
                { 'sourceTable' : 'Inputs', 'sourceColumn' : 'BOX', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' }]

       
    @classmethod
    def primaryKeys(cls):
        return [ [ "PROCESS", "BOX" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.USAGE = None
        self.PROCESS = None # Foreign key in table Processes
        self.BOX = None # Foreign key in table Boxes
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Inputs"

    def validate(self, update=False):
        Table.validate(self)
        if (self.USAGE.lower() != 'dependency' and
            self.USAGE.lower() != 'data'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: USAGE: ' +
                self.USAGE)

# Many-to-many
class Involvement(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Involvement` table records the involvement of a `Person` in a `Study`, including their role.",
            "Standards"  : "PROV:wasAssociatedWith",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ROLE":
                { "Type"        : "TEXT",
                  "Description" : "Role of the `Person` in the `Study`",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "PERSON":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of the `Person` involved",
                  "Standards"   : "PROV:Agent",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "STUDY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table of the `Study` the `Person` is involved in",
                  "Standards"   : "PROV:Activity",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Involvements', 'sourceColumn' : 'PERSON', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' },
                {'sourceTable' : 'Involvements', 'sourceColumn' : 'STUDY', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY' } ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "PERSON", "STUDY" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ROLE = None
        self.PERSON = None # Foreign key in table Persons
        self.STUDY = None # Foreign key in table Studies
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Involvements"


# Automatic population?
# Many-to-many
# Note both these are specifications
class Meets(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Meets` table records that a `Computer` meets a specified `Specification`.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "COMPUTER_SPECIFICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Specification` table describing the specification met by the `Computer`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Specification`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "REQUIREMENT_SPECIFICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Specification` table defining the required specification being met",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Specification`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Meets', 'sourceColumn' : 'COMPUTER_SPECIFICATION', 'targetTable' : 'Computers', 'targetColumn' : 'ID_COMPUTER' },
                { 'sourceTable' : 'Meets', 'sourceColumn' : 'REQUIREMENT_SPECIFICATION', 'targetTable' : 'Specifications', 'targetColumn' : 'ID_SPECIFICATION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "COMPUTER_SPECIFICATION","REQUIREMENT_SPECIFICATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.COMPUTER_SPECIFICATION = None # Foreign key in the table Specifications
        self.REQUIREMENT_SPECIFICATION = None # Foreign key in the table Specifications
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Meets"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.COMPUTER_SPECIFICATION != None:
            notNones += 1
        if self.REQUIREMENT_SPECIFICATION != None:
            notNones += 1
        if notNones != 2:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: COMPUTER_SPECIFICATION,' +
                'REQUIREMENT_SPECIFICATION')
        
# Specialisation of PROV:Entity
class Model(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Model` table identifies `Application`s that represent models, optionally linking to external model registries.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_MODEL":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Model`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` that is a `Model`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "COMSES":
                { "Type"        : "TEXT",
                  "Description" : "Reference to an entry in the CoMSES-Net model repository",
                  "Standards"   : "None",
                  "Validation"  : "String or identifier",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [ {'sourceTable' : 'Models', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION'} ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_MODEL" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_MODEL = None
        self.APPLICATION = None # Foreign key in the table Applications
        self.COMSES = None # comses: ID of model in CoMSES-Net table
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Models"

class Parameter(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Parameter` table records parameters used by `StatisticalMethod` or `VisualisationMethod`.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PARAMETER":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Parameter`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "DATA_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "Data type of the parameter",
                  "Standards"   : "XSD",
                  "Validation"  : "Valid XSD data type or URI",
                  "Automation"  : "None"
                }
            },
            { "STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table if the parameter applies to a statistical method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Null if VISUALISATION_METHOD is not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if the parameter applies to a visualisation method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Null if STATISTICAL_METHOD is not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Parameters', 'sourceColumn' : 'STATISTICAL_METHOD', 'targetTable' : 'StatisticalMethods', 'targetColumn' : 'ID_STATISTICAL_METHOD' },
                { 'sourceTable' : 'Parameters', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_PARAMETER" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PARAMETER = None
        self.DATA_TYPE = None
        self.STATISTICAL_METHOD = None # Foreign key in table StatisticalMethods
        self.VISUALISATION_METHOD = None # Foreign key in table StatisticalMethods
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Parameters"

# Specialisation of PROV:Agent
class Person(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Person` table records individuals associated with the system, such as users, contributors, or data owners.",
            "Standards"  : "PROV:Agent; FOAF",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PERSON":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Person`",
                  "Standards"   : "FOAF",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "EMAIL":
                { "Type"        : "TEXT",
                  "Description" : "Email address of the `Person`",
                  "Standards"   : "FOAF",
                  "Validation"  : "Valid email address string",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_PERSON" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PERSON = None
        self.EMAIL = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Persons"

    def validate(self, update=False):
        Table.validate(self)
        # From http://emailregex.com
        email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not email.match(self.EMAIL):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: EMAIL: ' +
                self.EMAIL)


class PersonalData(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `PersonalData` table records additional pieces of information about a `Person` as label–value pairs.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PERSONAL_DATA":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `PersonalData` entry",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "CATEGORY":
                { "Type"        : "TEXT",
                  "Description" : "Category describing the type of personal data",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "VALUE":
                { "Type"        : "TEXT",
                  "Description" : "`Value` of the personal data",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "ABOUT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of the `Person` this data is about",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [ {'sourceTable' : 'PersonalData', 'sourceColumn' : 'ABOUT', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_PERSONAL_DATA" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PERSONAL_DATA = None
        self.CATEGORY = None
        self.VALUE = None
        self.ABOUT = None # Foreign key in the Persons table
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "PersonalData"

# Specialisation of PROV:Entity
class Pipeline(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Pipeline` table records sequences of `Application`s, allowing workflows to be defined where one `Application` calls another.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PIPELINE":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Pipeline`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "CALLS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` called by this `Pipeline` step",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "PREVIOUS":
                { "Type"        : "TEXT",
                  "Nullable"    : True,
                  "Description" : "ID in `Pipeline` table of the previous `Pipeline` step",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Pipeline`",
                  "Null"        : "Null if this is the first step",
                  "Automation"  : "None"
                }
            }
        ]
   
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Pipelines', 'sourceColumn' : 'CALLS', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                {'sourceTable' : 'Pipelines', 'sourceColumn' : 'PREVIOUS', 'targetTable' : 'Pipelines', 'targetColumn' : 'ID_PIPELINE' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_PIPELINE" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PIPELINE = None
        self.CALLS = None # Foreign key in the table Applications
        self.PREVIOUS = None # Foreign key in the table Pipelines
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Pipelines"

    def validate(self, update=False):
        Table.validate(self)

# Specialisation of PROV:Activity
# Automatic population?
class Process(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Process` table records an execution of an `Application`, including when and how it was run.",
            "Standards"  : "PROV:Activity",
            "Automation" : "Entries are created automatically when an `Application` is executed, capturing runtime details."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PROCESS":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Process`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "START_TIME":
                { "Type"        : "TEXT",
                  "Description" : "Time at which the `Process` started",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Captured automatically at process start"
                }
            },
            { "END_TIME":
                { "Type"        : "TEXT",
                  "Description" : "Time at which the `Process` ended",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Captured automatically at process completion"
                }
            },
            { "ARGV":
                { "Type"        : "TEXT",
                  "Description" : "Command-line string used to invoke the `Application`",
                  "Standards"   : "POSIX",
                  "Validation"  : "String",
                  "Automation"  : "Constructed automatically from `Argument` and `ArgumentValue`"
                }
            },
            { "ENVIRONMENT":
                { "Type"        : "TEXT",
                  "Description" : "Environment variables used during execution",
                  "Standards"   : "POSIX",
                  "Validation"  : "List of strings",
                  "Automation"  : "Captured from runtime environment"
                }
            },
            { "WORKING_DIR":
                { "Type"        : "TEXT",
                  "Description" : "Working directory from which the `Process` was executed",
                  "Standards"   : "POSIX",
                  "Validation"  : "Valid file path",
                  "Automation"  : "Captured automatically from runtime"
                }
            },
            { "EXECUTABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` that was executed",
                  "Standards"   : "PROV:used",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "Set when the `Process` is created"
                }
            },
            { "SOME_USER":
                { "Type"        : "TEXT",
                  "Description" : "ID in `User` table of the user who initiated the `Process`",
                  "Standards"   : "PROV:wasAssociatedWith",
                  "Validation"  : "Must be an ID of a `User`",
                  "Null"        : "Not null",
                  "Automation"  : "Captured from system user context"
                }
            },
            { "HOST":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Computer` table of the machine on which the `Process` ran",
                  "Standards"   : "PROV:wasAssociatedWith",
                  "Validation"  : "Must be an ID of a `Computer`",
                  "Null"        : "Not null",
                  "Automation"  : "Captured from system environment"
                }
            },
            { "PARENT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Process` table of the parent `Process`, if any",
                  "Standards"   : "PROV:wasInformedBy",
                  "Validation"  : "Must be an ID of a `Process`",
                  "Null"        : "Null if no parent process",
                  "Automation"  : "Set if `Process` is spawned by another"
                }
            }
        ]

    @classmethod
    def foreignKeys(cls):
        return [{  'sourceTable' : 'Processes', 'sourceColumn' : 'EXECUTABLE', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'Processes', 'sourceColumn' : 'SOME_USER', 'targetTable' : 'Users', 'targetColumn' : 'ID_USER' },
                { 'sourceTable' : 'Processes', 'sourceColumn' : 'HOST', 'targetTable' : 'Computers', 'targetColumn' : 'ID_COMPUTER' },
                {'sourceTable' : 'Processes', 'sourceColumn' : 'PARENT', 'targetTable' : 'Processes', 'targetColumn' : 'ID_PROCESS' } ]

    # There were original a load of not null columns in the above table, but
    # this is called twice, once at the start of the process and once when the
    # process had finished. This proved problematic because I did not have the
    # original information such as START_TIME, HOST, etc. in the second call,
    # so althoughthe values START_TIME, WORKING_DIR, EXECUTABLE, SOME_USER,
    # HOST should never be null, in practice when we do the initial insert we
    # are expecting to fail on the second call, with an exception indicating
    # the row is already present. However it reports the null violation before
    # it even checks that, so we are not getting the "correct" exception.

    @classmethod
    def primaryKeys(cls):
        return [ ["ID_PROCESS" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PROCESS = None
        self.START_TIME = None
        self.END_TIME = None
        self.ARGV = None
        self.ENVIRONMENT = None
        self.WORKING_DIR = None
        self.EXECUTABLE = None # Foreign key in the table Applications
        self.SOME_USER = None # Foreign key in the table Users
        self.HOST = None # Foreign key in the table Computers
        self.PARENT = None # Foreign key in the table Processes
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Processes"

    def validate(self, update=False):
        Table.validate(self)
        # working_dir: Unix or DOS path
        # argv: regex
        # envs: regex based on:
        # for Unix:
        #      ENV_VAR1=some_value ENV_VAR2=some_other_value exectuable
        # or for Windows
        #      cmd /C "set ENV_VAR1=some_value && ENV_VAR2=some_other_value exectuable
        if self.START_TIME != None and not iso8601(self.START_TIME):
            raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                       ": column: START_TIME " + 
                        ": invalid value: " + 
                    str(self.START_TIME))
        if self.END_TIME != None:
            if not iso8601(self.END_TIME):
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Invalid column: END_TIME' +
                    str(self.END_TIME))
            # This next line is bogus and will not work.
            if (self.START_TIME != None and
                self.START_TIME > self.END_TIME):
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Invalid column: START_TIME = ' + 
                    str(self.START_TIME) +
                    ' and END_TIME = ' + 
                    str(self.END_TIME))

# Many-to-many
class Product(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Product` table describes the types of output that an `Application` can produce, including how those outputs are located.",
            "Standards"  : "None",
            "Automation" : "Some `Product`s may be inferred automatically based on `Application` execution and generated `Box`es."
        }

    @classmethod
    def columns(cls):
        return [
            { "OPTIONALITY":
                { "Type"        : "TEXT",
                  "Description" : "Whether the `Product` is always produced or only under certain conditions",
                  "Standards"   : "None",
                  "Validation"  : "One of 'always' or 'depends'",
                  "Automation"  : "None"
                }
            },
            { "LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "Description of how to locate the `Product` output",
                  "Standards"   : "None",
                  "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` producing this `Product`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table describing the type of `Box` produced",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "IN_FILE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table if the `Product` is contained within another file",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Null if LOCATOR is not 'in-file'",
                  "Automation"  : "None"
                }
            }
        ]

    @classmethod
    def foreignKeys(cls):
        return [{'sourceTable' : 'Products', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'Products', 'sourceColumn' : 'BOX_TYPE', 'targetTable' : 'BoxTypes', 'targetColumn' : 'ID_BOX_TYPE' },
                { 'sourceTable' : 'Products', 'sourceColumn' : 'IN_FILE', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' }]

    @classmethod
    def primaryKeys(cls):
        return [ ["APPLICATION", "BOX_TYPE" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.OPTIONALITY = None
        self.LOCATOR = None
        self.APPLICATION = None # Foreign key in the table Applications
        self.BOX_TYPE = None # Foreign key in the table BoxTypes
        self.IN_FILE = None # Foreign key in the table Boxes
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Products"

    def validate(self, update=False):
        Table.validate(self)
        if (self.OPTIONALITY.lower() != 'always' and
            self.OPTIONALITY.lower() != 'depends'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: OPTIONALITY: ')
        if (self.LOCATOR != None and 
            not locator.match(self.LOCATOR)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: LOCATOR: ' + 
                self.LOCATOR)

# Specialisation of PROV Activity
class Project(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Project` table records `Project`s, which are collections of Studies and may include funding and organisational information.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_PROJECT":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Project`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "TITLE":
                { "Type"        : "TEXT",
                  "Description" : "Title of the `Project`",
                  "Standards"   : "dc:title",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "FUNDER":
                { "Type"        : "TEXT",
                  "Description" : "Organisation or body funding the `Project`",
                  "Standards"   : "dc:publisher",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "GRANT_ID":
                { "Type"        : "TEXT",
                  "Description" : "Identifier of the grant funding the `Project`",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "STUDY":
                { "Type"        : "TEXT",
                  "Description" : "A `Study` is a piece of work at some level of aggregation.",
                  "Standards"   : "None",
                  "Validation"  : "An ID in the `Study` table.",
                  "Null"        : "Not Null",
                  "Automation"  : "None"
                }
             }
        ]

    @classmethod
    def foreignKeys(cls):
        return [{'sourceTable' : 'Projects', 'sourceColumn' : 'STUDY', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY'} ]
    @classmethod
    def primaryKeys(cls):
        return [ ["ID_PROJECT" ] ]
        
    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_PROJECT = None
        self.TITLE = None
        self.FUNDER = None
        self.GRANT_ID = None
        self.STUDY = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Projects"

        
# Many-to-many
class Requirement(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Requirement` table records requirements that an `Application` has with respect to `Specification`s, including exact, minimum, or matching constraints.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` that has the requirement",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "MATCH":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Specification` table specifying values that must match",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Specification`",
                  "Null"        : "Null if EXACT or MINIMUM is used",
                  "Automation"  : "None"
                }
            },
            { "MINIMUM":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Specification` table specifying minimum acceptable values",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Specification`",
                  "Null"        : "Null if EXACT or MATCH is used",
                  "Automation"  : "None"
                }
            },
            { "EXACT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Specification` table specifying exact required values",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Specification`",
                  "Null"        : "Null if MATCH or MINIMUM is used",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Requirements', 'sourceColumn' : 'MATCH', 'targetTable' : 'Specifications', 'targetColumn' : 'ID_SPECIFICATION' },
                { 'sourceTable' : 'Requirements', 'sourceColumn' : 'MINIMUM', 'targetTable' : 'Specifications', 'targetColumn' : 'ID_SPECIFICATION' },
                { 'sourceTable' : 'Requirements', 'sourceColumn' : 'EXACT', 'targetTable' : 'Specifications', 'targetColumn' : 'ID_SPECIFICATION' },
                { 'sourceTable' : 'Requirements', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "APPLICATION", "MATCH" ],
             [ "APPLICATION", "EXACT" ],
             [ "APPLICATION", "MINIMUM" ] ]  

        

    def __init__(self, values = None):
        Table.__init__(self)
        self.APPLICATION = None # Foreign key of the table Applications
        self.MATCH = None # Foreign key of the table Specifications
        self.MINIMUM = None # Foreign key of the table Specifications
        self.EXACT = None # Foreign key of the table Specifications
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Requirements"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.MINIMUM != None:
            notNones += 1
        if self.MATCH != None:
            notNones += 1
        if self.EXACT != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: MINIMUM,MATCH,EXACT')

class Specification(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Specification` table defines labelled specification values, typically used to describe properties of `Computer`s or requirements of `Application`s.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_SPECIFICATION":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Specification`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "CATEGORY":
                { "Type"        : "TEXT",
                  "Description" : "Category describing the type of specification",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "VALUE":
                { "Type"        : "TEXT",
                  "Description" : "`Value` of the specification",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "SPECIFICATION_OF":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Computer` table of the `Computer` this `Specification` describes",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Computer`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [ {'sourceTable' : 'Specifications', 'sourceColumn' : 'SPECIFICATION_OF', 'targetTable' : 'Computers', 'targetColumn' : 'ID_COMPUTER' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_SPECIFICATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_SPECIFICATION = None
        self.VALUE = None
        self.CATEGORY = None
        self.SPECIFICATION_OF = None # Foreign key of the table Specifications
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Specifications"

    #def validate(self, update=False):
        # TODO
        # value if this is the target of a match requirement,
        # then this may be a regex, otherwise it should be
        # some form of number.
        # No validation of foreign keys as there is additional many-to-many
        # keys from the "Requirements" table.

# Automatic population?
# Many-to-many

# This links Visualisation and Statistics to the an actual value, and as such
# represents an instantiation and extends the provenance into fine grain.

class StatisticalInput(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `StatisticalInput` table records the input `Variable`s or `Box`es used by a `StatisticalMethod` when performing a statistical computation.",
            "Standards"  : "PROV:used",
            "Automation" : "`Input`s may be inferred automatically when a `Statistics` computation is executed."
        }

    @classmethod
    def columns(cls):
        return [
            { "STATISTICS":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table of the method using the input",
                  "Standards"   : "PROV:used",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Visualisation`s table of the `Visualisation` used as input to the method",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `Visualisation`",
                  "Null"        : "Null if VARIABLE is not null",
                  "Automation"  : "Resolved automatically where possible"
                }
            },
            { "VALUE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Value` table of the `Variable` used as input to the method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Value`",
                  "Null"        : "Null if `Value` is not null",
                  "Automation"  : "Resolved automatically from `Content` definitions"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'StatisticalInputs', 'sourceColumn' : 'VISUALISATION', 'targetTable' : 'Visualisations', 'targetColumn' : 'ID_VISUALISATION' },
                { 'sourceTable' : 'StatisticalInputs', 'sourceColumn' : 'STATISTICS',    'targetTable' : 'Statistics',     'targetColumn' : 'ID_STATISTICS' },
                { 'sourceTable' : 'StatisticalInputs', 'sourceColumn' : 'VALUE',         'targetTable' : 'Value',          'targetColumn' : 'ID_VALUE' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "VALUE", "STATISTICS" ],
             [ "VALUE", "VISUALISATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.STATISTICS = None # Foreign key in the table Statistics
        self.VISUALISATION = None # Foreign key in the table Visualisation
        self.VALUE = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "StatisticalInputs"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.STATISTICS != None:
            notNones += 1
        if self.VISUALISATION != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + self.__class__.__name__ + ': Invalid column: STATISTICS,VISUALISATION')

class StatisticalMethod(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `StatisticalMethod` table records statistical methods that may be applied to data to generate `StatisticalVariable`s.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `StatisticalMethod`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_STATISTICAL_METHOD" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_STATISTICAL_METHOD = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "StatisticalMethods"

# Names the output of a StatisticalMethod
class StatisticalVariable(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `StatisticalVariable` table records variables that are generated by applying a `StatisticalMethod`.",
            "Standards"  : "None",
            "Automation" : "`StatisticalVariable`s may be created automatically as outputs of statistical computations."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_STATISTICAL_VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `StatisticalVariable`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "DATA_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "Data type of the `StatisticalVariable`",
                  "Standards"   : "XSD",
                  "Validation"  : "Valid XSD data type or URI",
                  "Automation"  : "None"
                }
            },
            { "STATISTIC_GENERATED_BY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table of the method that generates this `StatisticalVariable`",
                  "Standards"   : "PROV:wasGeneratedBy",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_GENERATED_BY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table of the method that generates this `Visualisation`",
                  "Standards"   : "PROV:wasGeneratedBy",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`.",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'StatisticalVariables', 'sourceColumn' : 'STATISTIC_GENERATED_BY', 'targetTable' : 'StatisticalMethods', 'targetColumn' : 'ID_STATISTICAL_METHOD' },
                { 'sourceTable' : 'StatisticalVariables', 'sourceColumn' : 'VISUALISATION_GENERATED_BY', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_STATISTICAL_VARIABLE" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_STATISTICAL_VARIABLE = None
        self.DATA_TYPE = None
        self.STATISTIC_GENERATED_BY = None
        self.VISUALISATION_GENERATED_BY = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "StatisticalVariables"
        
    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.STATISTIC_GENERATED_BY != None:
            notNones += 1
        if self.VISUALISATION_GENERATED_BY != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Must have at least one generated by: ' +
                " STATISTIC_GENERATED_BY: " +
                str(self.STATISTIC_GENERATED_BY) +
                " VISUALISATION_GENERATED_BY: " +
                str(self.VISUALISATION_GENERATED_BY))

# Specialisation of PROV:Activity
# Automatic population?
class Statistics(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Statistics` table records statistical computations, including when they were performed and how input data was selected.",
            "Standards"  : "PROV:Activity",
            "Automation" : "Entries may be created automatically when statistical computations are performed."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_STATISTICS":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Statistics` computation",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "DATE":
                { "Type"        : "DATE",
                  "Description" : "Date the statistical computation was performed",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Set automatically at execution time"
                }
            },
            { "QUERY":
                { "Type"        : "TEXT",
                  "Description" : "Query used to select the data for the statistical computation",
                  "Standards"   : "None",
                  "Validation"  : "Formatted string",
                  "Automation"  : "None"
                }
            },
            { "USED":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table of the method used for the computation",
                  "Standards"   : "PROV:used",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Not null",
                  "Automation"  : "Set when the `Statistics` entry is created"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Statistics', 'sourceColumn' : 'USED', 'targetTable' : 'StatisticalMethods', 'targetColumn' : 'ID_STATISTICAL_METHOD' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_STATISTICS" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_STATISTICS = None
        self.DATE = None
        self.QUERY = None
        self.USED = None # Foreign key from the table  StatisticalMethods 
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Statistics"

    def validate(self, update=False):
        Table.validate(self)
        if (self.DATE != None and
            not iso8601(self.DATE)):
            raise InvalidEntity('ERROR: Class: ' + self.__class__.__name__ + ': Invalid column: DATE')

# Specialisation of PROV:Activity
class Study(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Study` table records units of scientific work, representing collections of `Process`es, data, and outputs.",
            "Standards"  : "PROV:Activity",
            "Automation" : "Some fields may be populated automatically when `Process`es are grouped into Studies."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_STUDY":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Study`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "TITLE":
                { "Type"        : "TEXT",
                  "Description" : "Title or name of the `Study`",
                  "Standards"   : "dc:title",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "START_TIME":
                { "Type"        : "DATE",
                  "Description" : "Start time of the `Study`",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "May be inferred from earliest `Process`"
                }
            },
            { "END_TIME":
                { "Type"        : "DATE",
                  "Description" : "End time of the `Study`",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "May be inferred from latest `Process`"
                }
            },
            { "PROJECT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Project` table of the `Project` this `Study` belongs to",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Project`",
                  "Null"        : "Optional",
                  "Automation"  : "None"
                }
            },
            { "PART":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table if this `Study` is part of another `Study`",
                  "Standards"   : "PROV:wasPartOf",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Null if not part of another `Study`",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Studies', 'sourceColumn' : 'PROJECT', 'targetTable' : 'Projects', 'targetColumn' : 'ID_PROJECT' }, 
                { 'sourceTable' : 'Studies', 'sourceColumn' : 'PART', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY'  }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_STUDY" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        # As all this  is held in memory, the  next key has to
        # be calculated -  this means that autoincrment should
        # not be used.

        self.ID_STUDY = None
        self.TITLE = None
        self.START_TIME = None
        self.END_TIME = None
        self.PROJECT =  None # Foreign key in table Projects
        self.PART = None # Foreign key in table Studies
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Studies"

    def validate(self, update=False):
        Table.validate(self)
        if (self.START_TIME != None and
        not iso8601(self.START_TIME)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: START_TIME: ' +
                self.START_TIME)
        if self.END_TIME != None:
            if not iso8601(self.END_TIME):
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Invalid column: END_TIME: ' +
                    self.END_TIME)
        if self.END_TIME != None and self.START_TIME != None:
            if self.START_TIME > self.END_TIME:
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Invalid column: START_TIME,END_TIME: ' +
                    self.START_TIME +
                    ' ' +  
                    self.END_TIME + '\n')
        if update == False:
            notNones = 0
            if self.PROJECT != None:
                notNones += 1
            if self.PART != None:
                notNones += 1
            if notNones != 1 and notNones != 2:
                raise InvalidEntity('ERROR: Class: ' + 
                    self.__class__.__name__ + 
                    ': Must have at least one or both of: PROJECT,PART\n')

class Tag(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Tag` table records tags that can be used to classify and annotate other entities in the system.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_TAG":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Tag`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_TAG" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_TAG = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Tags"


# Many-to-many
class TagMap(Table):
    @classmethod
    def is_relation(cls):
        return True 
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `TagMap` table records the association of `Tag`s with other entities such as `Application`s, `Box`es, `Documentation`, Studies, and Methods.",
            "Standards"  : "None",
            "Automation" : "`Tag`s may be applied manually by users or inferred automatically based on metadata and usage."
        }

    @classmethod
    def columns(cls):
        return [
            { "TAG":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Tag` table of the `Tag` being applied",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Tag`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table if the `Tag` applies to an `Application`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "ASSUMPTION":
                { "Type"        : "TEXT",
                  "Description" : "ID in Assumptoin table if the `Tag` applies to an `Assumption`.",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of an `Assumption`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "BOX":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table if the `Tag` applies to a `Box`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table if the `Tag` applies to a `BoxType`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "DOCUMENTATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Documentation` table if the `Tag` applies to `Documentation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Documentation`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "OTHER_TAG":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Tag` table if the `Tag` relates to another `Tag`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Tag`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "PERSON":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table is the `Person` in the `Person` table.",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Tag`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "STATISTICAL_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalMethod` table if the `Tag` applies to a statistical method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalMethod`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "STUDY":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Study` table if the `Tag` applies to a `Study`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Study`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table if the `Tag` applies to a visualisation method",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Null if not applicable",
                  "Automation"  : "None"
                }
            },
       ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Tags', 'sourceColumn' : 'TAG', 'targetTable' : 'Tags', 'targetColumn' : 'ID_TAG' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'OTHER_TAG', 'targetTable' : 'Tags', 'targetColumn' : 'ID_TAG' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'BOX_TYPE', 'targetTable' : 'BoxTypes', 'targetColumn' : 'ID_BOX_TYPE' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'BOX', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'DOCUMENTATION', 'targetTable' : 'Documentation', 'targetColumn' : 'ID_DOCUMENTATION' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'STATISTICAL_METHOD', 'targetTable' : 'StatisticalMethods', 'targetColumn' : 'ID_STATISTICAL_METHOD' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'STUDY', 'targetTable' : 'Studies', 'targetColumn' : 'ID_STUDY' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'PERSON', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' },
                { 'sourceTable' : 'TagMaps', 'sourceColumn' : 'ASSUMPTION', 'targetTable' : 'Assumptions', 'targetColumn' : 'ID_ASSUMPTION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "TAG", "BOX_TYPE" ],
             [ "TAG", "OTHER_TAG"    ],
             [ "TAG", "APPLICATION"    ],
             [ "TAG", "BOX" ],
             [ "TAG", "DOCUMENTATION" ],
             [ "TAG", "STUDY" ],
             [ "TAG", "ASSUMPTION" ],
             [ "TAG", "STATISTICAL_METHOD" ],
             [ "TAG", "PERSON" ],
             [ "TAG", "VISUALISATION_METHOD" ] ]


    def __init__(self, values = None):
        Table.__init__(self)
        self.TAG = None  # Foreign key of the table Tags
        self.OTHER_TAG = None  # Foreign key of the table Tags
        self.BOX_TYPE = None  # Foreign key of the table BoxTypes
        self.APPLICATION = None  # Foreign key of the table Applications
        self.BOX = None  # Foreign key of the table Boxes
        self.ASSUMPTION = None  # Foreign key of the table Boxes
        self.PERSON = None  # Foreign key of the table Boxes
        self.DOCUMENTATION = None  # Foreign key of the table Documentation
        self.VISUALISATION_METHOD = None  # Foreign key of the table Documentation
        self.STATISTICAL_METHOD = None  # Foreign key of the table Documentation
        self.STUDY = None  # Foreign key of the table Studies
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "TagMaps"

    def validate(self, update=False):
        Table.validate(self)
        notNones = 0
        if self.BOX_TYPE != None:
            notNones += 1
        if self.APPLICATION != None:
            notNones += 1
        if self.BOX != None:
            notNones += 1
        if self.DOCUMENTATION != None:
            notNones += 1
        if self.STATISTICAL_METHOD != None:
            notNones += 1
        if self.VISUALISATION_METHOD != None:
            notNones += 1
        if self.PERSON != None:
            notNones += 1
        if self.ASSUMPTION != None:
            notNones += 1
        if self.STUDY != None:
            notNones += 1
        if self.OTHER_TAG != None:
            notNones += 1
        if notNones != 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Ambiguous primary key: ' +
                " BOX_TYPE: " +
                str(self.BOX_TYPE) +
                " APPLICATION: " +
                str(self.APPLICATION) +
                " BOX: " +
                str(self.BOX) +
                " DOCUMENTATION: " +
                str(self.DOCUMENTATION) +
                " STATISTICAL_METHOD: " +
                str(self.STATISTICAL_METHOD) +
                " VISUALISATION_METHOD: " +
                str(self.VISUALISATION_METHOD) +
                " PERSON: " +
                str(self.PERSON) +
                " ASSUMPTION: " +
                str(self.ASSUMPTION) +
                " STUDY: " +
                str(self.STUDY) +
                " TAG: " +
                str(self.OTHER_TAG))

# Specialisation of PROV:Agent
# Automatic population?
class User(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `User` table records system user accounts, linking operating system user information to a `Person`.",
            "Standards"  : "PROV:Agent",
            "Automation" : "Most values are obtained automatically from the operating system."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_USER":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `User`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "HOME_DIR":
                { "Type"        : "TEXT",
                  "Description" : "Home directory of the user",
                  "Standards"   : "POSIX",
                  "Validation"  : "Valid file path",
                  "Automation"  : "Retrieved from the operating system"
                }
            },
            { "ACCOUNT_OF":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Person` table of the `Person` this `User` account belongs to",
                  "Standards"   : "PROV:actedOnBehalfOf",
                  "Validation"  : "Must be an ID of a `Person`",
                  "Null"        : "Not null",
                  "Automation"  : "Resolved from system/user configuration"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Users', 'sourceColumn' : 'ACCOUNT_OF', 'targetTable' : 'Persons', 'targetColumn' : 'ID_PERSON' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_USER" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_USER = None
        self.HOME_DIR = None
        self.ACCOUNT_OF = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Users"

# Many-to-many
class Uses(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Uses` table records that an `Application` uses a `BoxType` as an input or dependency.",
            "Standards"  : "PROV:used",
            "Automation" : "May be inferred automatically based on `Application` execution and detected `Input`s."
        }

    @classmethod
    def columns(cls):
        return [
            { "APPLICATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Application` table of the `Application` that uses the input",
                  "Standards"   : "PROV:Activity",
                  "Validation"  : "Must be an ID of an `Application`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "BOX_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table of the type of `Box` that is used",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Not null",
                  "Automation"  : "None"
                }
            },
            { "IN_FILE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `BoxType` table if the `Uses` input is contained within another file",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `BoxType`",
                  "Null"        : "Null if LOCATOR is not 'in-file'",
                  "Automation"  : "None"
                }
            },
            { "LOCATOR":
                { "Type"        : "TEXT",
                  "Description" : "Description of how to locate the `Uses` input",
                  "Standards"   : "None",
                  "Validation"  : "Formatted rule string",
                  "Automation"  : "None"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Uses', 'sourceColumn' : 'APPLICATION', 'targetTable' : 'Applications', 'targetColumn' : 'ID_APPLICATION' },
                { 'sourceTable' : 'Uses', 'sourceColumn' : 'BOX_TYPE', 'targetTable' : 'BoxTypes', 'targetColumn' : 'ID_BOX_TYPE' },
                { 'sourceTable' : 'Uses', 'sourceColumn' : 'IN_FILE', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "APPLICATION", "BOX_TYPE" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.OPTIONALITY = None
        self.LOCATOR = None
        self.APPLICATION = None # Foreign key in the table Applications
        self.BOX_TYPE = None # Foreign key in the table BoxType
        self.IN_FILE = None # Foreign key in the table `Box`es
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Uses"

    def validate(self, update=False):
        Table.validate(self)
        if (self.OPTIONALITY.lower() != 'required' and
            self.OPTIONALITY.lower() != 'optional' and
            self.OPTIONALITY.lower() != 'depends'):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: OPTIONALITY: ' +
                self.OPTIONALITY)
        # Cannot do a database query to check for presence of IN_FILE,
        # so will have to rely on the constraints when the the 
        # database is committed
        if (self.LOCATOR != None and
            not locator.match(self.LOCATOR)):
            raise InvalidEntity('ERROR: Class: ' + self.__class__.__name__ + ': Invalid column: LOCATOR')
            
# Specialisation of PROV:Entity
# Automatic population?
class Value(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Value` table represents values of Variables or `StatisticalVariable`s. It is a virtual table whose entries are retrieved from `Box`es rather than stored directly.",
            "Standards"  : "PROV:Entity",
            "Automation" : "`Value`s are not stored explicitly; they are retrieved dynamically from `Box`es based on `Content` specifications."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_VALUE":
                { "Type"        : "TEXT",
                  "Constraint"  : "PRIMARY KEY", # This is interesting, it
                 # identifies this entry as primary, but this is only primary in
                 # addition to another foreign key - this is slightly broken - it
                 # breaks the consistency of the model. I need to think about
                 # this.
                  "Description" : "Identifier or representation of the value",
                  "Standards"   : "None",
                  "Validation"  : "This should be a unique string",
                  "Automation"  : "Retrieved from underlying data in `Box`"
                }
            },
            { "UNITS":
                { "Type"        : "TEXT",
                  "Description" : "The units of the value.",
                  "Standards"   : "None",
                  "Validation"  : "None",
                  "Automation"  : "None."
                }
            },
            { "FORMAT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Variable` table of the `Variable` this `Value` corresponds to",
                  "Standards"   : "None",
                  "Validation"  : "Values are not alway numbers.",
                  "Automation"  : "None."
                }
            },
            { "VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Variable` table of the `Variable` this `Value` corresponds to",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Variable`",
                  "Null"        : "Null if STATISTICAL_VARIABLE is used",
                  "Automation"  : "Resolved via `Content` definitions"
                }
            },
            { "STATISTICAL_VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `StatisticalVariable` table if this `Value` is the result of a statistical computation",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `StatisticalVariable`",
                  "Null"        : "Null if VARIABLE is used",
                  "Automation"  : "Resolved via statistical processing"
                }
            },
            { "PARAMETER":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Parameter` table if this `Value` corresponds to a parameter",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Parameter`",
                  "Null"        : "Optional",
                  "Automation"  : "Resolved during method execution"
                }
            },
            { "STATISTICAL_PARAMETER":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Statistics` table if this `Value` corresponds to a Statistic",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a Statistic",
                  "Null"        : "Optional",
                  "Automation"  : "Resolved during method execution"
                }
            },
             { "VISUALISATION_PARAMETER":
                { "Type"        : "TEXT",
                  "Description" : "ID in the `Visualisation` table if this `Value` corresponds to a `Visualisation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Visualisation`",
                  "Null"        : "Optional",
                  "Automation"  : "Resolved during method execution"
                }
            },
             { "RESULT_OF":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Statistics` table if this `Value` is the result of a statistical computation",
                  "Standards"   : "PROV:wasGeneratedBy",
                  "Validation"  : "Must be an ID of a `Statistics`",
                  "Null"        : "Optional",
                  "Automation"  : "Set when statistical outputs are generated"
                }
            },
            { "TIME":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Context` table representing the time associated with the `Value`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Context`",
                  "Null"        : "Optional",
                  "Automation"  : "Derived from `Content` locators"
                }
            },
            { "SPACE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Context` table representing the spatial context of the `Value`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Context`",
                  "Null"        : "Optional",
                  "Automation"  : "Derived from `Content` locators"
                }
            },
            { "AGENT":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Context` table representing the agent associated with the `Value`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Context`",
                  "Null"        : "Optional",
                  "Automation"  : "Derived from `Content` locators"
                }
            },
            { "LINK":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Context` table representing link relationships associated with the `Value`",
                  "Standards"   : "None",
                  "Validation"  : "Must be an ID of a `Context`",
                  "Null"        : "Optional",
                  "Automation"  : "Derived from `Content` locators"
                }
            },
            { "CONTAINED_IN":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table from which the `Value` is retrieved",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Not null",
                  "Automation"  : "Determined from data source"
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Value', 'sourceColumn' : 'VARIABLE', 'targetTable' : 'Variables', 'targetColumn' : 'ID_VARIABLE' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'STATISTICAL_VARIABLE', 'targetTable' : 'StatisticalVariables', 'targetColumn' : 'ID_STATISTICAL_VARIABLE' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'PARAMETER', 'targetTable' : 'Parameters', 'targetColumn' : 'ID_PARAMETER' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'STATISTICAL_PARAMETER', 'targetTable' : 'Statistics', 'targetColumn' : 'ID_STATISTICS' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'VISUALISATION_PARAMETER', 'targetTable' : 'Visualisations', 'targetColumn' : 'ID_VISUALISATION' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'RESULT_OF', 'targetTable' : 'Statistics', 'targetColumn' : 'ID_STATISTICS' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'CONTAINED_IN', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'TIME', 'targetTable' : 'Contexts', 'targetColumn' : 'ID_CONTEXT' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'SPACE', 'targetTable' : 'Contexts', 'targetColumn' : 'ID_CONTEXT' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'AGENT', 'targetTable' : 'Contexts', 'targetColumn' : 'ID_CONTEXT' },
                { 'sourceTable' : 'Value', 'sourceColumn' : 'LINK', 'targetTable' : 'Contexts', 'targetColumn' : 'ID_CONTEXT' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_VALUE", "VARIABLE"  ],
                 [ "ID_VALUE", "STATISTICAL_VARIABLE"  ],
                 [ "ID_VALUE", "PARAMETER"  ],
                 [ "ID_VALUE", "STATISTICAL_PARAMETER"  ],
                 [ "ID_VALUE", "VISUALISATION_PARAMETER"  ],
                 [ "ID_VALUE", "RESULT_OF"  ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        # One of time, space, agent or link must not be null.
        self.ID_VALUE = None
        self.FORMAT = None
        self.UNITS = None
        self.VARIABLE = None # Foreign key in the table Variables
        self.STATISTICAL_VARIABLE = None # Foreign key in the table StatisticalVariables
        self.PARAMETER = None # Foreign key in the table Parameters
        self.STATISTICAL_PARAMETER = None # Foreign key in the table Statistics
        self.VISUALISATION_PARAMETER = None # Foreign key in the table Visualisations
        self.RESULT_OF = None # Foreign key in the table Statistics
        self.CONTAINED_IN = None # Foreign key in the table Boxes
        self.TIME = None # Foreign key in the table Contexts
        self.SPACE = None # Foreign key in the table Contexts
        self.AGENT = None # Foreign key in the table Contexts
        self.LINK = None # Foreign key in the table Contexts
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Value"

        
class Variable(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Variable` table records variables that describe data, including their name, type, and roles such as time, space, agent, or link.",
            "Standards"  : "None",
            "Automation" : "`Variable`s are generally defined by the user; some roles may be inferred during data processing."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_VARIABLE":
                { "Type"        : "TEXT",
                  "Description" : "Identifier of the variable",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "None"
                }
            },
            { "NAME":
                { "Type"        : "TEXT",
                  "Description" : "Name of the variable",
                  "Standards"   : "None",
                  "Validation"  : "String",
                  "Automation"  : "None"
                }
            },
            { "DATA_TYPE":
                { "Type"        : "TEXT",
                  "Description" : "Data type of the variable",
                  "Standards"   : "XSD",
                  "Validation"  : "Valid XSD data type or URI",
                  "Automation"  : "None"
                }
            },
            { "IS_AGENT":
                { "Type"        : "INTEGER",
                  "Description" : "Indicates whether this variable represents an agent identifier",
                  "Standards"   : "None",
                  "Validation"  : "True or False",
                  "Automation"  : "None"
                }
            },
            { "IS_LINK":
                { "Type"        : "INTEGER",
                  "Description" : "Indicates whether this variable represents a link identifier",
                  "Standards"   : "None",
                  "Validation"  : "True or False",
                  "Automation"  : "None"
                }
            },
            { "IS_SPACE":
                { "Type"        : "INTEGER",
                  "Description" : "Indicates whether this variable represents spatial information",
                  "Standards"   : "None",
                  "Validation"  : "True or False",
                  "Automation"  : "None"
                }
            },
            { "IS_TIME":
                { "Type"        : "INTEGER",
                  "Description" : "Indicates whether this variable represents temporal information",
                  "Standards"   : "None",
                  "Validation"  : "True or False",
                  "Automation"  : "None"
                }
            }
        ]

    def __init__(self, values = None):
        Table.__init__(self)
        # only one of is_agent, is_link, is_space or is_time can have value 1,
        # the others must be zero
        self.ID_VARIABLE = None
        self.DATA_TYPE = None
        self.IS_AGENT = 0 # '[0,1]'
        self.IS_LINK = 0 #'[0,1]'
        self.IS_SPACE = 0  # '[0,1]'
        self.IS_TIME = 0 # '[0,1]'
        Table.set_values(self,values)

    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_VARIABLE" ] ]

    @classmethod
    def tableName(cls):
        return "Variables"


    def validate(self, update=False):
        Table.validate(self)
        total = self.IS_AGENT + self.IS_LINK + self.IS_SPACE + self.IS_TIME
        if total > 1:
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Only one of the following may be true: ' +
                ' IS_AGENT: ' +
                self.IS_AGENT, +
                ', IS_LINK: ' +
                self.IS_LINK +
                ', IS_SPACE: ' +
                self.IS_SPACE +
                ', IS_TIME: ' +
                self.IS_TIME)
            
# Specialisation of PROV:Activity
# Automatic population?
class Visualisation(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `Visualisation` table records visualisations generated from data, including when they were created and how the data was selected.",
            "Standards"  : "PROV:Activity",
            "Automation" : "Entries may be created automatically when a visualisation is generated."
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_VISUALISATION":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `Visualisation`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            },
            { "DATE":
                { "Type"        : "DATE",
                  "Description" : "Date the `Visualisation` was created",
                  "Standards"   : "ISO8601",
                  "Validation"  : "Datetime string",
                  "Automation"  : "Set automatically at creation time"
                }
            },
            { "QUERY":
                { "Type"        : "TEXT",
                  "Description" : "Query used to select data for the `Visualisation`",
                  "Standards"   : "None",
                  "Validation"  : "Formatted string",
                  "Automation"  : "None"
                }
            },
            { "VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "ID in `VisualisationMethod` table of the method used to generate the Visualisation",
                  "Standards"   : "PROV:used",
                  "Validation"  : "Must be an ID of a `VisualisationMethod`",
                  "Null"        : "Not null",
                  "Automation"  : "Set when the `Visualisation` is created"
                }
            },
            { "CONTAINED_IN":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Box` table of the `Box` containing the `Visualisation`",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `Box`",
                  "Null"        : "Optional",
                  "Automation"  : "Set if output is stored in a `Box`"
                }
            }
        ]

    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'Visualisations', 'sourceColumn' : 'VISUALISATION_METHOD', 'targetTable' : 'VisualisationMethods', 'targetColumn' : 'ID_VISUALISATION_METHOD' },
                {'sourceTable' : 'Visualisations', 'sourceColumn' : 'CONTAINED_IN', 'targetTable' : 'Boxes', 'targetColumn' : 'ID_BOX' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_VISUALISATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_VISUALISATION = None
        self.VISUALISATION_METHOD = None
        self.QUERY = None
        self.DATE = None
        self.CONTAINED_IN = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "Visualisations"

    def validate(self, update=False):
        Table.validate(self)
        if (not iso8601(self.DATE)):
            raise InvalidEntity('ERROR: Class: ' + 
                self.__class__.__name__ + 
                ': Invalid column: DATE = ' +
                self.DATE)

class VisualisationMethod(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `VisualisationMethod` table records methods used to generate visualisations from data.",
            "Standards"  : "None",
            "Automation" : "None"
        }

    @classmethod
    def columns(cls):
        return [
            { "ID_VISUALISATION_METHOD":
                { "Type"        : "TEXT",
                  "Description" : "Unique identifier for the `VisualisationMethod`",
                  "Standards"   : "None",
                  "Validation"  : "Must be unique",
                  "Automation"  : "Automated by the instantiating framework"
                }
            }
        ]
    @classmethod
    def primaryKeys(cls):
        return [ [ "ID_VISUALISATION_METHOD" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.ID_VISUALISATION_METHOD = None
        Table.set_values(self,values)

    @classmethod
    def tableName(cls):
        return "VisualisationMethods"


# Many-to-many
class VisualisationValue(Table):
    @classmethod
    def documentation(cls):
        return {
            "Description": "The `VisualisationValue` table links  a `Value` to a `Visualisation`, indicating which `Value`s are used in a given `Visualisation`.",
            "Standards"  : "PROV:used",
            "Automation" : "Entries are created automatically when a `Visualisation` is generated."
        }

    @classmethod
    def columns(cls):
        return [
            { "VALUE":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Value` table of the `Value` used in the `Visualisation`.",
                  "Standards"   : "PROV:Entity",
                  "Validation"  : "Must be an ID of a `Value`.",
                  "Null"        : "Not null.",
                  "Automation"  : "Populated automatically when the `Visualisation` is created."
                }
            },
            { "VISUALISATION":
                { "Type"        : "TEXT",
                  "Description" : "ID in `Visualisation` table of the `Visualisation` using the `Value`.",
                  "Standards"   : "PROV:Activity.",
                  "Validation"  : "Must be an ID of a `Visualisation`.",
                  "Null"        : "Not null.",
                  "Automation"  : "Populated automatically when the `Visualisation` is created."
                }
            }
        ]
    @classmethod
    def foreignKeys(cls):
        return [{ 'sourceTable' : 'VisualisationValues', 'sourceColumn' : 'VALUE', 'targetTable' : 'Value', 'targetColumn' : 'ID_VALUE' },
                { 'sourceTable' : 'VisualisationValues', 'sourceColumn' : 'VISUALISATION', 'targetTable' : 'Visualisations', 'targetColumn' : 'ID_VISUALISATION' }]
    @classmethod
    def primaryKeys(cls):
        return [ [ "VALUE", "VISUALISATION" ] ]

    def __init__(self, values = None):
        Table.__init__(self)
        self.VALUE = None # Foreign key in the table Value
        self.VISUALISATION = None # Foreign key in the table Visualisations
        Table.set_values(self,values)
        
    @classmethod
    def tableName(cls):
        return "VisualisationValues"

def connect_db():
    """function to create a connection with a db
    """
    conn = None

    if db_type == 'gremlin' or db_type == 'janusgraph': 
        try:
            conn = Client(gremlin_host,
                         'g', 
                         message_serializer=GraphSONSerializersV3d0()
            )
#            conn = Client(gremlin_host,
#                         'g', 
#                         message_serializer=GraphBinarySerializersV1()
#            )
        except gremlin_python.Error as e:
            print("error %s:\n" % e.args[0])
            raise
        finally:
            return conn
       
    elif db_type == 'sqlite3': 
        try:
            #conn = sqlite3.connect(db_fqfn, row_factory=sqlite3.Row)
            conn = sqlite3.connect(db_file)
            # This next statement is very important as it turns off
            # Python's sqlite module's rather random transaction
            # methodology.
            conn.row_factory = dict_factory
            conn.isolation_level = None

            cur = conn.cursor()    
        except sqlite3.Error as e:
            sys.stderr.write("error %s:\n" % e.args[0])
            sys.exit(1)
        finally:
            return conn
    elif db_type == 'postgres':
        try:
            conn = psycopg2.connect(dbname=db_name, user=db_user,  host=db_host,  password=db_passwd, cursor_factory = RealDictCursor)
            conn.set_session(autocommit = True)
        except psycopg2.Error as e:
            sys.stderr.write("error %s:\n" % e.args[0])
            sys.exit(1)
        finally:
            return conn
    else:
        sys.stderr.write("LIB: connect_db: Unknown database type %s \n" % db_type)
        raise

def disconnect_db(conn):
    conn.close()

def create_tables(conn):
    """Creates all the tables for the Repository for a Social Simulation database
    """

    if table_exists(conn, "Applications"):
       return
    
    if db_type == 'janusgraph':
        for entity in Table.commonFields():
            for attribute, valuePairs in entity.items():
                bindings = { "name": attribute }
                if debug:
                    sys.stderr.write("GREMLIN create_tables: property " + gremlin_make_a_property + " with bindings " + str(bindings) + ".\n")
                conn.submit(gremlin_make_a_property, bindings = bindings, request_options = gremlin_request_options).all().result()

    for name, cls in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table:
            cls.create_table(conn)

    if db_type == 'sqlite3' or db_type == 'postgres':
        for name, cls in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table and hasattr(cls, 'foreignKeys') and callable(getattr(cls, "foreignKeys")):
                cls.alter_table(conn)

def empty_tables(conn):
    """Truncates all the tables for the Repository for a Social Simulation database
    """
    if db_type == 'janusgraph' or db_type == 'gremlin':
        # Drop all edges
        while True:
            count = conn.submit("g.E().count()").all().result()[0]
            print(f"Edges remaining: {count}")
            if count == 0:
                break
            conn.submit(
                "g.with('evaluationTimeout', 3000000).E().limit(1000).drop().iterate()"
            ).all().result()

        # Drop all vertices
        while True:
            count = conn.submit("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V().count()").all().result()[0]
            print(f"Vertices remaining: {count}")
            if count == 0:
                break
            conn.submit(
                "g.with('evaluationTimeout', 3000000).V().limit(1000).drop().iterate()"
            ).all().result()
    elif db_type == 'postgres' or db_type == 'sqlite3':
        for name, cls in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table:
                cls.truncate_table(conn)
    else:
        raise Exception(f"Trying to truncate an unsuitable database {db_type}.\n")

def delete_tables(conn):
    """Truncates all the tables for the Repository for a Social Simulation database
    """
    if db_type == 'janusgraph':
        empty_tables(conn)
        print(""" We have emptied the database, but you really need to empty and restart the database to get rid of stuff.""")
    elif db_type == 'postgres' or db_type == 'sqlite3':
        for name, cls in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table:
                cls.dropTable(conn)
    else:
        raise Exception(f"Trying to delete an unsuitable database {db_type}.\n")
       
# Helper Functions
# ================

# Function to validate the database intialisation specification.
# This used to be done as a dictionary, but there is no way of validating
# duplicated for dictionairies in Python, so we must enter the specification
# as an array, then create a dictionary from it, making sure there are no
# duplicates, for both the dictionary key and the database keys. This 
# was not part of the specification, but I have done this, as the intialisation
# specification is getting unduly large.

   
def is_positive_int(s):
    """A function to get a positive integer
    """
    try:
        int(s)
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False

def iso8601(str):
    """
    Adapted from https://pypi.python.org/pypi/iso8601
    
        I adapted this because his version was not strict. This one
        is.

    Note we don't need the Python place holders, but I will leave
    them because I think it makes the string a bit clearer.
    
    """
    
    if ISO8601_REGEX.match(str):
        return True
    return False

def ip(address):
    """
    Checks for a valid IP address
    Lifted wholesale from https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
    """
    if IPV6_or_IPV4_REGEX.match(address):
        return True
    return False

def mimetype(allowableMimeTypes):
    """From https://www.iana.org/assignments/media-types/media-types.xhtml
    """
    
    global mimetypes_map
    
    for str in allowableMimeTypes.split(";"):
        if str.lower() not in mimetypes_map:
            return False
    return True

class InvalidNode(Exception):
    pass

class InvalidEdge(Exception):
    pass

def graph():

    return graphviz.Digraph(comment='Workflow')

def derive_edges():

    edges= {}
    foreign_key_table = {}
    for name, cls in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table:
            edges.update(derive_edge(cls.schema()))
    if debug:
        for edge in edges:
            sys.stderr.write('SQL derive_edges: ALL edges: ' + str(edge) + ' = ' + str(edges[edge]) + "\n")
    return edges                       
        
def derive_edge(schema):
    """
    This is a dictionary indexed on the name of the edge
    Each edge value is a dictionary which may have one of four indexes

    + join
    + source
    + target
    + id

    The values of these dictionaries may contain a single value, as in 
    the case of source and target, otherwise "join" is another dictionary.

    The simple values in id, source and target contain a single entry in
    the form:

    table(column_name)

    The "source" specifies the source table of the edge
    The "target" specifies the target table of the edge
    The "id" specifies the where you will find the origin in the source
        table

    The join through another relation is a little bit more comple

    source -> join.source <=> join.target -> target 

    edge[edge_name] = { join = {source = join.source(join.source.column)
                                target = join.target(join.target.colum) }
                        source = source(sourceColumn)
                        target = target(targetColumn) }

    """
    edge = {}
    node = re.search(
        r'CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\S*)\s*\(\s*$',
        schema, re.MULTILINE)    
    if node == None:
        sys.exit("No create table statement for " + schema)
    table = globals()[getattr(Table, node.group(1))()]
    # This next list which keys have alread been used as many-to-many keys
    # and therefore cannot be used as  one-to-one keys
    used = list()
    # The next test indicates if the table itself is merely a link
    if table.is_relation():
        
        for key in table.primaryKeys():
            edgeDetail = {}
            source_foreign_key = re.search(r'^\s*FOREIGN\s+KEY\s*\(' + key[0].upper()  +  r'\)\s*REFERENCES\s+(\S+)\s*\((\S+)\)', schema, re.MULTILINE)
            target_foreign_key = re.search(r'^\s*FOREIGN\s+KEY\s*\(' + key[1].upper()  +  r'\)\s*REFERENCES\s+(\S+)\s*\((\S+)\)', schema, re.MULTILINE)
            if debug:
                sys.stderr.write("SQL: derive_edge: " + str(key[0]) + " -> " + str(source_foreign_key.group(1)) + "(" + str(source_foreign_key.group(2)) + ")\n")
                sys.stderr.write("SQL: derive_edge: " + str(key[1]) + " -> " + str(target_foreign_key.group(1)) + "(" + str(target_foreign_key.group(2)) + ")\n")
            join = {}
            edgeDetail["source"] = str(source_foreign_key.group(1)) + "(" + str(source_foreign_key.group(2)) + ")"
            edgeDetail["target"] = str(target_foreign_key.group(1)) + "(" + str(target_foreign_key.group(2)) + ")"
            join["source"] = table.tableName() + "(" + key[0] + ")"
            join["target"] = table.tableName() + "(" + key[1] + ")"
            edgeDetail["join"] = join
            used.append(key[0])
            used.append(key[1])
            edge[table.__name__.lower() + "-to-" + key[1].lower()] = edgeDetail                

    for key in table.foreignKeys():
        if key not in used:
            edgeDetail = {}
            targetTable = globals()[getattr(Table, key["sourceTable"])()]
            edgeDetail["source"] = (
                key["sourceTable"] + "(" + 
                key["sourceColumn"] + ")")
            edgeDetail["target"] = (
                key["targetTable"] + "(" + 
                key["targetColumn"] + ")")
            edgeDetail["id"] = ( table.tableName() + 
                "(" + ",".join(table.primaryKeys()[0]) +")" )
            edge[key["sourceColumn"].lower() + '-from-' + table.__name__.lower()] = ( edgeDetail )                

    return edge

def labels():

    labels = {} 
    for name, cls in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table and hasattr(cls, 'columns') and callable(getattr(cls, 'columns')):
            keys = [list(d.keys())[0] for d in cls.columns()]
            labels.update({ str(cls.__name__) : keys })
    return labels

def get_nodes(conn, nodes, labels):
    with conn:
        activeNodes = {}    

        cur = conn.cursor()
        for node in nodes:
            table = globals()[getattr(Table, node)()]
            if labels[node] == None:
                sys.exit('Problem with ' + node + ': no labels provided')
            nodeSQL =   'SELECT ' + ','.join(labels[table.tableName()]) + ' FROM ' + table.tableName()

            if debug:
                sys.stderr.write("SQL: get_nodes: " + nodeSQL + "\n")
            cur.execute(nodeSQL)
            rows = cur.fetchall()
            for row in rows:
                if debug:
                    sys.stderr.write("SQL: get_nodes: Row = " + str(row) + "\n")
                nodeText = "" 

                # A dictionary should make life easier.
                # The first line appears to be treated differently
                className = ""
                for primary_key in table.primaryKeys():
                    for part_primary_key in primary_key:
                        for key in row:
                            if key.lower() == part_primary_key.lower() and row[key] != None:
                                if debug:
                                    sys.stderr.write("SQL: get_nodes: " + "table = " + str(table) + "key " + str(key) + " = " + str(row[key]) + ' in row ' + str(row) + "\n")
                                className = className + str(row[key])
                for key in row:
                    if key.lower() in [a.lower()  for a in nodes[node]]:
                        nodeText = '<B>' + str(row[key]) + '</B><BR/>' + nodeText
                    elif row[key.lower()] == None:
                        pass
                    else:
                        nodeText = nodeText + '<BR/>' +  str(key) + ' = ' + format_text(row[key])
                nodeText = '<<U>' + node + '</U><BR/>' + nodeText + '>'
                activeNodes[(str(node),str(className))] = nodeText

    return activeNodes;

def draw_nodes(conn, graph, nodes, labels):
    activeNodes = get_nodes(conn, nodes, labels)
    for activeNode in activeNodes:
        graph.node(str(activeNode[0]) + '.' +  
            str(activeNode[1]), activeNodes[activeNode])
    return activeNodes
    
def format_text(text, length=30):
    # Remove any daft formatting and blank spacing.
    text = str(text)
    text = text.replace('\\n', ' ')
    text = ' '.join(text.splitlines())
    tokens = re.split(tidySpace,text)
    output = ''
    lineLength = 0
    for token in tokens:
        if lineLength + len(token) > length:
            output = output + "<BR/>" + token
            lineLength = len(token)
        else:
            output = output + " " + token
            lineLength = lineLength + 1 + len(token)
    return output

    

def get_edges(conn, edges, activeNodes):
    with conn:
        # This reads the edges dictionary, locates those involved with the
        # active nodes, and then reads the necessary information from the database
        # about those connections.

        # Because edges being dealt with in this function are either
        # one-to-one or one-to-many, then because of the possibility
        # of the latter you have to detect the link from the target ID to
        # the source ID, which must perforce give a one-to-one linkage.

        # The join subclause is a relational device which is a link in-
        # stantiated as a table, and in this case we have:

        # source -> join.source <=> join.target -> target 

        cur = conn.cursor()
        activeEdges = {}
        for (classType,className) in activeNodes:
            if debug:
                sys.stderr.write("SQL get_edges: Class type = " + classType + " className = " + className + "\n")
            for edge in edges:
                found = re.search(r'^(.*)\((.*)\)$',edges[edge]['target'])
                if not found:
                    raise InvalidEdge
                targetTable = found.group(1) 
                targetRow = found.group(2)
                if targetTable != classType:
                    continue
                found = re.search(r'^(.*)\((.*)\)$',edges[edge]['source'])
                if not found:
                    raise InvalidEdge
                sourceTable = found.group(1)
                sourceRow = found.group(2)
                if 'join' in edges[edge]:
                    if debug:
                        sys.stderr.write("SQL get_edges: " + classType  + " Processing = " + str(edges[edge]) + "\n")
                    found = re.search(r'^(.*)\((.*)\)$',edges[edge]['join']['target'])
                    if not found:
                        raise InvalidEdge
                    mediatorTargetTable = found.group(1) 
                    mediatorTargetRow = found.group(2)
                    found = re.search(r'^(.*)\((.*)\)$',edges[edge]['join']['source'])
                    if not found:
                        raise InvalidEdge
                    mediatorSourceTable = found.group(1)
                    mediatorSourceRow = found.group(2)
                    found = re.search(r'^(.*)\((.*)\)$',edges[edge]['source'])
                    if not found:
                        raise InvalidEdge
                    idTable = found.group(1)
                    idRow = found.group(2)
                    sql_string = ("SELECT " +  
                                idRow + 
                                " FROM " +
                                idTable + ',' + mediatorSourceTable +
                                " WHERE " +
                                idTable + "." + idRow +
                                " = " +
                                mediatorSourceTable + '.' + mediatorSourceRow +
                                " AND " +
                                mediatorTargetTable + '.' + mediatorTargetRow +
                                " = '" +
                                 str(className) +
                                "'")
                else:
                    found = re.search(r'^(.*)\((.*)\)$',edges[edge]['id'])
                    if not found:
                        raise InvalidEdge
                    idTable = found.group(1)
                    idRow= found.group(2)
                    if idTable != sourceTable:
                        raise InvalidEdge

                    sql_string = ("SELECT " +  
                                idRow + 
                                " FROM " +
                                sourceTable +
                                " WHERE " +
                                sourceRow +
                                " = '" +
                                str(className) +
                                "'")

                if debug:
                    sys.stderr.write("SQL get_edges: Edge: " + sql_string + '\n')
                cur.execute(sql_string)
                rows = cur.fetchall()
                for row in rows:
                    label = edge
                    if debug:
                        sys.stderr.write("SQL get_edges: Found Edge " + edge + " = " + str(edges[edge]) + " for " + str(row) + '\n')
                    if 'label' in edges[edge]:
                        label = edges[edge]['label']
                    activeEdges[((sourceTable, str(list(row.values())[0])),
                        (classType, str(className)))] = label
                    if debug:
                        sys.stderr.write("SQL get_edges: Will draw  = " + str((sourceTable, str(list(row.values())[0]))) + " to " + str((classType, str(className))) + '\n')
        

    return activeEdges
                
def remove_orphans(nodes, edges):
    remaining_nodes = nodes.copy()
    result = nodes.copy()
    for edge in edges:
        if edge[0] in remaining_nodes:
            del remaining_nodes[edge[0]]
        if edge[1] in remaining_nodes:
            del remaining_nodes[edge[1]]
    for orphan in remaining_nodes:
        del result[orphan] 
    return result

def remove_edges(nodes,edges):
    # So my edge is of the form edge ((SourceTableName, primary_key_value) , (TargetTableName, primary_key_value)) = label
    
    edgesLeft = edges.copy()
    tables = list()
    for node in nodes:
        tables.append(node[0])
        if debug:
            sys.stderr.write("SQL removed_edges: Nodes = " + str(tables) +'\n')

    for edge in edges:
        if debug:
            sys.stderr.write("SQL removed_edges: Examining edge = " + str(edge) + " = " + str(edges[edge]) +'\n')
        if edge in edges and (edge[0][0] not in tables or edge[1][0] not in tables):
            del edgesLeft[edge]
    return edgesLeft

def save_dot(nodes, edges, output=None):

    graph = graphviz.Digraph()
    #graph.attr(ratio="fill", size = "8.3,11.7", margin = 0)
    #graph.attr(size = "8.3,11.7", margin = "0", ratio="fill")
    graph.attr(margin = "0", ratio="fill")
    
    if nodes != None:
        for node in nodes:
            graph.node(str(node[0]) + '.' +  str(node[1]), nodes[node])

    if edges != None:
        for edge in edges:
            if debug:
                sys.stderr.write("SQL save_dot: DRAWING edge = " + str(edge) + " = " + str(edges[edge]) +'\n')
            graph.edge(edge[0][0] + '.' + edge[0][1], edge[1][0] + '.' + edge[1][1], label=edges[edge])

    if output == None:
        print(graph)
    else:
        graph.save(output)

def draw_graph (conn, nodes, output):

    original_nodes = get_nodes(conn, nodes, labels())
    possible_edges = get_edges(conn, derive_edges(), original_nodes)
#    save_dot(original_nodes,possible_edges,output=output)
    active_nodes = remove_orphans(original_nodes, possible_edges)
    active_edges = remove_edges(active_nodes, possible_edges)
    save_dot(active_nodes,active_edges,output=output)

def encodeIndex (stringIndex: str):
    # I am not convinced this is the best way of doing this. It might be better
    # to use some kind of hex dump function.
    result:int = 0
    for i in range(0, len(stringIndex)):
        result = result + (256 ** i) * ord(stringIndex[i])
    return result
    

def decodeIndex ( numericIndex: int ):
    # I am not convinced this is the best way of doing this. It might be better
    # to use some kind of hex dump function.
    result = ""
    myIndex:int  = numericIndex 
    while myIndex > 0:
        digit = myIndex % 256 
        result = result + chr(digit)
        # Note the use of floor division: //
        myIndex = int((myIndex - digit) // int(256))
    return result    

def gremlin_safe_string(s: str) -> str:
    return (
        s
        .replace('\\', '\\\\')      # escape backslashes first
        .replace('\r\n', '\\n')     # Windows newlines
        .replace('\r', '\\n')       # old Mac / weird input
        .replace('\n', '\\n')       # Unix newlines
    )

def gremlin_wait_for_vertex(conn, vertex_id, key=None, retries=20, delay=2):
    """Wait until a vertex exists before proceeding"""
    query = ""
    if db_type == 'janusgraph':
        query = ( 
            "g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V().has('" +
            key +
            "','" +
            vertex_id +
            "').count()"
        )
    else:
        query = ( 
            "g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V('" +
            vertex_id +
            "').count()"
        )
    for attempt in range(retries):
        result = gremlin_submit(conn, query, 'waiting')
        if result[0] > 0:
            return True
        if debug:
            sys.stderr.write("PYTHON: gremlin_wait_for_vertex: " + str(vertex_id) + " attempt " + str(attempt + 1) + "/" + str(retries) + "\n")
        time.sleep(delay * (attempt + 1))  # exponential backoff
    return False

def table_exists(conn, table_name):

    if db_type == 'janusgraph':
        if hasattr(Table, table_name) and callable(getattr(Table, table_name)):
            query = "graph.openManagement().getVertexLabel('" + str(getattr(Table, table_name)()) + "')"
            result = gremlin_submit(conn, query, 'query')
            return result[0]
        else:
            return False
    elif db_type == 'postgres':
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = %s
                AND table_schema = 'public'
            )
        """, (table_name.lower(),))
    elif db_type == 'sqlite3':
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM sqlite_master 
                WHERE type = 'table' 
                AND name = ?
            )
        """, (table_name,))
    else:
        raise ValueError(f"LIB: table_exists: Unsupported database: {db_type}")
    
    cur = conn.cursor()
    result = cur.fetchone()

    if isinstance(result, dict):
        return bool(result['exists'])
    return bool(result[0])

def gremlin_add_edge( conn, someArgs ):

    """
    Create an edge with the given label from out_id -> in_id in a Gremlin graph,
    optionally setting edge properties from `props` dict.
    """

    edge_label = someArgs[0].split('=')[1]
    out_id = someArgs[1].split('=')[1]
    out_key = someArgs[1].split('=')[0][2:]
    in_id = someArgs[2].split('=')[1]
    in_key = someArgs[2].split('=')[0][2:]
    if edge_label not in globals().keys():
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Class {edge_label} does not exist!\n")
    cls = globals()[edge_label]
    if not cls.is_relation():
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Class {edge_label} is not a relation!\n")
    in_foreign_key = None
    out_foreign_key = None
    for keyset in cls.foreignKeys():
        if keyset['sourceColumn'].lower() == in_key:
            in_foreign_key = keyset['targetColumn']
            break
    if in_foreign_key == None:
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Relevant in foreign key for {in_id}, label {in_key} on {edge_label} does not exist!\n")
    for keyset in cls.foreignKeys():
        if keyset['sourceColumn'].lower() == out_key:
            out_foreign_key = keyset['targetColumn']
            break
    if out_foreign_key == None:
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Relevant out foreign key for {out_id}, label {out_key} on {edge_label} does not exist!\n")


    props = {}
    for arg in someArgs[3:]:
        key, value = arg.lstrip('-').split('=', 1)
        props[key.upper()] = value

    # Wait for both vertices to exist before creating edge
    if not gremlin_wait_for_vertex(conn, in_id, key = in_foreign_key):
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Timeout waiting for vertex {in_id} id: {in_foreign_key}")
    if not gremlin_wait_for_vertex(conn, out_id, key = out_foreign_key):
        raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Timeout waiting for vertex {out_id} id: {out_foreign_key}")

    if db_type == 'janusgraph':
        query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V().has('" + 
                 out_foreign_key +
                 "','" +
                 out_id + 
                 "').out('" + 
                 str(edge_label) + 
                 "').has('" + 
                 in_foreign_key +
                 "','" +
                 in_id + 
                 "')"
        )
    else:
        query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V('" + 
                 out_id + 
                 "').out('" + 
                 str(edge_label) + 
                 "').hasId('" + 
                 in_id + 
                 "')"
        )
    query += ".hasNext()"
    result = gremlin_submit(conn, query, 'exists')
    if result[0] == False:
        try:
            query = ("g.with('evaluationTimeout', " + 
               str(gremlin_timeout) +
               ").addE('" +
               str(edge_label) +
               "')" 
            )
            # Attach edge properties
            for k, v in props.items():
                query = query + ".property('" + k + "','" + v + "')"
            if db_type == 'janusgraph':
                query = (query + ".from(__.V().has('" + 
                         str(out_foreign_key) +
                         "','" +
                         str(out_id) + 
                         "')).to(__.V().has('" + 
                         str(in_foreign_key) +
                         "','" +
                         str(in_id) + 
                         "'))"
                )
            else: 
                query = (query + ".from(__.V('" + 
                         str(out_id) + 
                         "')).to(__.V('" + 
                         str(in_id) + 
                         "'))"
                )
            query += ".next()"
            result = gremlin_submit(conn, query, 'insert')
        except Exception as e:
            raise Exception(f"PYTHON: gremlin_add_edge: GREMLIN: Error creating edge: {e}\n")
    else:
        # It exists we need to get the properties of this 
        # Get existing edge properties
            if db_type == 'janusgraph':
                query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V().has('" + 
                         out_key +
                         "','" +
                         out_id + 
                         "').out('" + 
                         str(edge_label) + 
                         "').has('" + 
                         in_key +
                         "','" +
                         in_id + 
                         "')"
                )
            else:
                query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V('" + 
                         out_id + 
                         "').out('" + 
                         str(edge_label) + 
                         "').hasId('" + 
                         in_id + 
                         "')"
                )
            query += ".valueMap()"
            result = gremlin_submit(conn, query, 'properties')
            
            if result:
                existing = result[0]

                # Compare and build update query
                updates = {}
                for key, value in props.items():
                    if debug:
                        sys.stderr.write("PYTHON: gremlin_add_edge: GREMLIN: key " + key + " value " + value + "\n")
                    existing_val = existing.get(key, [None])
                    # valueMap returns lists so unwrap
                    if isinstance(existing_val, list):
                        existing_val = existing_val[0]
                    if existing_val == None or gremlin_safe_string(existing_val) != gremlin_safe_string(value):
                        updates[key] = gremlin_safe_string(value)

                # Apply updates if any differences found
                if updates:
                    if db_type == 'janusgraph':
                        query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V().has('" + 
                                 str(out_key) + 
                                 "','" +
                                 str(out_id) + 
                                 "').outE('" + 
                                 str(edge_label) + 
                                 "').where(otherV().has('" +
                                 in_key +
                                 "','" +
                                 str(in_id) + 
                                 "'))"
                        )
                    else:
                        query = ("g.with('evaluationTimeout', " + str(gremlin_timeout) + ").V('" + 
                                 str(out_id) + 
                                 "').outE('" + 
                                 str(edge_label) + 
                                 "').where(otherV().hasId('" +
                                 str(in_id) + 
                                 "'))"
                        )
                    for key, value in updates.items():
                        query += ".property('" + str(key) + "', '" + gremlin_safe_string(value) + "')"
                    query += ".next()"
                    gremlin_submit(conn, query, 'property update')

    return result

def specification():
    markdown = ""
    for name, cls in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cls) and issubclass(cls, Table) and cls != Table:
            if cls.markdown() != None:
                markdown += cls.markdown()
    return markdown

def gremlin_submit(conn, query, info, retries=10):
    for attempt in range(retries):
        try:
            if debug:
                sys.stderr.write("GREMLIN: " + inspect.stack()[1].function + ": " + info + ": " + query + ".\n")
            result = conn.submit(query).all().result()
            if debug:
                sys.stderr.write("GREMLIN: " + inspect.stack()[1].function + ": " + info + ": result: " + str(result) + ".\n")
            return result
        except GremlinServerError as e:
            error = str(e)
            # 'violates a uniqueness constraint' -> silently ignore, return None, carry on
            # Lock contention -> retry with backoff
            # Any other SchemaViolationException -> reraise as genuine error
            if 'violates a uniqueness constraint' in error:
                return None
            elif any(r in error for r in [
                'PermanentLockingException',
                'TemporaryLockingException',
                'Local lock contention',
                'Too many open transactions'] ) and attempt < retries - 1:
                # exponential backoff
                sleep = (2 ** attempt) + random.uniform(0,1)
                if debug:
                    sys.stderr.write("GREMLIN: " + inspect.stack()[0].function + ": " + info + ": waiting: " + str(sleep) + "...\n")
                time.sleep(sleep)
            else:
                raise
        except Exception as e:
            raise

