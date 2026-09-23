#!/usr/bin/env python3
import os, sys, json, ijson
from gremlin_python.structure.graph import Graph
from gremlin_python.process.traversal import T
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.serializer import GraphSONSerializersV3d0

HOST = os.environ.get("SSREPI_GREMLIN_HOST", "ws://localhost:8182/gremlin")
JSON = os.environ.get("GRAPH_JSON", "graph.json")
TS   = os.environ.get("TRAVERSAL_SOURCE", "g")

def open_remote(ts):
    conn = DriverRemoteConnection(HOST, ts, message_serializer=GraphSONSerializersV3d0())
    g = Graph().traversal().withRemote(conn)
    return g, conn

def add_vertex(g, v):
    vid   = v.get("T.id"); label = v.get("T.label", "vertex")
    props = {k: v[k] for k in v if k not in ("T.id","T.label")}
    t = g.addV(label).property(T.id, vid)
    for k,val in props.items(): t = t.property(str(k), val)
    t.iterate(); return True

def add_edge(g, e):
    eid = e.get("T.id"); label = e.get("T.label","edge")
    outV = (e.get("Direction.OUT") or {}).get("T.id")
    inV  = (e.get("Direction.IN")  or {}).get("T.id")
    if outV is None or inV is None: raise ValueError(f"Edge {eid} missing OUT/IN ids")
    props = {k: e[k] for k in e if k not in ("T.id","T.label","Direction.OUT","Direction.IN")}
    t = g.V(outV).as_("a").V(inV).as_("b").addE(label).from_("a").to("b").property(T.id, eid)
    for k,val in props.items(): t = t.property(str(k), val)
    t.iterate(); return True

def main():
    if not os.path.exists(JSON): print(f"Missing {JSON}", file=sys.stderr); sys.exit(1)
    g, conn = open_remote(TS)
    try:
        v_ok = v_fail = e_ok = e_fail = 0
        with open(JSON,"rb") as f:
            for v in ijson.items(f, "vertices.item"):
                try:
                    if add_vertex(g, v): v_ok += 1
                    if v_ok % 1000 == 0: print(f"[V] {v_ok} loaded (fail {v_fail})")
                except Exception as ex:
                    v_fail += 1; print(f"[V] FAIL {v.get('T.id')}: {ex}", file=sys.stderr)
        with open(JSON,"rb") as f:
            for e in ijson.items(f, "edges.item"):
                try:
                    if add_edge(g, e): e_ok += 1
                    if e_ok % 1000 == 0: print(f"[E] {e_ok} loaded (fail {e_fail})")
                except Exception as ex:
                    e_fail += 1; print(f"[E] FAIL {e.get('T.id')}: {ex}", file=sys.stderr)
        v_count = g.V().count().next(); e_count = g.E().count().next()
        print("\n=== RESTORE SUMMARY ===")
        print(f"V loaded {v_ok} fail {v_fail}   graph V(): {v_count}")
        print(f"E loaded {e_ok} fail {e_fail}   graph E(): {e_count}")
        if v_fail or e_fail: sys.exit(2)
    finally:
        try: conn.close()
        except: pass

if __name__ == "__main__":
    main()

