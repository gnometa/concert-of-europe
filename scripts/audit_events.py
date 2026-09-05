#!/usr/bin/env python
"""Structural audit of CoE_RoI_R/events/ (files starting with a digit, + or A-G).

Read-only. Reuses the tolerant Clausewitz parser in refcheck.py.
refcheck.py already covers dead event ids, missing loc keys, undefined
modifiers/flags, orphan events and unknown culture/religion/goods/cb/reform
names -- this script does not repeat those.  It looks at script vocabulary and
logic: unknown keywords, date gates that are dead or assume the vanilla 1836
start, repeatable permanent effects, contradictory triggers, scope mistakes,
dead ai_chance weights and impossible MTTHs.

Usage
  python scripts/audit_events.py            defect report
  python scripts/audit_events.py vocab      unknown keywords with counts only
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck
from refcheck import MOD, VANILLA, ROOT, rel, tree, read, parse

START_YEAR = 1821
VANILLA_START = 1836

TAG_RE = re.compile(r"^[A-Z][A-Z0-9]{2}$")
STATE_RE = re.compile(r"^[A-Z][A-Z0-9]{2}_\d+$")
SPECIAL = {"THIS", "FROM", "this", "from", "OR", "AND", "NOT", "NAND", "NOR", "hidden_tooltip"}

PROVINCE_SCOPES = {
    "any_owned", "any_owned_province", "random_owned", "any_neighbor_province",
    "random_neighbor_province", "capital_scope", "any_empty_neighbor_province",
    "random_empty_neighbor_province", "any_state", "random_state", "state_scope",
    "all_core", "any_core", "random_core", "any_province", "random_province",
    "any_owned_state", "random_owned_state", "location", "any_neighbor_state",
    "random_neighbor_owned_province",
}
COUNTRY_SCOPES = {
    "any_country", "random_country", "any_neighbor_country", "random_neighbor_country",
    "any_greater_power", "random_greater_power", "any_sphere_member", "random_sphere_member",
    "any_substate", "random_substate", "war_countries", "owner", "controller",
    "country", "overlord", "sphere_owner", "cultural_union", "crisis_state",
}
POP_SCOPES = {"any_pop", "random_pop", "poor_strata", "middle_strata", "rich_strata"}

# effects that stack for ever if the event repeats
PERMANENT = {
    "add_core", "add_country_modifier", "add_province_modifier", "add_accepted_culture",
}
# trigger keys that show the author thought about repetition
GUARDS = {
    "has_country_flag", "has_global_flag", "has_province_flag", "has_country_modifier",
    "has_province_modifier", "is_core", "has_pop_culture", "accepted_culture",
    "is_accepted_culture", "has_leader", "owns", "empty", "owned_by",
    "controlled_by", "is_colonial", "is_our_vassal", "vassal_of",
}

WORD = re.compile(r"\b([a-z][a-z0-9_]{2,})\s*=")


def wiki_words():
    out = set()
    for name in ("list-of-conditions.md", "list-of-effects.md", "list-of-scopes.md",
                 "event-modding.md", "modifier-effects.md", "decision.md", "event.md",
                 "how-to-make-an-event.md", "how-to-make-a-decision.md"):
        p = ROOT / "docs" / "wiki" / name
        if p.is_file():
            txt = p.read_text(encoding="utf-8", errors="replace")
            out |= set(WORD.findall(txt))
            for m in re.finditer(r"^\s*[-*|]\s*\*?([a-z][a-z0-9_]{2,})\b", txt, re.M):
                out.add(m.group(1))
    return out


def vanilla_words():
    """Every key vanilla's own events and decisions use."""
    out = set()
    for folder in ("events", "decisions"):
        base = VANILLA / folder
        if not base.is_dir():
            return out
        for f in sorted(base.rglob("*.txt")):
            try:
                for node in parse(read(f)):
                    for n in node.walk():
                        if n.key:
                            out.add(n.key.lower())
            except Exception:
                pass
    return out


