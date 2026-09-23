#!/usr/bin/env python3

__copyright__ = 'Copyright 2016'
__license__ = 'This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.'
__version__ = '1.0.0'
__authors__ = 'Doug Salt'
__credits__ = 'Gary Polhill, Lorenzo Milazzo'
__modified__ = '2017-03-02'


import sys

sys.path.append('lib')
import record as record


def _scalar(row, key=None):
    if isinstance(row, dict):
        return row[key] if key else next(iter(row.values()))
    return row[0]

def get_table_names(conn, schema='public'):
    '''Return a list of table names (ordinary, partitioned, foreign) in schema.'''
    with conn.cursor() as cur:
        cur.execute('''
            SELECT c.relname AS name
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = %s
              AND c.relkind IN ('r','p','f')
            ORDER BY c.relname;
        ''', (schema,))
        rows = cur.fetchall()
    if rows and isinstance(rows[0], dict):
        return [r['name'] for r in rows]
    return [r[0] for r in rows]

def count_rows_in_table(conn, schema, table):
    '''Return exact row count for one table.'''
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM '{schema}'.'{table}';")
        return _scalar(cur.fetchone())

def count_total_rows(conn, schema='public'):
    '''Count total number of rows across all tables in the schema.'''
    total = 0
    tables = get_table_names(conn, schema)
    print(f"Found {len(tables)} tables in schema '{schema}'")
    for t in tables:
        try:
            rows = count_rows_in_table(conn, schema, t)
            print(f'{t}: {rows}')
            total += rows
        except Exception as e:
            sys.stderr.write(f'Warning: failed to count {t}: {e}\n')
    return total

def get_vertices(gremlin_client):

    query = 'g.V().groupCount().by(label).order(local).by(values, desc)'
    result = gremlin_client.submit(query).all().result()
    print(result)
    query = "g.with('evaluationTimeout', 1200000).V().count()"
    result = gremlin_client.submit(query).all().result()
    return result

def get_edges(gremlin_client):
    query = 'g.E().groupCount().by(label).order(local).by(values, desc)'
    result = gremlin_client.submit(query).all().result()
    print(result)
    query = "g.with('evaluationTimeout', 1200000).E().count()"
    result = gremlin_client.submit(query).all().result()
    return result

def get_nodes_by_label(gremlin_client,label):
    query = "g.V().hasLabel('" + label + "').id().toList()"
    result = gremlin_client.submit(query).all().result()
    return result

if __name__ == '__main__':

    if record.debug:
        sys.stderr.write('PYTHON: totals.py: Entering...\n')

    conn = record.connect_db()
    if record.db_type == 'gremlin' or record.db_type == 'janusgraph':
#        for element in get_nodes_by_label(conn,label):
#            print(element)

        print('There are ' + str(get_vertices(conn)) + ' vertices.')
        print('There are ' + str(get_edges(conn)) + ' edges.')
    else:
        schema = 'public'
        total_rows = count_total_rows(conn, schema)
        print(f"\nGrand total rows across all tables in '{schema}': {total_rows}")

    record.disconnect_db(conn)

    if record.debug:
        sys.stderr.write('PYTHON: totals.py: Exiting...\n')
