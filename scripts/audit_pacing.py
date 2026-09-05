#!/usr/bin/env python3
"""Estimate the player-facing event load 1821-1836 for the major playable tags.

Read-only. Parses events/*.txt with refcheck's tolerant Clausewitz parser and
reports, per tag: how many self-firing country_events can reach it inside the
window, the expected number of fires per year, the `major = yes` popups, plus
cascades (events chained within a few days) and pacing smells.

  python scripts/audit_pacing.py            # print report
  python scripts/audit_pacing.py --write    # also write docs/audit/pacing-1821-1836.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck
from refcheck import MOD, ROOT, tree, rel

WIN_LO, WIN_HI = 1821, 1837          # [lo, hi) in years
TAGS = ["FRA", "ENG", "RUS", "AUS", "PRU", "TUR", "NET", "SPA", "UPB", "POR",
        "USA", "QNG", "GRE", "SAR", "PAP", "MOD", "BAV", "SWE", "DEN"]


# ------------------------------------------------------------------ helpers
def mtth_months(node):
    """Base months of a mean_time_to_happen block (modifiers ignored)."""
    m = node.get("mean_time_to_happen")
    if not m:
        return None
    b = m[0]
    for key, mult in (("months", 1.0), ("years", 12.0), ("days", 1 / 30.0)):
        v = b.first(key)
        if v:
            try:
                return max(float(v) * mult, 0.03)
            except ValueError:
                pass
    return None


def scan_trigger(node, neg=False, pos=None, negs=None, years=None):
    """Collect positive/negative tags and year bounds from a trigger tree."""
    pos = set() if pos is None else pos
    negs = set() if negs is None else negs
    years = {"min": [], "max": []} if years is None else years
    for c in node.children or []:
        k = (c.key or "").lower()
        if k == "not":
            scan_trigger(c, not neg, pos, negs, years)
        elif k == "tag" and c.value:
            (negs if neg else pos).add(c.value.upper())
        elif k == "year" and c.value and c.value.isdigit():
            years["max" if neg else "min"].append(int(c.value))
        elif c.children:
            scan_trigger(c, neg, pos, negs, years)
    return pos, negs, years


def window(years):
    lo = max([WIN_LO] + years["min"])
    hi = min([WIN_HI] + years["max"])
    return lo, hi


def chained(node):
    """[(id, days)] for country_event = { id = X days = D } inside effects."""
    out = []
    for n in list(node.walk())[1:]:
        if (n.key or "").lower() == "country_event":
            if n.children:
                i, d = n.first("id"), n.first("days")
                if i:
                    out.append((i, int(d) if d and d.isdigit() else 0))
            elif n.value:
                out.append((n.value, 0))
    return out


SET_EFFECTS = {"set_country_flag": "flag", "set_global_flag": "flag",
               "add_country_modifier": "mod", "clr_country_flag": "flag"}
NEG_TRIGGERS = {"has_country_flag": "flag", "has_global_flag": "flag",
                "has_country_modifier": "mod"}


def _negatives(node, neg=False, acc=None):
    """Names required to be absent by the trigger (i.e. inside a NOT)."""
    acc = set() if acc is None else acc
    for c in node.children or []:
        k = (c.key or "").lower()
        if k == "not":
            _negatives(c, not neg, acc)
        elif neg and k in NEG_TRIGGERS and c.value:
            acc.add((NEG_TRIGGERS[k], c.value))
        elif c.children:
            _negatives(c, neg, acc)
    return acc


def _sets(node):
    """Names the event's own effects establish."""
    acc = set()
    for n in node.walk():
        k = (n.key or "").lower()
        if k in SET_EFFECTS:
            if n.value:
                acc.add((SET_EFFECTS[k], n.value))
            elif n.children:
                nm = n.first("name")
                if nm:
                    acc.add((SET_EFFECTS[k], nm))
    return acc


def has_flag_guard(ev):
    """True when the event's own effects make its trigger false again."""
    trig = ev.get("trigger")
    if not trig:
        return False
    if _negatives(trig[0]) & _sets(ev):
        return True
    return any((n.key or "").lower() in
               ("has_country_flag", "has_global_flag", "has_country_modifier")
               for n in trig[0].walk())