def script_names():
    """Names that are themselves legal keys in a trigger/effect: technologies,
    inventions, reform/issue options, ideologies, pop types, buildings, goods,
    rebel types, crimes.  refcheck already checks that these resolve."""
    out = set()
    for folder in ("technologies", "inventions"):
        for f in (MOD / folder).glob("*.txt"):
            out |= {n.key for n in tree(f) if n.key}
    for name in ("issues.txt", "ideologies.txt", "rebel_types.txt", "crime.txt",
                 "buildings.txt", "goods.txt", "cb_types.txt", "governments.txt"):
        p = MOD / "common" / name
        if not p.is_file():
            continue
        for grp in tree(p):
            if grp.key:
                out.add(grp.key)
            for c in grp.children or []:
                if c.key:
                    out.add(c.key)
                for g in c.children or []:
                    if g.key:
                        out.add(g.key)
    out |= {p.stem for p in (MOD / "poptypes").glob("*.txt")}
    return {n.lower() for n in out if n}


VOCAB = None


def vocab():
    global VOCAB
    if VOCAB is None:
        VOCAB = {w.lower() for w in wiki_words()} | vanilla_words() | script_names() | {
            "is_triggered_only", "fire_only_once", "allow_multiple_instances",
            "major", "news", "news_title", "news_desc_long", "news_desc_medium",
            "news_desc_short", "election", "issue_group", "picture", "title",
            "desc", "option", "name", "trigger", "effect", "limit", "factor",
            "modifier", "months", "years", "days", "ai_chance", "mean_time_to_happen",
            "id", "war", "attacker_goal", "defender_goal", "casus_belli", "call_ally",
        }
    return VOCAB


def in_range(path):
    if path.parent.name.lower() == "dim":
        return True
    return bool(re.match(r"^[0-9+A-Ga-g]", path.name))


def event_files():
    for f in sorted((MOD / "events").rglob("*.txt")):
        if in_range(f):
            yield f


class Ev:
    def __init__(self, node, f):
        self.node, self.file = node, f
        self.kind = node.key.lower()
        self.id = node.first("id")
        self.line = node.line
        self.trig = node.get("trigger")
        self.mtth = node.get("mean_time_to_happen")
        self.opts = node.get("option")
        self.once = (node.first("fire_only_once") or "no") == "yes"
        self.tonly = (node.first("is_triggered_only") or "no") == "yes"


def load():
    evs = []
    for f in event_files():
        for node in tree(f):
            if node.key and node.key.lower() in ("country_event", "province_event") and node.children is not None:
                evs.append(Ev(node, f))
    return evs


def walk_ctx(node, ctx, out):
    for c in node.children or []:
        if c.key is None:
            walk_ctx(c, ctx, out)
            continue
        out.append((c.key, ctx, c.line))
        if c.children is None:
            continue
        kl = c.key.lower()
        if kl in ("limit", "trigger"):
            walk_ctx(c, "trigger", out)
        elif kl == "effect":
            walk_ctx(c, "effect", out)
        elif kl in ("ai_chance", "mean_time_to_happen"):
            walk_ctx(c, "mtth", out)
        elif kl == "modifier":
            walk_ctx(c, "trigger" if ctx == "mtth" else ctx, out)
        else:
            walk_ctx(c, ctx, out)


def keyword_scan(evs):
    hits = defaultdict(list)
    V = vocab()
    for e in evs:
        out = []
        for t in e.trig:
            walk_ctx(t, "trigger", out)
        for m in e.mtth:
            walk_ctx(m, "mtth", out)
        for o in e.opts:
            walk_ctx(o, "effect", out)
        for k, ctx, line in out:
            kl = k.lower()
            if kl in V or k in SPECIAL or TAG_RE.match(k) or STATE_RE.match(k) or k.isdigit():
                continue
            hits[kl].append((rel(e.file), line, ctx))
    return hits


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def date_year(v):
    m = re.match(r"^(\d{3,4})", str(v or ""))
    return int(m.group(1)) if m else None


