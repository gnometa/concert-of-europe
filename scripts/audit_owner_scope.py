#!/usr/bin/env python3
"""Find any_owned / random_owned blocks that can never match.

An effect like

    any_owned = { limit = { province_id = 1209 } ... }

runs in the *current country scope*. When that scope is statically known (the
event's trigger pins it with a single top-level `tag = X`, or the block sits
inside an explicit `TAG = { ... }` scope) and that country owns none of the
provinces the limit names, the whole block is a silent no-op - the engine
reports nothing. The Anglo-Afghan chain shipped three of these (ENG applying
modifiers to AFG-owned Kabul and to HND-core provinces owned by the vassal).

Ownership is read from history/provinces at the 1821.9.1 bookmark, so a hit is
only certain for the start state; the report classifies each case.

Usage: python scripts/audit_owner_scope.py (exit 1 when a high case is found)
Report: docs/audit/owner-scope.md
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck as rc

ROOT = rc.ROOT
MOD = rc.MOD
START = (1821, 9, 1)

TAG_RE = re.compile(r"^[A-Z]{3}$")

# keys whose block runs in some other scope than the enclosing country
SCOPE_CHANGERS = {
    "any_country", "random_country", "all_core", "any_owned", "random_owned",
    "any_pop", "random_pop", "any_state", "random_state", "any_substate",
    "random_substate", "any_neighbor_country", "any_greater_power",
    "any_neighbor_province", "random_neighbor_province", "any_core",
    "random_empty_neighbor_province", "capital_scope", "this", "from",
    "overlord", "sphere_owner", "war_countries", "any_sphere_member",
    "random_sphere_member", "controller", "owner", "location", "country",
    "cultural_union", "crisis_state", "state_scope", "province_event",
    "country_event", "any_war_countries", "any_defender_country",
    "any_attacker_country",
}


def tags():
    out = set()
    for n in rc.tree(MOD / "common" / "countries.txt"):
        if n.key and TAG_RE.match(n.key):
            out.add(n.key)
    return out


COUNTRIES = tags()


# ------------------------------------------------------------ 1821 ownership
def start_state():
    owner, cores = {}, defaultdict(set)
    for f in (MOD / "history" / "provinces").rglob("*.txt"):
        m = re.match(r"(\d+)", f.name)
        if not m:
            continue
        pid = int(m.group(1))
        entries = []
        for n in rc.tree(f):
            if n.key and re.match(r"^\d+\.\d+\.\d+$", n.key) and n.children is not None:
                d = tuple(int(x) for x in n.key.split("."))
                if d <= START:
                    entries.append((d, n.children))
            else:
                entries.append(((0, 0, 0), [n]))
        for _, group in sorted(entries, key=lambda e: e[0]):
            for n in group:
                if not n.key:
                    continue
                k = n.key.lower()
                if k == "owner" and n.value:
                    owner[pid] = n.value
                elif k == "add_core" and n.value:
                    cores[n.value].add(pid)
                elif k == "remove_core" and n.value:
                    cores[n.value].discard(pid)
    return owner, cores


OWNER, CORES = start_state()
OWNED_BY = defaultdict(set)
for _pid, _t in OWNER.items():
    OWNED_BY[_t].add(_pid)


# ------------------------------------------------------------ limit scanning
def limit_refs(node):
    """(province ids, core tags) the limit *requires*.

    Only unconditional conditions count: a `province_id` inside OR (an
    alternative), inside NOT (an exclusion) or inside a nested scope such as
    `owner = { ... }` says nothing about which province the block must match.
    """
    pids, cores = [], []

    def scan_limit(n):
        for d in n.children or []:
            k = (d.key or "").lower()
            if d.children is not None:
                if k in ("and", ""):
                    scan_limit(d)
                continue
            if k == "province_id" and d.value and d.value.isdigit():
                pids.append(int(d.value))
            elif k == "is_core" and d.value and TAG_RE.match(d.value):
                cores.append(d.value)

    for c in node.children or []:
        if c.key and c.key.lower() == "limit" and c.children is not None:
            scan_limit(c)
    return pids, cores


# effects that hand land over, or that only make sense as one branch of a
# conditional release; a block built out of these is deliberately optional
BRANCH_EFFECTS = {
    "release", "release_vassal", "secede_province", "change_tag", "inherit",
    "annex_to", "change_controller", "all_core", "war", "add_core",
    "remove_core", "country_event", "change_region_name",
}


def branchy(node):
    return any(d.key and d.key.lower() in BRANCH_EFFECTS for d in node.walk())


def resequenced(block):
    """The effect gives the scope new land before the any_owned runs."""
    for d in block.walk():
        if d.key and d.key.lower() in ("inherit", "annex_to", "secede_province",
                                       "change_tag", "release", "release_vassal"):
            return True
    return False


def scan(node, scope, hits, holder):
    for c in node.children or []:
        if c.children is None:
            continue
        key = (c.key or "").lower()
        if c.key and TAG_RE.match(c.key) and c.key in COUNTRIES:
            scan(c, c.key, hits, holder)
        elif key in ("any_owned", "random_owned"):
            if scope:
                pids, cores = limit_refs(c)
                if pids and not any(OWNER.get(p) == scope for p in pids):
                    hits.append((c.line, scope, "province", pids, branchy(c), holder))
                if cores and not any(OWNER.get(p) == scope for t in cores for p in CORES.get(t, ())):
                    hits.append((c.line, scope, "core", cores, branchy(c), holder))
            scan(c, None, hits, holder)
        elif key in SCOPE_CHANGERS:
            scan(c, None, hits, holder)
        else:
            scan(c, scope, hits, holder)


def pinned_tag(block, keys):
    for c in block.children or []:
        if c.key and c.key.lower() in keys and c.children is not None:
            found = [d.value for d in c.children if d.key and d.key.lower() == "tag" and d.value]
            if len(found) == 1 and found[0] in COUNTRIES:
                return found[0]
    return None


def requires_ownership(block, pids, cores):
    """The event/decision itself gates on holding the land, so the scope is
    only reached after a conquest/formation that this audit cannot see."""
    for c in block.children or []:
        if not c.key or c.key.lower() not in ("trigger", "potential", "allow"):
            continue
        for d in c.walk():
            if not d.key:
                continue
            k = d.key.lower()
            if k == "owns" and d.value and d.value.isdigit() and int(d.value) in pids:
                return True
            if k in ("any_owned", "all_core", "any_core", "num_of_cities",
                     "is_culture_group", "owns", "owned_by"):
                return True
            if d.key.isdigit():          # `<pid> = { owned_by = THIS }`
                return True
            if k == "is_core" and d.value in cores:
                return True
    return False


def window(block):
    """(latest year the trigger gates on, window is knowable).

    Options are skipped: `year` inside ai_chance says nothing about when the
    event fires. An is_triggered_only event with no year gate inherits its
    caller's window, which this audit does not follow - those are reported low.
    """
    years, triggered_only = [], False
    for c in block.children or []:
        if not c.key:
            continue
        k = c.key.lower()
        if k == "is_triggered_only" and c.value == "yes":
            triggered_only = True
        if k in ("trigger", "potential", "allow") and c.children is not None:
            for d in c.walk():
                if d.key and d.key.lower() == "year" and d.value and d.value.isdigit():
                    years.append(int(d.value))
    if years:
        return max(years), True
    return None, not triggered_only


def collect():
    cases = []
    for ev, f in rc.all_events():
        scope = pinned_tag(ev, {"trigger"})
        hits = []
        for c in ev.children or []:
            if c.key and c.key.lower() in ("option", "immediate") and c.children is not None:
                scan(c, scope, hits, c)
        if hits:
            cases.append((f, ev.first("id"), "event", window(ev), hits, ev))
    for dec, f in rc.all_decisions():
        scope = pinned_tag(dec, {"potential", "allow"})
        hits = []
        for c in dec.children or []:
            if c.key and c.key.lower() == "effect" and c.children is not None:
                scan(c, scope, hits, c)
        if hits:
            cases.append((f, dec.key, "decision", window(dec), hits, dec))
    return cases


def describe(kind, refs):
    if kind == "province":
        return ", ".join("%d (owned by %s)" % (p, OWNER.get(p, "nobody")) for p in refs)
    return ", ".join("core %s (owner of those: %s)" %
                     (t, ", ".join(sorted({OWNER.get(p, "?") for p in CORES.get(t, ())})) or "none")
                     for t in refs)


def severity(scope, kind, refs, win, block, branch, holder):
    year, known = win
    if branch:
        return "low", "conditional release/secede branch"
    if resequenced(holder):
        return "low", "the effect moves land around before this runs"
    pids = set(refs) if kind == "province" else {p for t in refs for p in CORES.get(t, ())}
    owners = {OWNER.get(p) for p in pids}
    owners.discard(None)
    if not owners:
        return "low", "unowned at start too"
    if not OWNED_BY.get(scope):
        return "low", "%s does not exist at the 1821 start" % scope
    if pids & CORES.get(scope, set()):
        return "low", "%s cores the land" % scope
    cores = set(refs) if kind == "core" else set()
    if requires_ownership(block, pids, cores):
        return "low", "gated on owning it"
    if not known:
        return "low", "window unknown (is_triggered_only)"
    if year is not None and year >= 1850:
        return "low", "late window (year >= %d)" % year
    return "high", "unconditional, early window"


def main():
    cases = collect()
    rows = []
    for f, ident, what, year, hits, block in cases:
        for line, scope, kind, refs, branch, holder in hits:
            sev, why = severity(scope, kind, refs, year, block, branch, holder)
            rows.append((sev, rc.rel(f), line, scope, what, ident, why, kind,
                         describe(kind, refs)))
    rows.sort(key=lambda r: (r[0] != "high", r[1], r[2]))
    high = sum(1 for r in rows if r[0] == "high")
    print("%d unreachable any_owned/random_owned blocks (%d high, %d low)" % (len(rows), high, len(rows) - high))
    for sev, f, line, scope, what, ident, why, kind, desc in rows:
        print("[%s] %s:%d  %s %s scoped to %s -> %s  [%s]" %
              (sev, f, line, what, ident, scope, desc, why))
    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())