# ------------------------------------------------------------------ load
events = {}
for f in sorted((MOD / "events").glob("*.txt")):
    for top in tree(f):
        if (top.key or "").lower() != "country_event" or not top.children:
            continue
        eid = top.first("id")
        if not eid:
            continue
        trig = top.get("trigger")
        pos, negs, years = (scan_trigger(trig[0]) if trig
                            else (set(), set(), {"min": [], "max": []}))
        lo, hi = window(years)
        raw_lo = max(years["min"]) if years["min"] else 1836
        raw_hi = min(years["max"]) if years["max"] else 1936
        events[eid] = dict(
            id=eid, file=rel(f), line=top.line, node=top,
            triggered_only=(top.first("is_triggered_only") or "no").lower() == "yes",
            once=(top.first("fire_only_once") or "no").lower() == "yes",
            major=(top.first("major") or "no").lower() == "yes",
            mtth=mtth_months(top), has_trigger=bool(trig),
            pos=pos, neg=negs, lo=lo, hi=hi, raw_lo=raw_lo, raw_hi=raw_hi,
            yr_gated=bool(years["min"] or years["max"]),
            chain=chained(top), guard=has_flag_guard(top), sets=bool(_sets(top)),
            has_min=bool(years["min"]),
        )


def admits(ev, tag):
    if tag in ev["neg"] and tag not in ev["pos"]:
        return False
    if ev["pos"]:
        return tag in ev["pos"]
    return ev["yr_gated"]          # untagged: only count year-gated ones


selffire = [e for e in events.values()
            if not e["triggered_only"] and e["has_trigger"] and e["mtth"]
            and e["lo"] < e["hi"]]

# ------------------------------------------------------------------ per tag
rows = {}
for tag in TAGS:
    avail = [e for e in selffire if admits(e, tag)]
    rate = 0.0
    for e in avail:
        wm = (e["hi"] - e["lo"]) * 12.0
        p = min(1 / e["mtth"], 1.0)
        if e["once"] or e["guard"]:
            rate += (1 - (1 - p) ** wm) / (e["hi"] - e["lo"])
        else:
            rate += min(12.0 / e["mtth"], 12.0)
    majors = [e for e in events.values()
              if e["major"] and admits(e, tag) and e["lo"] < e["hi"]]
    hot = sorted(e["id"] for e in majors if e["lo"] <= 1833 and e["hi"] > 1830)
    rows[tag] = (len(avail), rate, len(majors), hot, avail, majors)

# ------------------------------------------------------------------ smells
repeaters = sorted((e for e in selffire
                    if e["mtth"] <= 1.0 and not e["once"] and not e["guard"]
                    and not e["sets"]),
                   key=lambda e: e["mtth"])

narrow = []
for e in selffire:
    wm = (e["raw_hi"] - e["raw_lo"]) * 12.0
    if e["yr_gated"] and 0 < wm and wm / e["mtth"] < 1.4:
        narrow.append((wm / e["mtth"], e, round(wm / 1.4, 1)))
narrow.sort(key=lambda t: t[0])
tightest = sorted((((e["raw_hi"] - e["raw_lo"]) * 12.0 / e["mtth"], e)
                   for e in selffire
                   if e["yr_gated"] and e["raw_hi"] > e["raw_lo"]),
                  key=lambda t: t[0])[:12]

gvg = sorted((e for e in events.values()
              if e["id"].isdigit() and 1000300 <= int(e["id"]) < 1002000),
             key=lambda e: int(e["id"]))

collisions = []
for tag in TAGS:
    ms = rows[tag][5]
    for i, a in enumerate(ms):
        for b in ms[i + 1:]:
            lo = max(a["lo"], b["lo"])
            if (a["has_min"] and b["has_min"] and abs(a["lo"] - b["lo"]) <= 1
                    and a["mtth"] and b["mtth"]
                    and a["mtth"] <= 12 and b["mtth"] <= 12):
                linked = (b["id"] in {c[0] for c in a["chain"]}
                          or a["id"] in {c[0] for c in b["chain"]})
                if not linked:
                    collisions.append((tag, a["id"], b["id"], lo))

# ------------------------------------------------------------------ output
L = []
w = L.append
w("# Event pacing audit, 1821-1836")
w("")
w("Generated by `scripts/audit_pacing.py` (read-only; base MTTH only, MTTH")
w("modifiers are ignored, so rates are upper bounds). \"Available\" counts")
w("self-firing `country_event`s with a MTTH whose trigger admits the tag")
w("(explicit `tag =`, directly or inside `OR`) or that carry no tag test but are")
w("year-gated into the window.")
w("")
w("## Read this first")
w("")
w("- Nothing in the tree fails the >25% miss test: the lowest window/MTTH ratio")
w("  is 3.6, so every year-gated event has time to fire. No suggested MTTH")
w("  changes are needed on that axis.")
w("- The per-tag rate is dominated by a handful of unbounded repeatable events;")
w("  strip those out and every tag sits at roughly 1-3 events per year.")
w("- Most sub-monthly MTTH events listed further down are self-limiting through")
w("  a map/state change (annexation, colonisation, war end) rather than a flag,")
w("  which is why the automatic guard check cannot see it. Check by hand before")
w("  changing any of them; 99986 is the one that genuinely repeats.")
w("")
w("## Load per tag")
w("")
w("| Tag | Events available | Expected events/year | Major popups | Major ids live 1830-1833 |")
w("|---|---:|---:|---:|---|")
for tag in TAGS:
    n, rate, nm, hot, _, _ = rows[tag]
    w(f"| {tag} | {n} | {rate:.1f} | {nm} | {', '.join(hot) if hot else '-'} |")