def check_dates(e, P):
    """Date bounds that are not negated. `NOT = { year = X }` is handled by
    check_early_window; a bare `year = X` is a lower bound."""
    def rec(n, neg, P):
        for c in n.children or []:
            kl = (c.key or "").lower()
            if kl in ("not", "nand"):
                rec(c, not neg, P)
                continue
            if c.children is not None:
                rec(c, neg, P)
                continue
            if neg or kl not in ("year", "start_date", "end_date") or not c.value:
                continue
            y = num(c.value) if kl == "year" else date_year(c.value)
            if y is None:
                continue
            y = int(y)
            if kl == "year" and y < START_YEAR and c.op != "<":
                P.append(("medium", "%s:%d - `year = %d` is below the 1821.9.1 start, so the gate is always true (dead gate)" % (rel(e.file), c.line, y)))
            elif y >= VANILLA_START:
                P.append(("info", "%s:%d - `%s = %s` assumes the 1836 vanilla start; the first %d years of the 1821 game are locked out" % (
                    rel(e.file), c.line, kl, c.value, y - START_YEAR)))
    for t_ in e.trig:
        rec(t_, False, P)


def check_repeat(e, P):
    # only self-firing events can repeat: they need both a trigger and an MTTH
    if e.once or e.tonly or not e.trig or not e.mtth:
        return
    guarded = False
    for t in e.trig:
        for n in t.walk():
            if n.key and n.key.lower() in GUARDS:
                guarded = True
    perm = set()
    for o in e.opts:
        for n in o.walk():
            if not n.key or n.key.lower() not in PERMANENT:
                continue
            kl = n.key.lower()
            if kl.startswith("add_") and kl.endswith("_modifier"):
                # a modifier with a finite duration is meant to be re-applied
                d = num(n.first("duration")) if n.children else None
                if d is not None and d > 0:
                    continue
                perm.add("%s (permanent duration)" % kl)
            else:
                perm.add(kl)
    if perm and not guarded:
        P.append(("high", "%s:%d - event %s can fire again and again (no fire_only_once, no flag/modifier guard in trigger) but grants permanent %s" % (
            rel(e.file), e.line, e.id, ", ".join(sorted(perm)))))


def collect_pairs(node):
    facts, negs = [], []

    def rec(n, neg):
        for c in n.children or []:
            if c.key is None:
                rec(c, neg)
                continue
            kl = c.key.lower()
            if kl in ("or", "nor"):
                continue
            if kl in ("not", "nand"):
                rec(c, not neg)
                continue
            if kl == "and":
                rec(c, neg)
                continue
            if c.children is None and c.value is not None:
                (negs if neg else facts).append((kl, c.value.lower(), c.line))
    rec(node, False)
    return facts, negs


def check_logic(e, P):
    for t in e.trig:
        facts, negs = collect_pairs(t)
        fset = {(k, v) for k, v, _ in facts}
        for k, v, line in negs:
            if (k, v) in fset:
                P.append(("high", "%s:%d - trigger asserts `%s = %s` and its negation at the same level: always false" % (rel(e.file), line, k, v)))
        tags = [(v, line) for k, v, line in facts if k == "tag"]
        if len({v for v, _ in tags}) > 1:
            P.append(("high", "%s:%d - trigger requires two different tags (%s) outside an OR: always false" % (
                rel(e.file), tags[0][1], ", ".join(sorted({v for v, _ in tags})))))
        for n in t.walk():
            if n.key and n.key.lower() in ("not", "nand", "or", "and") and not (n.children or []):
                P.append(("medium", "%s:%d - empty `%s = { }` in trigger (always %s)" % (
                    rel(e.file), n.line, n.key.upper(), "true" if n.key.lower() in ("not", "nand") else "false")))


def check_early_window(e, P):
    """In Victoria 2 a NOT with several statements is a NOR (all must be false),
    so `NOT = { year = 1836 ... }` is a genuine upper bound.  Such an event was
    dead on a 1836 start; at 1821 it is live for the first 15 years, which is
    usually the point but is worth eyeballing because it fires immediately."""
    for t_ in e.trig:
        for n in t_.walk():
            if not n.key or n.key.lower() not in ("not", "nand"):
                continue
            for c in n.children or []:
                if c.key and c.key.lower() == "year" and num(c.value) and int(num(c.value)) <= VANILLA_START:
                    mt = e.mtth[0] if e.mtth else None
                    fast = mt is not None and (num(mt.first("days")) or 99) <= 7
                    P.append(("info", "%s:%d - `NOT = { year = %s }` was dead on a 1836 start; at 1821 it is live%s" % (
                        rel(e.file), c.line, c.value, " and fires within days of the start" if fast else "")))


