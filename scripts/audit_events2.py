#!/usr/bin/env python
"""Second-opinion structural audit of CoE_RoI_R events + decisions. Read-only.

Lenses: FROM misuse, province/country scope of effects, random_list weights,
empty options, major spam, news localisation, permanent-vs-temporary modifiers,
change_tag/release targets, per-country use of global flags, province_event
owner triggers without an ownership gate.
"""
import re
import sys
import json
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck
from refcheck import MOD, VANILLA, ROOT, rel, tree, read, parse, loc_keys

TAG = re.compile(r"^[A-Z][A-Z0-9]{2}$")
PROV_SCOPES = {"any_owned", "any_owned_province", "random_owned", "any_neighbor_province",
               "random_neighbor_province", "capital_scope", "any_empty_neighbor_province",
               "random_empty_neighbor_province", "any_state", "random_state", "state_scope",
               "all_core", "any_core", "random_core", "any_province", "random_province",
               "any_owned_state", "random_owned_state", "location", "any_neighbor_state",
               "random_neighbor_owned_province"}
CTY_SCOPES = {"any_country", "random_country", "any_neighbor_country", "random_neighbor_country",
              "any_greater_power", "random_greater_power", "any_sphere_member",
              "random_sphere_member", "any_substate", "random_substate", "war_countries",
              "owner", "controller", "country", "overlord", "sphere_owner", "cultural_union",
              "crisis_state", "THIS", "FROM"}
POP_SCOPES = {"any_pop", "random_pop", "poor_strata", "middle_strata", "rich_strata"}
SCOPE_KEYS = PROV_SCOPES | CTY_SCOPES | POP_SCOPES
CTY_ONLY_EFFECTS = {"add_country_modifier", "prestige", "treasury", "leadership",
                    "badboy", "war_exhaustion", "plurality", "add_tech", "research_points",
                    "set_country_flag", "clr_country_flag", "government", "add_accepted_culture",
                    "political_reform", "social_reform", "end_war", "release", "release_vassal",
                    "change_tag", "change_tag_no_core_switch", "add_casus_belli",
                    "diplomatic_influence", "relation", "capital", "primary_culture",
                    "civilized", "add_war_goal", "war", "annex_to", "inherit", "create_vassal",
                    "nationalvalue", "ruling_party", "add_crisis_interest", "military_reform",
                    "economic_reform", "add_army_leader", "add_navy_leader"}


def scope_change(key):
    if key is None:
        return False
    return key in SCOPE_KEYS or bool(TAG.match(key))


def files():
    for f in sorted((MOD / "events").rglob("*.txt")):
        yield f
    for f in sorted((MOD / "decisions").glob("*.txt")):
        yield f


EVENTS = {}
ALLEV = []
DECS = []
for f in files():
    for node in tree(f):
        k = (node.key or "").lower()
        if k in ("country_event", "province_event") and node.children is not None:
            ALLEV.append((node, f))
            i = node.first("id")
            if i:
                EVENTS.setdefault(i, (node, f, k))
        elif k == "political_decisions" and node.children:
            for d in node.children:
                if d.key and d.children is not None:
                    DECS.append((d, f))


def kids(n):
    return n.children or []


def walk(node, depth, cb, path=()):
    for c in kids(node):
        cb(c, depth, path)
        if c.children is not None:
            d = depth + (1 if scope_change(c.key) else 0)
            walk(c, d, cb, path + ((c.key or ""),))


DEFECTS = []


def add(sev, path, line, prob, fix):
    DEFECTS.append((sev, "%s:%s" % (path, line), prob, fix))


# ---------- fire sites
fires = []
def collect_fires(node, f, cname, ckind):
    def cb(c, depth, path):
        kl = (c.key or "").lower()
        if kl in ("country_event", "province_event"):
            tid = c.value if c.children is None else c.first("id")
            if tid:
                fires.append((tid, depth, f, c.line, ckind, cname, kl))
    walk(node, 0, cb)


for node, f in ALLEV:
    collect_fires(node, f, node.first("id"), "event")
for d, f in DECS:
    collect_fires(d, f, d.key, "decision")

onaction_ids = defaultdict(set)
for grp in tree(MOD / "common" / "on_actions.txt"):
    if grp.key and grp.children:
        for c in kids(grp):
            v = c.value if c.children is None else None
            if v and str(v).isdigit():
                onaction_ids[str(v)].add(grp.key)

# ---------- (a)
FROM_OK = {"on_battle_won", "on_battle_lost", "on_surrender", "on_new_great_nation",
           "on_lost_great_nation", "on_war_end", "on_country_annexed",
           "on_province_change_owner", "on_election_tick"}
uses_from = {}
for i, (node, f, kind) in EVENTS.items():
    cnt = [0]

    def cb(c, depth, path, cnt=cnt):
        if (c.key or "") == "FROM" or (c.value or "") == "FROM":
            cnt[0] += 1
    walk(node, 0, cb)
    if cnt[0]:
        uses_from[i] = (node, f, kind, cnt[0])