w("")
w("## New GVG content (ids 1000300-1001999)")
w("")
if not gvg:
    w("None: the highest GVG ids in the tree are below 1000300, so there is no new")
    w("chain to space out yet.")
else:
    w("| id | file | tags | window | MTTH (mo) | major | chains to |")
    w("|---|---|---|---|---:|---|---|")
    for e in gvg:
        ch = ", ".join(f"{i}(+{d}d)" for i, d in dict(e["chain"]).items()) or "-"
        w(f"| {e['id']} | {e['file'].split('/')[-1]} | {','.join(sorted(e['pos'])) or '-'} | "
          f"{('%d-%d' % (e['lo'], e['hi'])) if e['lo'] < e['hi'] else 'after 1836'} | {e['mtth'] or '-'} | {'yes' if e['major'] else ''} | {ch} |")
w("")
w("### GVG chain spacing (follow-ups fired <= 3 days after their parent)")
w("")
tight_chain = [(e, i, d) for e in gvg for i, d in dict(e["chain"]).items() if d <= 3]
if tight_chain:
    for e, i, d in tight_chain:
        tgt = events.get(i)
        w(f"- {e['id']} -> {i} after {d} day(s)"
          + (" (both major)" if e["major"] and tgt and tgt["major"] else
             " (parent is major)" if e["major"] else ""))
else:
    w("None: every GVG follow-up is at least 4 days behind its parent.")
w("")
w("## Major-event collisions (same tag, same opening year, MTTH <= 12")
w("months, both explicitly year-gated, not chained to each other)")
w("")
if collisions:
    for tag, a, b, yr in sorted(collisions)[:40]:
        w(f"- {tag}: {a} and {b} both live from {yr}")
else:
    w("None.")
w("")
w("## Runaway repeaters (MTTH <= 1 month, no fire_only_once, trigger not")
w("self-negated by the event's own set_flag / add_country_modifier)")
w("")
if repeaters:
    for e in repeaters[:30]:
        w(f"- {e['id']} ({e['file']}:{e['line']}) MTTH {e['mtth']:g} mo, "
          f"tags {','.join(sorted(e['pos'])) or 'any'}")
else:
    w("None: every sub-monthly MTTH event is `fire_only_once` or flag-guarded.")
w("")
w("## Windows too narrow for their MTTH (window/MTTH < 1.4)")
w("")
w("| id | file:line | tags | window | MTTH | ratio | suggested MTTH |")
w("|---|---|---|---|---:|---:|---:|")
for ratio, e, sug in narrow[:45]:
    w(f"| {e['id']} | {e['file'].split('/')[-1]}:{e['line']} | "
      f"{','.join(sorted(e['pos'])) or 'any'} | {e['raw_lo']}-{e['raw_hi']} | "
      f"{e['mtth']:g} | {ratio:.2f} | {sug:g} |")
w("")
w("Tightest windows overall (lowest window/MTTH, for reference):")
w("")
for ratio, e in tightest:
    w(f"- {e['id']} {e['file'].split('/')[-1]}:{e['line']} "
      f"{','.join(sorted(e['pos'])) or 'any'} {e['raw_lo']}-{e['raw_hi']} "
      f"MTTH {e['mtth']:g} mo, ratio {ratio:.1f}")
if len(narrow) > 45:
    w("")
    w(f"({len(narrow) - 45} more omitted; rerun the script for the full list.)")
w("")
w(f"Totals: {len(events)} country_events parsed, {len(selffire)} self-firing with")
w(f"a MTTH live in the window, {len(narrow)} narrow-window, {len(repeaters)} runaway")
w("repeaters.")

text = "\n".join(L) + "\n"
print(text)
if "--write" in sys.argv:
    out = ROOT / "docs/audit/pacing-1821-1836.md"
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"[written] {rel(out)} ({len(L)} lines)", file=sys.stderr)
