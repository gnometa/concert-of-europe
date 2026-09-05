#!/usr/bin/env python
"""Structural audit of CoE_RoI_R/decisions/*.txt.

Read-only. Reuses the tolerant Clausewitz parser in refcheck.py.
refcheck.py already covers missing loc keys, dead event ids and unknown
modifier/cb/culture names -- this script does not repeat those. It looks at
the shape of each decision: guards, effects, repeatability, AI weight,
scope mistakes and date gates relative to the mod's 1821.9.1 start.

Usage
  python scripts/audit_decisions.py            defect report
  python scripts/audit_decisions.py table      one tab-separated row per decision
  python scripts/audit_decisions.py dup        duplicate-purpose candidates only
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck
from refcheck import MOD, rel, tree, all_decisions, script_files

START_YEAR = 1821

TAG_RE = re.compile(r"^[A-Z]{3}$")
# `TUR_893 = { ... }` is a named state scope, not a country
STATE_RE = re.compile(r"^[A-Z]{3}_\d+$")

PROVINCE_SCOPES = {
    "any_owned", "any_owned_province", "random_owned", "any_neighbor_province",
    "random_neighbor_province", "capital_scope", "any_empty_neighbor_province",
    "random_empty_neighbor_province", "any_state", "random_state", "state_scope",
    "all_core", "any_core", "random_core", "any_province", "random_province",
    "any_owned_state", "random_owned_state", "location", "any_neighbor_state",
}
COUNTRY_SCOPES = {
    "any_country", "random_country", "any_neighbor_country", "random_neighbor_country",
    "any_greater_power", "random_greater_power", "any_sphere_member", "random_sphere_member",
    "any_substate", "random_substate", "war_countries", "owner", "controller",
    "country", "overlord", "sphere_owner",
}
POP_SCOPES = {"any_pop", "random_pop", "poor_strata", "middle_strata", "rich_strata"}

COUNTRY_ONLY = {
    "prestige", "badboy", "money", "leadership", "research_points", "war_exhaustion",
    "add_accepted_culture", "government", "civilized", "change_tag", "capital",
    "plurality", "infamy", "add_country_modifier", "release", "inherit", "annex_to",
}
PROVINCE_ONLY = {
    "add_province_modifier", "life_rating", "trade_goods", "change_controller",
    "secede_province",
}

FLAG_SET = {"set_country_flag", "set_global_flag", "set_province_flag"}
FLAG_CLR = {"clr_country_flag", "clr_global_flag", "clr_province_flag"}
FLAG_HAS = {"has_country_flag", "has_global_flag", "has_province_flag"}

ONESHOT_EFFECTS = {
    "change_tag", "change_tag_no_core_switch", "inherit", "annex_to", "civilized",
    "government", "capital", "primary_culture", "release_vassal",
}


def known_tags():
    tags = set()
    for n in tree(MOD / "common" / "countries.txt"):
        if n.key and TAG_RE.match(n.key):
            tags.add(n.key)
    return tags


def hist_tags():
    out = set()
    for f in (MOD / "history" / "countries").glob("*.txt"):
        # history files are keyed by the leading tag; the mod uses
        # "TAG - Name.txt", "TAG- Name.txt" and bare "TAG.txt"
        m = re.match(r"([A-Z]{3})\s*(?:-|\.txt$)", f.name)
        if m:
            out.add(m.group(1))
    return out


def flat(node):
    for c in node.children or []:
        yield from c.walk()


def polar_flags(node, neg=False):
    """yield (flag, positive?) for every has_*_flag under node, tracking NOT depth."""
    for c in node.children or []:
        k = (c.key or "").lower()
        if c.children is not None:
            yield from polar_flags(c, neg ^ (k == "not"))
        elif k in FLAG_HAS and c.value:
            yield c.value, not neg


def collect(node, keys):
    out = []
    for n in flat(node):
        if n.key and n.key.lower() in keys and n.value:
            out.append(n.value)
    return out


def scope_walk(node, scope="country"):
    """yield (node, scope) for every descendant, tracking province/country scope."""
    for c in node.children or []:
        s = scope
        k = (c.key or "").lower()
        if c.children is not None:
            if k in PROVINCE_SCOPES or k.isdigit() or STATE_RE.match(c.key or ""):
                s = "province"
            elif k in COUNTRY_SCOPES or TAG_RE.match(c.key or ""):
                s = "country"
            elif k in POP_SCOPES:
                s = "pop"
        yield c, s
        if c.children is not None:
            yield from scope_walk(c, s)


class Dec:
    def __init__(self, node, f):
        self.node, self.file, self.name, self.line = node, f, node.key, node.line
        self.pot = (node.get("potential") or [None])[0]
        self.allow = (node.get("allow") or [None])[0]
        self.effect = (node.get("effect") or [None])[0]
        self.awd = (node.get("ai_will_do") or [None])[0]

        def blob(n):
            if not n:
                return ""
            return " ".join("%s=%s" % (x.key, x.value)
                            for x in ([n] + list(flat(n))) if x.key and x.value)

        self.pot_txt = blob(self.pot)
        self.allow_txt = blob(self.allow)
        self.eff_txt = blob(self.effect)
        self.guard_txt = self.pot_txt + " " + self.allow_txt
        self.disabled = "always=no" in self.guard_txt.replace(" ", "")
        # a decision the AI cannot see needs no ai_will_do
        self.player_only = "ai=no" in self.pot_txt.replace(" ", "")
        self.flags_checked, self.flags_required = set(), set()
        for n in (self.pot, self.allow):
            if n:
                for fl, pos in polar_flags(n):
                    self.flags_checked.add(fl)
                    if pos:
                        self.flags_required.add(fl)
        self.flags_set = set(collect(self.effect, FLAG_SET)) if self.effect else set()
        self.flags_clr = set(collect(self.effect, FLAG_CLR)) if self.effect else set()
        self.tags = set()
        for n in (self.pot, self.allow, self.effect):
            if not n:
                continue
            for x in [n] + list(flat(n)):
                for v in (x.value, x.key):
                    if v and TAG_RE.match(v) and v not in (
                            "AND", "NOT", "OR", "YES", "THIS", "FROM", "REB", "ALL"):
                        self.tags.add(v)
        self.years = []
        for n in (self.pot, self.allow):
            if n:
                for x in flat(n):
                    if x.key and x.key.lower() == "year" and x.value and x.value.isdigit():
                        self.years.append((int(x.value), x.line))
        self.awd_factor = None
        if self.awd:
            try:
                self.awd_factor = float(self.awd.first("factor"))
            except (TypeError, ValueError):
                self.awd_factor = None
        self.eff_keys = {(n.key or "").lower() for n in flat(self.effect)} if self.effect else set()

    def effect_writes(self):
        """guard tokens ('key=value') that the effect flips, so the decision
        cannot immediately be taken again."""
        toks = set()
        if not self.effect:
            return toks
        for n in flat(self.effect):
            k = (n.key or "").lower()
            v = n.value
            if k in FLAG_SET and v:
                toks.add("has_%s=%s" % (k[4:], v))
            elif k in FLAG_CLR and v:
                # clearing a flag invalidates a positive has_*_flag guard
                toks.add("has_%s=%s" % (k[4:], v))
            elif k in ("tech_school", "political_reform", "social_reform",
                       "economic_reform", "military_reform") and v:
                toks.add("SUB:=%s" % v)
            elif k in ("remove_country_modifier", "remove_province_modifier") and v:
                toks.add("has_%s=%s" % (k[7:], v))
            elif k in ("add_country_modifier", "add_province_modifier") and n.children is not None:
                nm = n.first("name")
                if nm:
                    toks.add("has_%s=%s" % (k[4:], nm))
            elif k in ("government", "capital", "primary_culture", "civilized",
                       "nationalvalue", "religion", "ruling_party_ideology") and v:
                toks.add("%s=%s" % (k, v))
            elif k in ("add_accepted_culture", "remove_accepted_culture") and v:
                toks.update(("accepted_culture=%s" % v, "culture=%s" % v))
            elif k in ("activate_invention", "activate_technology") and v:
                toks.update(("invention=%s" % v, "%s=1" % v))
            elif k in ("release", "create_vassal", "release_vassal", "annex_to",
                       "inherit", "puppet") and v:
                toks.add("__tag__%s" % v)
        return toks

    @property
    def repeatable(self):
        """True when nothing in the effect can stop the guards being true again."""
        if self.disabled or not self.effect:
            return False
        if self.eff_keys & ONESHOT_EFFECTS:
            return False
        guard = self.guard_txt
        for t in self.effect_writes():
            if t.startswith("__tag__"):
                tag = t[7:]
                if tag in guard and ("exists" in guard or "vassal" in guard or "owned_by" in guard):
                    return False
            elif t.startswith("SUB:"):
                if t[4:] in guard:
                    return False
            elif t in guard:
                return False
        if ("secede_province" in self.eff_keys or "add_core" in self.eff_keys or
                "change_controller" in self.eff_keys) and any(
                t in guard for t in ("owns=", "controls=", "empty=", "owned_by=",
                                     "all_core", "is_core=", "province_id=")):
            return False
        # the effect only fires an event; whatever closes the loop lives there
        if self.eff_keys <= {"country_event", "province_event", "id", "days", "limit",
                             "random_owned", "any_owned", "prestige"}:
            return False
        if "war" in self.eff_keys and "war=" in guard:
            return False
        return True


def load():
    return [Dec(n, f) for n, f in all_decisions()
            if n.key.lower() not in refcheck.DECISION_CLAUSES]


AI_NEEDED = re.compile(r"form|unif|west|reform|colon|claim|proclaim|restore|annex|integrat", re.I)


def table(decs):
    print("name\tfile\tline\tpot\tallow\teff\tawd\tawd0\tdisabled\trepeat\tflags_chk\tflags_set\ttags")
    for d in decs:
        print("\t".join([
            d.name, rel(d.file), str(d.line),
            "y" if d.pot else "-", "y" if d.allow else "-",
            "y" if d.effect else "-", "y" if d.awd else "-",
            "y" if d.awd_factor == 0 else "-",
            "y" if d.disabled else "-",
            "y" if d.repeatable else "-",
            ",".join(sorted(d.flags_checked)) or "-",
            ",".join(sorted(d.flags_set)) or "-",
            ",".join(sorted(d.tags)) or "-",
        ]))


def dups(decs):
    out = []
    byname = defaultdict(list)
    for d in decs:
        byname[d.name].append(d)
    for name, group in sorted(byname.items()):
        if len(group) > 1:
            out.append(("EXACT", name, [(rel(x.file), x.line) for x in group]))
    sig = defaultdict(list)
    for d in decs:
        if d.disabled:
            continue
        key_effects = tuple(sorted(d.eff_keys & {
            "change_tag", "inherit", "annex_to", "add_core", "civilized",
            "government", "add_accepted_culture", "release_vassal"}))
        pot_tag = d.pot.first("tag") if d.pot else None
        if pot_tag and key_effects:
            sig[(pot_tag, key_effects)].append(d)
    for (tag, eff), group in sorted(sig.items(), key=lambda x: str(x[0])):
        files = {rel(x.file) for x in group}
        if len(group) > 1 and len(files) > 1 and eff != ("add_core",):
            out.append(("SAMETAG", "%s %s" % (tag, "+".join(eff)),
                        [(rel(x.file), x.line, x.name) for x in group]))
    # nation formation: two decisions that turn you into the same tag
    form = defaultdict(list)
    for d in decs:
        if d.disabled or not d.effect:
            continue
        for n in flat(d.effect):
            if n.key and n.key.lower() in ("change_tag", "change_tag_no_core_switch") and n.value:
                form[n.value].append(d)
    for target, group in sorted(form.items()):
        if len(group) > 1:
            out.append(("FORM", "become %s" % target,
                        [(rel(x.file), x.line, x.name) for x in group]))
    return out


def defects(decs):
    tags = known_tags()
    htags = hist_tags()
    setflags = set()
    for f in list(script_files("events", "decisions", recursive=True)) + \
            list(script_files("inventions", "technologies")) + \
            sorted((MOD / "history").rglob("*.txt")):
        for node in tree(f):
            for n in node.walk():
                if n.key and n.children is None and n.key.lower() in FLAG_SET:
                    setflags.add(n.value)
    P = []

    def add(sev, d, line, problem, fix):
        P.append((sev, "%s:%s -- %s -- %s" % (rel(d.file), line, problem, fix)))

    for d in decs:
        if d.disabled:
            continue
        for fl in sorted(d.flags_required - setflags):
            add("high", d, d.line,
                "decision %s requires flag '%s' that nothing ever sets (can never be taken)" % (d.name, fl),
                "set the flag somewhere, or drop the condition")
        for fl in sorted((d.flags_checked - d.flags_required) - setflags):
            add("low", d, d.line,
                "decision %s NOTs flag '%s' that nothing ever sets (dead condition)" % (d.name, fl),
                "drop the condition")
        for t in sorted(d.tags - tags):
            add("high", d, d.line,
                "decision %s references tag %s which is not in common/countries.txt" % (d.name, t),
                "correct the tag or register it")
        for t in sorted((d.tags & tags) - htags):
            add("medium", d, d.line,
                "decision %s references tag %s which has no history/countries file" % (d.name, t),
                "add a history file or drop the reference")
        if not d.effect:
            add("medium", d, d.line, "decision %s has no effect block" % d.name,
                "add one or delete the decision")
        if not d.pot:
            add("medium", d, d.line, "decision %s has no potential block (always listed)" % d.name,
                "add a potential gate")
        if d.repeatable:
            add("medium", d, d.line,
                "decision %s can be taken repeatedly (effect changes nothing its guards test)" % d.name,
                "set a country flag in the effect and NOT it in potential")
        if AI_NEEDED.search(d.name) and not d.player_only:
            if d.awd is None:
                add("medium", d, d.line, "AI-relevant decision %s has no ai_will_do" % d.name,
                    "add ai_will_do = { factor = 1 }")
            elif d.awd_factor == 0:
                add("high", d, d.line,
                    "AI-relevant decision %s has ai_will_do factor = 0 (AI never takes it)" % d.name,
                    "raise the factor or gate it with modifiers")
        if d.effect:
            for n, scope in scope_walk(d.effect):
                k = (n.key or "").lower()
                if scope == "province" and k in COUNTRY_ONLY:
                    add("high", d, n.line, "%s: '%s' used inside a province scope" % (d.name, k),
                        "move it to country scope")
                if scope == "country" and k in PROVINCE_ONLY:
                    add("high", d, n.line, "%s: '%s' used at country scope" % (d.name, k),
                        "wrap it in a province scope")
                if k == "add_core" and n.children is None and n.value and TAG_RE.match(n.value) \
                        and scope == "country":
                    add("high", d, n.line,
                        "%s: add_core = %s at country scope does nothing" % (d.name, n.value),
                        "put it inside any_owned or a province id scope")
        for y, line in d.years:
            if y < START_YEAR:
                add("low", d, line, "%s: year = %d is before the 1821 start (always true)" % (d.name, y),
                    "remove the condition")
            elif 1835 <= y <= 1840:
                add("low", d, line, "%s: year = %d looks like a vanilla 1836-start gate" % (d.name, y),
                    "re-date for the 1821 timeline")
    return P


def main(argv):
    decs = load()
    mode = argv[0] if argv else "report"
    if mode == "table":
        table(decs)
        return 0
    if mode == "dup":
        for kind, what, where in dups(decs):
            print("%s\t%s\t%s" % (kind, what, where))
        return 0
    P = defects(decs)
    print("# %d decisions in %d files (%d disabled, %d repeatable, %d without ai_will_do, "
          "%d with ai_will_do factor 0)" % (
              len(decs), len({d.file for d in decs}),
              sum(1 for d in decs if d.disabled),
              sum(1 for d in decs if d.repeatable),
              sum(1 for d in decs if d.awd is None),
              sum(1 for d in decs if d.awd_factor == 0)))
    for sev in ("high", "medium", "low"):
        rows = [t for s, t in P if s == sev]
        print("\n== [%s] %d" % (sev, len(rows)))
        for r in rows:
            print(r)
    print("\n== duplicates")
    for kind, what, where in dups(decs):
        print("%s\t%s\t%s" % (kind, what, where))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
