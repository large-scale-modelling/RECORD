#!/usr/bin/env python3

_copyright__ = "Copyright 2016"
__license__ = "This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the Licence, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
__version__ = "1.1.0"
__authors__ = "Doug Salt"
__credits__ = "Gary Polhill, Lorenzo Milazzo"
__modified__ = "2026-03-12"

import argparse
import json
import subprocess
import sys

sys.path.append("lib")
import record as record


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export the configured RECORD database to the named output file."
    )
    parser.add_argument(
        "output_file",
        help=(
            "Output file to create. For Gremlin databases this will be a JSON file; "
            "for PostgreSQL databases this will be a pg_dump custom-format backup."
        ),
    )
    return parser.parse_args()


def get_vertices(gremlin_client):
    query = "g.V().with('evaluationTimeout', 300000).elementMap()"
    result = gremlin_client.submit(query).all().result()
    return result


def get_edges(gremlin_client):
    query = "g.E().with('evaluationTimeout', 3000000).elementMap()"
    result = gremlin_client.submit(query).all().result()
    return result


def stringify_keys(obj):
    if isinstance(obj, dict):
        return {str(k): stringify_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [stringify_keys(item) for item in obj]
    return obj


def save_graph_to_file(vertices, edges, filename):
    graph_data = {
        "vertices": stringify_keys(vertices),
        "edges": stringify_keys(edges),
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)
    print(f"Graph saved to {filename}")


if __name__ == "__main__":
    args = parse_args()

    if record.debug:
        sys.stderr.write("PYTHON: record-export-database.py: Entering...\n")

    conn = record.connect_db()
    try:
        if record.db_type == "gremlin":
            vertices = get_vertices(conn)
            edges = get_edges(conn)
            save_graph_to_file(vertices, edges, args.output_file)
        else:
            cmd = [
                "pg_dump",
                "-F",
                "c",
                "-f",
                args.output_file,
                "ssrepi",
            ]
            subprocess.run(cmd, check=True)
    finally:
        record.disconnect_db(conn)

    if record.debug:
        sys.stderr.write("PYTHON: record-export-database.py: Exiting...\n")