fire_by_target = defaultdict(list)
for tid, depth, f, line, ck, cn, kl in fires:
    fire_by_target[tid].append((depth, f, line, ck, cn))

a_self, a_oa = [], []
for i, (node, f, kind, n) in uses_from.items():
    if (node.first("is_triggered_only") or "no") != "yes":
        continue
    callers = fire_by_target.get(i, [])
    for depth, cf, cl, ck, cn in callers:
        if depth == 0:
            a_self.append((i, rel(cf), cl, ck, cn))
    if not callers and i in onaction_ids and not (onaction_ids[i] & FROM_OK):
        a_oa.append((i, rel(f), node.line, sorted(onaction_ids[i])))

for i, cf, cl, ck, cn in a_self:
    add("medium", cf, cl,
        "fires event %s (is_triggered_only, reads FROM) with no scope change, so FROM == THIS" % i,
        "wrap the call in the intended scope (THIS/tag/owner/random_country) or drop FROM in event %s" % i)
for i, f, ln, oas in a_oa:
    add("high", f, ln,
        "event %s reads FROM but is only reachable from on_actions %s, where FROM is undefined" % (i, ",".join(oas)),
        "remove the FROM references or fire the event from a scoped effect")

b_prov = []
for i, (node, f, kind) in EVENTS.items():
    if kind != "province_event":
        continue
    def cb(c, depth, path, i=i, f=f):
        kl = (c.key or "").lower()
        low = [p.lower() for p in path]
        if kl in CTY_ONLY_EFFECTS and depth == 0 and not ({"trigger", "mean_time_to_happen", "ai_chance", "limit"} & set(low)):
            b_prov.append((i, rel(f), c.line, kl))
    walk(node, 0, cb)
for i, f, line, kl in b_prov:
    add("high", f, line, "province_event %s uses country-only effect `%s` in province scope" % (i, kl),
        "wrap it in owner = { ... }")

# ---------- (b)
b_zero = b_single = b_chance = 0
for node, f in ALLEV + DECS:
    def cb(c, depth, path, f=f):
        global b_zero, b_single, b_chance
        kl = (c.key or "").lower()
        if kl == "random_list" and c.children is not None:
            ws = [int(x.key) for x in kids(c) if x.key and re.fullmatch(r"\d+", x.key)]
            if ws and sum(ws) == 0:
                b_zero += 1
                add("high", rel(f), c.line, "random_list weights sum to 0 - no branch can be picked",
                    "give at least one entry a non-zero weight")
            if len(ws) == 1:
                b_single += 1
                add("low", rel(f), c.line, "random_list with a single entry (always taken)",
                    "inline the effect and drop the random_list")
        if kl == "random" and c.children is not None:
            ch = c.first("chance")
            try:
                v = float(ch)
            except (TypeError, ValueError):
                return
            if v <= 0:
                b_chance += 1
                add("high", rel(f), c.line, "random chance = %s - block can never fire" % ch,
                    "raise the chance or delete the block")
            elif v >= 100:
                b_chance += 1
                add("low", rel(f), c.line, "random chance = %s - block always fires" % ch,
                    "drop the random wrapper")
    walk(node, 0, cb)

# ---------- (c)
NON_EFFECT = {"name", "ai_chance"}
empty_opts = 0
empty_ex = []
for i, (node, f, kind) in EVENTS.items():
    for o in node.get("option"):
        real = [c for c in kids(o) if c.key and c.key.lower() not in NON_EFFECT]
        if not real:
            empty_opts += 1
            if len(empty_ex) < 12:
                empty_ex.append((i, rel(f), o.line))

majors = []
for i, (node, f, kind) in EVENTS.items():
    if (node.first("major") or "no") != "yes":
        continue
    if (node.first("is_triggered_only") or "no") == "yes":
        continue
    cnt = sum(1 for t in node.get("trigger") for x in t.walk() if x.key)
    mt = node.get("mean_time_to_happen")
    m = None
    if mt:
        for u in ("days", "months", "years"):
            v = mt[0].first(u)
            if v:
                m = "%s %s" % (v, u)
    majors.append((cnt, i, rel(f), node.line, m))
majors.sort()

# ---------- (d)
LK = loc_keys()
news_missing, news_loc = [], []
for i, (node, f, kind) in EVENTS.items():
    if (node.first("news") or "no") != "yes":
        continue
    for k in ("news_desc_long", "news_desc_medium", "news_desc_short"):
        v = node.first(k)
        if v is None:
            news_missing.append((i, rel(f), node.line, k))
        elif v not in LK:
            news_loc.append((i, rel(f), node.line, k, v))
    t = node.first("news_title")
    if t and t not in LK:
        news_loc.append((i, rel(f), node.line, "news_title", t))

