#!/usr/bin/env python3
"""Audit country_events with fire_only_once = yes whose trigger admits more
than one country.  `fire_only_once` is engine-wide (once per game, any
country), so such an event fires for exactly one country ever.

Classes:
  A  trigger has an OR of tag = tests
  B  trigger has culture / culture_group / continent / GP / civilized tests
  C  no country-identifying trigger (probably a genuine world event)

Usage: python scripts/audit_fire_once.py [--csv]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck as rc

CULT = {"primary_culture", "culture", "accepted_culture", "has_pop_culture"}
GROUP = {"culture_group"}
GEO = {"continent", "region"}
GP = {"is_greater_power", "civilized", "is_secondary_power", "is_vassal",
      "government", "capital"}


def loc_map():
    m = {}
    for f in sorted((rc.MOD / "localisation").glob("*.csv")):
        for ln in rc.read(f).split("\n"):
            if ";" in ln:
                k, _, rest = ln.partition(";")
                m.setdefault(k.strip(), rest.split(";")[0])
    return m


def flags_set(ev):
    out = set()
    for o in ev.get("option"):
        for n in o.walk():
            if n.key and n.key.lower() == "set_country_flag":
                out.add(n.value)
    return out


def flags_notted(trig):
    out = set()
    for n in trig.walk():
        if n.key and n.key.lower() == "not":
            for c in n.children or []:
                if c.key and c.key.lower() == "has_country_flag":
                    out.add(c.value)
    return out


def analyse(trig):
    """Return (has_bare_tag, or_tag_sets, hits).

    A bare `owns = <province>` counts as identifying: only one country can own
    a given province, so the event is effectively single-country.
    """
    bare = False
    or_tags = []
    hits = []

    SCOPES = ("any_country", "all_country", "any_owned_province", "any_pop",
              "any_neighbor_country", "any_greater_power", "any_sphere_member",
              "any_substate", "war_countries", "all_core", "any_state",
              "any_core", "capital_scope", "overlord", "sphere_owner", "THIS",
              "FROM", "owner", "controller", "location", "country")

    def rec(node, in_or, in_not, in_scope):
        nonlocal bare
        for c in node.children or []:
            k = (c.key or "").lower()
            if k in ("tag", "owns", "owns_state", "controls") and not in_or and not in_not and not in_scope:
                bare = True
            elif k == "or" and c.children:
                t = [d.value for d in c.children if (d.key or "").lower() == "tag"]
                if t and not in_scope and not in_not:
                    or_tags.append(t)
                rec(c, True, in_not, in_scope)
            elif k in ("not", "and", "nor"):
                rec(c, in_or, in_not or k in ("not", "nor"), in_scope)
            elif c.children:
                rec(c, in_or, in_not, in_scope or k in SCOPES or len(k) == 3)
            else:
                if (k in CULT or k in GROUP or k in GEO or k in GP) and not in_scope:
                    hits.append(f"{k}={c.value}")
    rec(trig, False, False, False)
    return bare, or_tags, hits


def main():
    loc = loc_map()
    rows = []
    for f in rc.script_files("events"):
        for ev in rc.tree(f):
            if (ev.key or "").lower() != "country_event":
                continue
            if not ev.get("fire_only_once"):
                continue
            if (ev.first("is_triggered_only") or "no").lower() == "yes":
                continue
            trigs = ev.get("trigger")
            eid = ev.first("id")
            if not trigs:
                rows.append((rc.rel(f), ev.line, eid, "C", "(no trigger)", "", ""))
                continue
            bare, or_tags, hits = analyse(trigs[0])
            if bare:
                continue
            if or_tags:
                cls, what = "A", " | ".join("OR(" + ",".join(t) + ")" for t in or_tags)
            elif hits:
                cls, what = "B", ", ".join(sorted(set(hits))[:6])
            else:
                cls, what = "C", "(no country test)"
            sets = flags_set(ev)
            notted = flags_notted(trigs[0])
            guard = "GUARDED" if sets & notted else ("sets:" + ",".join(sorted(sets)) if sets else "")
            rows.append((rc.rel(f), ev.line, eid, cls, what, guard,
                         loc.get("EVTNAME" + str(eid), "")))
    for r in sorted(rows, key=lambda r: (r[3], r[0], r[1])):
        print("\t".join(str(x) for x in r))
    from collections import Counter
    c = Counter(r[3] for r in rows)
    print("# counts", dict(sorted(c.items())), "total", len(rows), file=sys.stderr)


if __name__ == "__main__":
    main()
