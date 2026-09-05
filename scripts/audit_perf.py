#!/usr/bin/env python3
"""Trigger-cost audit for always-evaluated events in the CoE_RoI_R mod.

Every event without `is_triggered_only = yes` has its `trigger` block evaluated
once per scope per day: once per province for a province_event, once per country
for a country_event.  A `mean_time_to_happen` does not reduce that, it only
scales the roll *after* the trigger has passed (`docs/wiki/event-modding.md`).
The engine evaluates a trigger block top to bottom and short-circuits on the
first failing clause, so the order of the clauses inside `trigger = { }` is what
decides the real daily cost.

Scoring:
  cost(clause)  leaf clauses cost ~1; an iteration scope costs its expected
                iteration count times the cost of its own body
  short-circuit each clause is only paid for when every clause before it passed,
                so a cheap selective gate in front of an expensive scope removes
                most of that scope's cost

Usage
  python scripts/audit_perf.py               top 40 by estimated daily cost
  python scripts/audit_perf.py --top N       show N rows
  python scripts/audit_perf.py --csv         machine-readable, all events
  python scripts/audit_perf.py --file F      only events from files matching F
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck
from refcheck import rel

# Scope counts.  ~2700 land provinces of the 3304 rows in map/definition.csv are
# ever owned; ~200 of the 573 tags in common/countries.txt exist at any one time.
PROVINCES = 2700
COUNTRIES = 200

# Expected iteration count for each scope-opening trigger key.  Anything > 1 is
# "expensive": the engine re-runs the whole body once per member.
SCOPES = {
    "any_country": COUNTRIES,
    "any_existing_country": COUNTRIES,
    "all_country": COUNTRIES,
    "any_defined_country": COUNTRIES,
    "any_pop": 60.0,
    "any_owned_province": 18.0,
    "any_owned": 18.0,
    "all_owned": 18.0,
    "any_core": 20.0,
    "all_core": 20.0,
    "any_state": 6.0,
    "any_substate": 2.0,
    "any_neighbor_province": 4.0,
    "any_neighbor_country": 5.0,
    "any_greater_power": 8.0,
    "any_sphere_member": 6.0,
    "war_countries": 3.0,
    "state_scope": 20.0,       # aggregates every pop in the state
    "any_pop_type": 10.0,
}
# Single-target scope switches: no iteration, but the body still costs.
PASSTHROUGH = {
    "owner", "controller", "location", "capital_scope", "country", "this",
    "from", "overlord", "sphere_owner", "province_scope", "region",
}
BOOLEAN = {"and", "or", "not", "hidden_trigger"}

# Cheap, highly selective gates.  cost = relative price of evaluating the
# clause; pass = rough fraction of scopes that get past it.
CHEAP = {
    "year": (0.2, 0.55), "month": (0.2, 0.5), "end_date": (0.2, 0.9),
    "tag": (0.1, 0.02), "exists": (0.2, 0.9), "civilized": (0.2, 0.5),
    "ai": (0.2, 0.9), "is_greater_power": (0.2, 0.06),
    "has_country_flag": (0.3, 0.15), "has_global_flag": (0.2, 0.3),
    "has_province_flag": (0.3, 0.15),
    "is_vassal": (0.2, 0.2), "is_colonial": (0.2, 0.3),
    "is_culture_group": (0.3, 0.15), "is_core": (0.3, 0.2),
    "province_id": (0.3, 0.02), "continent": (0.3, 0.2),
    "government": (0.3, 0.2), "primary_culture": (0.3, 0.1),
    "religion": (0.3, 0.2), "trade_goods": (0.3, 0.05),
    "has_province_modifier": (0.4, 0.3), "has_country_modifier": (0.4, 0.3),
    "war": (0.2, 0.6), "capital": (0.3, 0.1), "owned_by": (0.3, 0.1),
    "controlled_by": (0.3, 0.1), "is_capital": (0.2, 0.1),
    "revolt_percentage": (0.5, 0.5), "empty": (0.2, 0.3),
    "always": (0.1, 0.5),
}
# Keys that count as a "cheap gate" for the ordering report.
CHEAP_GATE_KEYS = {
    "year", "month", "tag", "exists", "civilized", "has_country_flag",
    "has_global_flag", "has_province_flag", "is_greater_power", "province_id",
    "trade_goods", "continent", "is_colonial", "is_vassal", "capital",
    "owned_by", "controlled_by", "end_date", "ai", "is_capital", "empty",
    "has_province_modifier", "has_country_modifier", "government", "religion",
    "primary_culture", "is_culture_group", "is_core", "war", "always",
}
DEFAULT = (1.0, 0.5)


def clause_cost(node):
    """(cost, pass_probability) for one trigger clause, with short-circuiting."""
    key = (node.key or "").lower()
    if node.children is None:
        return CHEAP.get(key, DEFAULT)
    body_cost, body_pass = block_cost(node.children)
    if key in SCOPES:
        n = SCOPES[key]
        # any_/all_ scopes stop early on the first (non-)match: ~half the
        # members on average, and never fewer than one.
        return max(1.0, n * 0.5) * max(body_cost, 0.5), min(0.9, 0.15 + body_pass)
    if key in PASSTHROUGH:
        return max(body_cost, 0.2), body_pass
    if key == "not":
        return body_cost, 1.0 - body_pass * 0.6
    if key == "or":
        # an OR pays for every branch until one passes
        return body_cost, min(0.95, body_pass * len(node.children or [1]) + 0.1)
    return body_cost, body_pass


def block_cost(children):
    """Top-to-bottom short-circuited cost of a list of clauses."""
    total, reach, p_all = 0.0, 1.0, 1.0
    for ch in children or []:
        c, p = clause_cost(ch)
        total += reach * c
        reach *= p
        p_all *= p
    return total, p_all


def is_expensive(node):
    key = (node.key or "").lower()
    if key in SCOPES:
        return True
    if node.children is not None and key in (PASSTHROUGH | BOOLEAN):
        return any(is_expensive(c) for c in node.children or [])
    return False


def is_cheap_gate(node, depth=0):
    """A leaf gate, or a NOT/OR/AND or single-target scope switch (owner = { tag })
    whose body is made only of cheap gates.  No iteration anywhere inside."""
    key = (node.key or "").lower()
    if node.children is None:
        return key in CHEAP_GATE_KEYS
    if depth > 2 or not node.children:
        return False
    if key in ("not", "or", "and") or key in PASSTHROUGH:
        return all(is_cheap_gate(c, depth + 1) for c in node.children)
    return False


def render(node, depth=0):
    key = node.key or ""
    if node.children is None:
        return f"{key} {node.op or '='} {node.value}".strip()
    if depth >= 1:
        return key + " = { ... }"
    inner = " ".join(render(c, depth + 1) for c in (node.children or [])[:2])
    more = " ..." if len(node.children or []) > 2 else ""
    return key + " = { " + inner + more + " }"


def scan(file_filter=None):
    rows = []
    for ev, f in refcheck.all_events():
        if file_filter and file_filter not in rel(f):
            continue
        if (ev.first("is_triggered_only") or "").lower() == "yes":
            continue
        trig = ev.get("trigger")
        if not trig or not trig[0].children:
            continue
        clauses = trig[0].children
        cost, _ = block_cost(clauses)
        scopes = PROVINCES if ev.key.lower() == "province_event" else COUNTRIES
        first_cheap = next((i for i, c in enumerate(clauses) if is_cheap_gate(c)), None)
        first_exp = next((i for i, c in enumerate(clauses) if is_expensive(c)), None)
        rows.append({
            "id": ev.first("id"), "file": rel(f), "line": ev.line,
            "type": ev.key.lower(), "scopes": scopes,
            "daily": cost * scopes, "trigger_cost": cost,
            "n": len(clauses), "first_cheap": first_cheap, "first_exp": first_exp,
            "head": [render(c) for c in clauses[:3]],
        })
    rows.sort(key=lambda r: -r["daily"])
    return rows


def main(argv):
    top, as_csv, ff = 40, False, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--top":
            i += 1
            top = int(argv[i])
        elif a == "--csv":
            as_csv = True
        elif a == "--file":
            i += 1
            ff = argv[i]
        i += 1
    rows = scan(ff)
    if as_csv:
        print("daily,id,type,file,line,clauses,first_cheap,first_expensive")
        for r in rows:
            print("%.0f,%s,%s,%s,%d,%d,%s,%s" % (
                r["daily"], r["id"], r["type"], r["file"], r["line"],
                r["n"], r["first_cheap"], r["first_exp"]))
        return 0
    total = sum(r["daily"] for r in rows) or 1.0
    print("%d self-firing events; total estimated cost %s clause-evals/day"
          "  (province=%d, country=%d)"
          % (len(rows), format(total, ",.0f"), PROVINCES, COUNTRIES))
    print()
    for n, r in enumerate(rows[:top], 1):
        bad = ""
        if r["first_exp"] is not None and (
                r["first_cheap"] is None or r["first_cheap"] > r["first_exp"]):
            bad = "  <-- expensive clause before any cheap gate"
        print("%3d. %12s  %10s  %-8s %s:%d%s" % (
            n, format(r["daily"], ",.0f"), r["id"], r["type"][:8],
            r["file"], r["line"], bad))
        print("     clauses=%d first_cheap=%s first_expensive=%s"
              % (r["n"], r["first_cheap"], r["first_exp"]))
        for h in r["head"]:
            print("       | " + h[:110])
    sub = sum(r["daily"] for r in rows[:top])
    print()
    print("top %d = %s (%.0f%% of total)"
          % (min(top, len(rows)), format(sub, ",.0f"), 100 * sub / total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