def check_ai_chance(e, P):
    """An ai_chance factor of 0 on one option is a normal way of steering the AI;
    it is only a defect when every option of the event is weighted 0."""
    weights = []
    for o in e.opts:
        acs = o.get("ai_chance")
        if not acs:
            return
        f = num(acs[0].first("factor"))
        if f is None:
            return
        mods = acs[0].get("modifier")
        if any(num(m.first("factor")) not in (None, 0) for m in mods):
            f = 1
        weights.append(f)
    if len(weights) > 1 and all(w == 0 for w in weights):
        P.append(("medium", "%s:%d - event %s: every option has ai_chance factor 0, so the AI picks the first option by default" % (
            rel(e.file), e.line, e.id)))


def check_mtth(e, P):
    for m in e.mtth:
        base = None
        for k in ("months", "years", "days"):
            v = num(m.first(k))
            if v is not None:
                base = v
        for mod in m.get("modifier"):
            if num(mod.first("factor")) == 0:
                trg = [c for c in mod.children or [] if c.key and c.key.lower() != "factor"]
                if not trg:
                    P.append(("high", "%s:%d - MTTH modifier `factor = 0` with no trigger: the event can never fire" % (rel(e.file), mod.line)))
        if base is not None and base <= 0:
            P.append(("medium", "%s:%d - MTTH base is %s" % (rel(e.file), m.line, base)))


def check_scope(e, P):
    for o in e.opts:
        def rec(n, kind):
            for c in n.children or []:
                if c.key is None:
                    rec(c, kind)
                    continue
                kl = c.key.lower()
                nk = kind
                if kl in PROVINCE_SCOPES or c.key.isdigit():
                    nk = "province"
                elif kl in COUNTRY_SCOPES or TAG_RE.match(c.key):
                    nk = "country"
                elif kl in POP_SCOPES:
                    nk = "pop"
                if kl == "country_event" and kind == "province":
                    P.append(("high", "%s:%d - country_event fired inside a province scope with no owner/country switch" % (rel(e.file), c.line)))
                if kl == "province_event" and kind == "country":
                    P.append(("high", "%s:%d - province_event fired at country scope with no province scope change" % (rel(e.file), c.line)))
                if c.children is not None and kl not in ("country_event", "province_event"):
                    rec(c, nk)
        rec(o, "province" if e.kind == "province_event" else "country")


def defects(evs):
    P = []
    for e in evs:
        check_dates(e, P)
        check_repeat(e, P)
        check_logic(e, P)
        check_ai_chance(e, P)
        check_early_window(e, P)
        check_mtth(e, P)
        check_scope(e, P)
    return P


def main(argv):
    evs = load()
    hits = keyword_scan(evs)
    if argv and argv[0] == "vocab":
        for k, v in sorted(hits.items(), key=lambda kv: -len(kv[1])):
            print("%-40s %4d  %s:%d (%s)" % (k, len(v), v[0][0], v[0][1], v[0][2]))
        return 0
    files = sorted({e.file for e in evs})
    print("# %d events in %d files (%d fire_only_once, %d is_triggered_only, %d with MTTH)" % (
        len(evs), len(files), sum(1 for e in evs if e.once),
        sum(1 for e in evs if e.tonly), sum(1 for e in evs if e.mtth)))
    print("\n== unknown keywords: %d distinct" % len(hits))
    for k, v in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        print("%-40s %4d  %s:%d (%s)" % (k, len(v), v[0][0], v[0][1], v[0][2]))
    P = defects(evs)
    for sev in ("high", "medium", "info"):
        rows = [t for s, t in P if s == sev]
        print("\n== [%s] %d" % (sev, len(rows)))
        for r in rows:
            print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