# ---------- (e)
durs = defaultdict(lambda: [0, 0, []])
for node, f in ALLEV + DECS:
    def cb(c, depth, path, f=f):
        kl = (c.key or "").lower()
        if kl in ("add_country_modifier", "add_province_modifier") and c.children is not None:
            nm = c.first("name")
            d = c.first("duration")
            if not nm:
                return
            e = durs[nm]
            if d is not None and str(d).strip().startswith("-"):
                e[0] += 1
            else:
                e[1] += 1
            e[2].append((rel(f), c.line, d))
    walk(node, 0, cb)
mixed = {k: v for k, v in durs.items() if v[0] and v[1]}

# ---------- (f)
reg = {n.key for n in tree(MOD / "common" / "countries.txt") if n.key and TAG.match(n.key)}
hist = {p.name.split(" - ")[0] for p in (MOD / "history" / "countries").glob("*.txt")}
cores = set()
for p in (MOD / "history" / "provinces").rglob("*.txt"):
    for m in re.finditer(r"add_core\s*=\s*([A-Z][A-Z0-9]{2})", read(p)):
        cores.add(m.group(1))
f_tag, f_rel = [], []
for node, f in ALLEV + DECS:
    def cb(c, depth, path, f=f):
        kl = (c.key or "").lower()
        v = c.value
        if not (v and isinstance(v, str) and TAG.match(v)):
            return
        if kl in ("change_tag", "change_tag_no_core_switch") and (v not in reg or v not in hist):
            f_tag.append((rel(f), c.line, kl, v, v in reg, v in hist))
        if kl in ("release", "release_vassal") and (v not in cores or v not in reg):
            f_rel.append((rel(f), c.line, kl, v, v in reg, v in cores))
    walk(node, 0, cb)
for p, l, kl, v, r, h in f_tag:
    add("high", p, l, "%s = %s but tag %s %s" % (kl, v, v,
        "is not registered in common/countries.txt" if not r else "has no history/countries file"),
        "register the tag / add its history file, or point the effect at an existing tag")
for p, l, kl, v, r, c_ in f_rel:
    add("medium", p, l, "%s = %s but tag %s has %s" % (kl, v, v,
        "no cores in history/provinces" if not c_ else "no entry in common/countries.txt"),
        "give the tag cores in province history or remove the release")

# ---------- (g)
gflags = defaultdict(list)
for node, f in ALLEV + DECS:
    def cb(c, depth, path, f=f):
        kl = (c.key or "").lower()
        if kl in ("set_global_flag", "clr_global_flag") and c.value:
            gflags[c.value].append((rel(f), c.line, kl))
    walk(node, 0, cb)
susp = []
for name, uses in sorted(gflags.items()):
    hit = None
    low = name.lower()
    for t in reg:
        if re.search(r"(^|_)" + t.lower() + r"(_|$)", low):
            hit = t
            break
    if hit is None and re.search(r"(^|_)(our|my)(_|$)", low):
        hit = "our/my"
    if hit:
        susp.append((name, hit, uses))

# ---------- (h)
GATES = {"owned", "is_colonial", "exists", "empty", "owned_by", "controlled_by",
         "any_owned_province", "state_scope", "owner_of"}
h_count = 0
h_ex = []
for i, (node, f, kind) in EVENTS.items():
    if kind != "province_event":
        continue
    for t in node.get("trigger"):
        ownr = [x for x in t.walk() if x.key and x.key.lower() == "owner" and x.children is not None]
        if not ownr:
            continue
        keys = {x.key.lower() for x in t.walk() if x.key}
        if not (keys & GATES):
            h_count += 1
            if len(h_ex) < 10:
                h_ex.append((i, rel(f), ownr[0].line))

out = {
    "counts": {
        "events": len(EVENTS), "decisions": len(DECS), "fire_sites": len(fires),
        "a_from_self": len(a_self), "a_from_onaction": len(a_oa),
        "a_prov_country_effect": len(b_prov),
        "b_rl_zero": b_zero, "b_rl_single": b_single, "b_chance": b_chance,
        "c_empty_options": empty_opts, "c_major_untriggered": len(majors),
        "d_news_missing": len(news_missing), "d_news_loc": len(news_loc),
        "e_mixed_duration": len(mixed), "f_change_tag": len(f_tag), "f_release": len(f_rel),
        "g_global_flags": len(gflags), "g_suspect": len(susp), "h_owner_nogate": h_count,
    },
    "empty_ex": empty_ex, "majors": majors[:12], "news_missing": news_missing[:20],
    "news_loc": news_loc[:20],
    "mixed": {k: (v[0], v[1], v[2][:3]) for k, v in list(mixed.items())[:20]},
    "f_tag": f_tag[:20], "f_rel": f_rel[:20],
    "susp": [(n, h, u[:2]) for n, h, u in susp[:20]],
    "h_ex": h_ex, "a_self": a_self[:20], "a_oa": a_oa[:10],
    "prov_effects": b_prov[:20],
    "defects": sorted(DEFECTS, key=lambda d: ({"high": 0, "medium": 1, "low": 2}[d[0]], d[1])),
}
print(json.dumps(out, indent=1, default=str))
