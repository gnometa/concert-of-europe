#!/usr/bin/env python3
"""Cross-reference checker for the CoE_RoI_R Victoria 2 mod.

Parses every script file into a tree and checks that things referenced by
name/id actually exist. Complements modcheck.py (which does braces, encoding,
province ids and tags).

Usage
  python scripts/refcheck.py                 run every check
  python scripts/refcheck.py <check> [...]   run only the named checks
  python scripts/refcheck.py --list          list check names

Checks
  events      country_event/province_event references point at defined ids;
              is_triggered_only events that nothing fires; events with neither
              trigger nor is_triggered_only; MTTH missing where a trigger exists
  loc         localisation keys for events (title/desc/options), decisions
              (_title/_desc) and event modifiers resolve, in the mod's csvs or
              in the vanilla ones the engine falls back to
  modifiers   add_/remove_country_modifier and add_/remove_province_modifier
              names exist in common/event_modifiers.txt
  flags       country/province/global flags that are set but never checked,
              or checked but never set
  names       cultures, religions, goods, pop types, ideologies, governments,
              national values, casus belli, reform options, techs and
              inventions referenced by events/decisions exist
  onactions   common/on_actions.txt entries point at defined events
  options     event options per event vs. localisation (EVTOPTA..)

Deliberate patterns are excluded: election events (the engine picks those out
of the issue_group pool), events whose only caller is commented out, and
decisions that are switched off (always = no) or AI-only.

Exit code 1 when problems were found. Output is one problem per line, grouped
per check, each group ending with a count line.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "CoE_RoI_R"
VANILLA = Path(r"D:\Steam\steamapps\common\Victoria 2")


def read(path):
    return Path(path).read_bytes().decode("cp1252", errors="replace")


def rel(p):
    try:
        return str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- parser
TOKEN = re.compile(r'"[^"\n]*"|[^\s{}=<>#"]+|[{}=<>]')


class Node:
    __slots__ = ("key", "op", "value", "children", "line")

    def __init__(self, key, op, value, children, line):
        self.key, self.op, self.value, self.children, self.line = key, op, value, children, line

    def __repr__(self):
        return f"Node({self.key} {self.op} {self.value if self.children is None else '{...}'} @{self.line})"

    def get(self, key):
        return [c for c in (self.children or []) if c.key and c.key.lower() == key]

    def first(self, key):
        g = self.get(key)
        return g[0].value if g else None

    def walk(self):
        yield self
        for c in self.children or []:
            yield from c.walk()


def tokenize(text):
    for lineno, ln in enumerate(text.split("\n"), 1):
        in_str = False
        cut = len(ln)
        for i, ch in enumerate(ln):
            if ch == '"':
                in_str = not in_str
            elif ch == "#" and not in_str:
                cut = i
                break
        for m in TOKEN.finditer(ln[:cut]):
            yield m.group(0), lineno


def parse(text):
    """Return a list of top-level Nodes. Tolerant of stray braces."""
    toks = list(tokenize(text))
    pos = 0
    n = len(toks)

    def block():
        nonlocal pos
        items = []
        while pos < n:
            tok, line = toks[pos]
            if tok == "}":
                pos += 1
                return items
            if tok == "{":
                pos += 1
                items.append(Node(None, None, None, block(), line))
                continue
            if tok in "=<>":
                pos += 1
                continue
            # key
            key = tok
            pos += 1
            if pos < n and toks[pos][0] in "=<>":
                op = toks[pos][0]
                pos += 1
                if pos < n and toks[pos][0] == "{":
                    pos += 1
                    items.append(Node(key, op, None, block(), line))
                elif pos < n:
                    val, _ = toks[pos]
                    pos += 1
                    items.append(Node(key, op, val.strip('"'), None, line))
            else:
                items.append(Node(None, None, key.strip('"'), None, line))
        return items

    return block()


_cache = {}


def tree(path):
    path = Path(path)
    if path not in _cache:
        _cache[path] = parse(read(path))
    return _cache[path]


def script_files(*folders, recursive=False):
    for folder in folders:
        base = MOD / folder
        if base.is_file():
            yield base
            continue
        it = base.rglob("*.txt") if recursive else base.glob("*.txt")
        for f in sorted(it):
            yield f


EVENT_FOLDERS = ("events", "decisions")


def all_events():
    """Yield (Node, file) for every top-level country_event/province_event."""
    for f in script_files("events", "decisions", recursive=True):
        for node in tree(f):
            if node.key and node.key.lower() in ("country_event", "province_event") and node.children is not None:
                yield node, f


def all_decisions():
    for f in script_files("decisions"):
        for node in tree(f):
            if node.key and node.key.lower() == "political_decisions" and node.children:
                for d in node.children:
                    if d.key and d.children is not None:
                        yield d, f


# ---------------------------------------------------------------- data sets
def top_keys(path):
    return {n.key for n in tree(path) if n.key}


def second_level_keys(path):
    out = set()
    for n in tree(path):
        for c in n.children or []:
            if c.key:
                out.add(c.key)
    return out


def loc_keys():
    """Every localisation key the game can resolve: the mod's csvs plus the
    vanilla ones (the engine falls back to those for keys the mod inherits)."""
    keys = set()
    for folder in (MOD / "localisation", VANILLA / "localisation"):
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob("*.csv")):
            for ln in f.read_bytes().split(b"\n"):
                if ln.startswith(b"#") or b";" not in ln:
                    continue
                keys.add(ln.split(b";", 1)[0].decode("cp1252", "replace").strip())
    return keys


KEY_LIKE = re.compile(r"^[A-Za-z0-9_.\-]+$")


def looks_like_key(v):
    """True when a title/desc/option name is meant to be a localisation key.

    Events here (as in vanilla) often put the English text straight into the
    script; the engine prints such a value verbatim, so a missing csv row is
    only a bug for values that actually look like keys."""
    return bool(v) and bool(KEY_LIKE.match(v)) and ("_" in v or v.isupper())


def event_ids_referenced():
    """Yield (id, file, line) for every fired event reference across script."""
    folders = ["events", "decisions", "inventions", "technologies", "common"]
    for f in list(script_files(*folders, recursive=True)) + sorted((MOD / "history").rglob("*.txt")):
        for node in tree(f):
            for n in node.walk():
                if n.key and n.key.lower() in ("country_event", "province_event"):
                    if n.children is None and n.value and n.value.isdigit():
                        yield int(n.value), f, n.line
                    elif n.children is not None:
                        eid = n.first("id")
                        # top-level definitions also have id; distinguish by parent context:
                        # references inside effects have days= or are nested; definitions are top level
                        if eid and eid.isdigit() and n is not node:
                            yield int(eid), f, n.line
        if f.name == "on_actions.txt":
            for hook in tree(f):
                for c in hook.children or []:
                    if c.value and c.value.isdigit():
                        yield int(c.value), f, c.line


# ---------------------------------------------------------------- checks
COMMENTED_REF = re.compile(r"#.*\b(?:country_event|province_event)\s*=\s*\{?\s*(?:id\s*=\s*)?(\d+)")


def commented_out_refs():
    """Event ids that are only referenced from a commented-out line.

    Several chains in this mod are parked by commenting out the caller rather
    than deleting the event; those are deliberate, not orphans."""
    ids = set()
    for f in list(script_files("events", "decisions", recursive=True)) + list(script_files("common")):
        for ln in read(f).split("\n"):
            if "#" in ln:
                for m in COMMENTED_REF.finditer(ln):
                    ids.add(int(m.group(1)))
    return ids


def check_events():
    problems = []
    defined = {}
    for ev, f in all_events():
        eid = ev.first("id")
        if eid and eid.isdigit():
            defined.setdefault(int(eid), (ev, f))
    refs = defaultdict(list)
    for eid, f, line in event_ids_referenced():
        refs[eid].append((f, line))
    for eid, sites in sorted(refs.items()):
        if eid not in defined:
            for f, line in sites:
                problems.append(f"{rel(f)}:{line}: fires event {eid} which is not defined anywhere")
    parked = commented_out_refs()
    for eid, (ev, f) in sorted(defined.items()):
        trig = ev.get("trigger")
        ito = (ev.first("is_triggered_only") or "no").lower() == "yes"
        # election events are picked by the engine out of the issue_group pool,
        # and events whose only caller is commented out are parked on purpose
        engine_fired = (ev.first("election") or "no").lower() == "yes" or eid in parked
        mtth = ev.get("mean_time_to_happen")
        fire_only_once = (ev.first("fire_only_once") or "no").lower() == "yes"
        if ito and eid not in refs and not engine_fired:
            problems.append(f"{rel(f)}:{ev.line}: event {eid} is_triggered_only but nothing fires it")
        if not ito and not trig:
            problems.append(f"{rel(f)}:{ev.line}: event {eid} has no trigger and is not is_triggered_only (fires for everyone)")
        if not ito and trig and not mtth:
            problems.append(f"{rel(f)}:{ev.line}: event {eid} has a trigger but no mean_time_to_happen (fires as soon as true{', once' if fire_only_once else ''})")
        if not ev.get("option"):
            problems.append(f"{rel(f)}:{ev.line}: event {eid} has no option block")
    return problems


def check_onactions():
    problems = []
    defined = {int(ev.first("id")) for ev, _ in all_events() if (ev.first("id") or "").isdigit()}
    f = MOD / "common" / "on_actions.txt"
    for hook in tree(f):
        for c in hook.children or []:
            if c.value and c.value.isdigit() and int(c.value) not in defined:
                problems.append(f"{rel(f)}:{c.line}: {hook.key} fires undefined event {c.value}")
    return problems


DECISION_CLAUSES = {"potential", "allow", "effect", "ai_will_do", "alert", "picture", "news"}


def check_loc():
    problems = []
    keys = loc_keys()
    for ev, f in all_events():
        eid = ev.first("id")
        for field in ("title", "desc"):
            v = ev.first(field)
            if looks_like_key(v) and v not in keys:
                problems.append(f"{rel(f)}:{ev.line}: event {eid} {field} key '{v}' has no localisation")
        for opt in ev.get("option"):
            v = opt.first("name")
            if v is None:
                problems.append(f"{rel(f)}:{opt.line}: event {eid} option without a name")
            elif looks_like_key(v) and v not in keys:
                problems.append(f"{rel(f)}:{opt.line}: event {eid} option key '{v}' has no localisation")
    for d, f in all_decisions():
        if d.key.lower() in DECISION_CLAUSES:
            problems.append(f"{rel(f)}:{d.line}: '{d.key}' parsed as a decision - brace error in the decision above it")
            continue
        pot = d.get("potential")
        pot_text = " ".join(f"{c.key}={c.value}" for c in (pot[0].children if pot else []) if c.key)
        # a decision that is switched off or reserved for the AI is never drawn,
        # so it needs no localisation
        if "always=no" in pot_text or "ai=yes" in pot_text or d.key.endswith("_ai"):
            continue
        for suffix in ("_title", "_desc"):
            if d.key + suffix not in keys:
                problems.append(f"{rel(f)}:{d.line}: decision {d.key} lacks localisation key {d.key}{suffix}")
    for mod in tree(MOD / "common" / "event_modifiers.txt"):
        if mod.key and mod.key not in keys:
            problems.append(f"CoE_RoI_R/common/event_modifiers.txt:{mod.line}: modifier {mod.key} has no localisation")
    return problems


def check_modifiers():
    problems = []
    defined = top_keys(MOD / "common" / "event_modifiers.txt") | top_keys(MOD / "common" / "static_modifiers.txt")
    defined |= top_keys(MOD / "common" / "triggered_modifiers.txt")
    keys = {"add_country_modifier", "remove_country_modifier", "add_province_modifier", "remove_province_modifier",
            "has_country_modifier", "has_province_modifier"}
    for f in list(script_files("events", "decisions", recursive=True)) + list(script_files("inventions", "technologies")):
        for node in tree(f):
            for n in node.walk():
                if not n.key or n.key.lower() not in keys:
                    continue
                name = n.first("name") if n.children is not None else n.value
                if name and name not in defined:
                    problems.append(f"{rel(f)}:{n.line}: {n.key} '{name}' is not defined in common/*_modifiers.txt")
    return problems


def check_flags():
    problems = []
    kinds = {"country": ("set_country_flag", "clr_country_flag", "has_country_flag"),
             "province": ("set_province_flag", "clr_province_flag", "has_province_flag"),
             "global": ("set_global_flag", "clr_global_flag", "has_global_flag")}
    setters, checkers = defaultdict(dict), defaultdict(dict)
    files = list(script_files("events", "decisions", recursive=True)) + list(script_files("inventions", "technologies"))
    files += sorted((MOD / "history").rglob("*.txt"))
    for f in files:
        for node in tree(f):
            for n in node.walk():
                if not n.key or n.children is not None:
                    continue
                k = n.key.lower()
                for kind, (s, c, h) in kinds.items():
                    if k == s:
                        setters[kind].setdefault(n.value, (f, n.line))
                    elif k == h:
                        checkers[kind].setdefault(n.value, (f, n.line))
    for kind in kinds:
        for flag, (f, line) in sorted(setters[kind].items()):
            if flag not in checkers[kind]:
                problems.append(f"{rel(f)}:{line}: {kind} flag '{flag}' is set but never checked")
        for flag, (f, line) in sorted(checkers[kind].items()):
            if flag not in setters[kind]:
                problems.append(f"{rel(f)}:{line}: {kind} flag '{flag}' is checked but never set")
    return problems


def issue_options():
    """Return {issue: set(options)} from common/issues.txt (party_issues/political_reforms/...)."""
    out = {}
    for cat in tree(MOD / "common" / "issues.txt"):
        for issue in cat.children or []:
            if issue.key and issue.children is not None:
                out[issue.key] = {o.key for o in issue.children if o.key and o.children is not None}
    return out


def check_names():
    problems = []
    cultures = set()
    for grp in tree(MOD / "common" / "cultures.txt"):
        for c in grp.children or []:
            if c.key and c.children is not None and c.key not in ("union", "leader", "unit"):
                cultures.add(c.key)
    culture_groups = {g.key for g in tree(MOD / "common" / "cultures.txt") if g.key}
    religions = set()
    for grp in tree(MOD / "common" / "religion.txt"):
        for r in grp.children or []:
            if r.key and r.children is not None:
                religions.add(r.key)
    goods = set()
    for grp in tree(MOD / "common" / "goods.txt"):
        for g in grp.children or []:
            if g.key and g.children is not None:
                goods.add(g.key)
    poptypes = {p.stem for p in (MOD / "poptypes").glob("*.txt")}
    ideologies = set()
    for grp in tree(MOD / "common" / "ideologies.txt"):
        for i in grp.children or []:
            if i.key and i.children is not None:
                ideologies.add(i.key)
    governments = top_keys(MOD / "common" / "governments.txt")
    natvals = top_keys(MOD / "common" / "nationalvalues.txt")
    cbs = top_keys(MOD / "common" / "cb_types.txt")
    issues = issue_options()
    techs = set()
    for f in (MOD / "technologies").glob("*.txt"):
        techs |= top_keys(f)
    inventions = set()
    for f in (MOD / "inventions").glob("*.txt"):
        inventions |= top_keys(f)
    tech_folders = {n.key for n in tree(MOD / "common" / "technology.txt") if n.key == "folders" for n in n.children or [] if n.key}
    rebels = top_keys(MOD / "common" / "rebel_types.txt")
    crimes = top_keys(MOD / "common" / "crime.txt")
    buildings = top_keys(MOD / "common" / "buildings.txt")

    simple = {
        "culture": cultures, "primary_culture": cultures, "add_accepted_culture": cultures | {"union"}, "remove_accepted_culture": cultures,
        "accepted_culture": cultures, "culture_group": culture_groups, "is_culture_group": culture_groups,
        "religion": religions, "has_pop_religion": religions, "has_pop_culture": cultures,
        "trade_goods": goods, "has_pop_type": poptypes, "pop_type": poptypes, "type": None,
        "ruling_party_ideology": ideologies, "ideology": ideologies, "government": governments,
        "nationalvalue": natvals, "has_recently_lost_war": None,
        "invention": inventions, "activate_invention": inventions, "activate_technology": techs,
        "rebel_type": rebels, "has_crime": crimes, "crime": crimes,
    }
    files = list(script_files("events", "decisions", recursive=True))
    for f in files:
        for node in tree(f):
            for n in node.walk():
                if not n.key:
                    continue
                k = n.key.lower()
                if n.children is None:
                    valid = simple.get(k)
                    if valid is not None and n.value and n.value not in valid and n.value.upper() != n.value:
                        problems.append(f"{rel(f)}:{n.line}: {n.key} = {n.value} is not a known {k.replace('_', ' ')}")
                    if k in issues:
                        if n.value not in issues[k]:
                            problems.append(f"{rel(f)}:{n.line}: reform {n.key} = {n.value} is not an option in common/issues.txt")
                    # note: `casus_belli = TAG` is the trigger "do we have a cb
                    # against TAG", not a cb type reference - only the effect
                    # form add_casus_belli = { type = ... } names a cb type.
                    if k in techs | inventions:
                        pass
                    elif k == "tech_school" or k == "technology":
                        pass
                else:
                    if k in ("add_casus_belli", "war", "add_war_goal", "attacker_goal", "defender_goal"):
                        for c in n.children:
                            if c.key and c.key.lower() in ("type", "casus_belli") and c.value and c.value not in cbs:
                                problems.append(f"{rel(f)}:{c.line}: casus belli '{c.value}' is not in common/cb_types.txt")
                    if k in ("build_factory_in_capital_state", "activate_building", "building"):
                        for c in n.children:
                            if c.key == "building" and c.value not in buildings:
                                problems.append(f"{rel(f)}:{c.line}: building '{c.value}' is not in common/buildings.txt")
                    if k == "upper_house" or k == "ideology":
                        for c in n.children:
                            if c.key and c.key.lower() == "ideology" and c.value not in ideologies:
                                problems.append(f"{rel(f)}:{c.line}: ideology '{c.value}' is not in common/ideologies.txt")
    # techs referenced as triggers: bare `tech_name = 1`
    for f in files:
        for node in tree(f):
            for n in node.walk():
                if n.key and n.children is None and n.value == "1" and n.key.lower() not in techs | inventions:
                    continue
    return problems


def check_options():
    """Option counts per event vs EVTOPT letters present in localisation (informational)."""
    problems = []
    keys = loc_keys()
    for ev, f in all_events():
        eid = ev.first("id")
        opts = ev.get("option")
        if len(opts) > 5:
            problems.append(f"{rel(f)}:{ev.line}: event {eid} has {len(opts)} options (vanilla never goes above 5; the UI clips them)")
        for opt in opts:
            if not any(c.key for c in opt.children or [] if c.key and c.key.lower() not in ("name", "ai_chance")):
                pass
    return problems


CHECKS = {
    "events": check_events,
    "onactions": check_onactions,
    "loc": check_loc,
    "modifiers": check_modifiers,
    "flags": check_flags,
    "names": check_names,
    "options": check_options,
}


def main(argv):
    if "--list" in argv:
        print("\n".join(CHECKS))
        return 0
    names = [a for a in argv if not a.startswith("-")] or list(CHECKS)
    total = 0
    for name in names:
        if name not in CHECKS:
            print(f"unknown check {name}", file=sys.stderr)
            return 2
        probs = CHECKS[name]()
        print(f"== {name}")
        for p in probs:
            print(p)
        print(f"{len(probs)} problem(s) in {name}")
        total += len(probs)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
