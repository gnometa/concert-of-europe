#!/usr/bin/env python3
"""Restore real pop religions in CoE_RoI_R/history/pops/1821.9.1.

The mod's 1821 pop files were mechanically rewritten so that the *religion*
field carries a culture or sub-culture name and the real religion was pushed
into a trailing comment:

    culture = german  #culture = north_german
    religion = north_german #religion = protestant

This tool undoes that transposition:

    culture = north_german
    religion = protestant

Rules (see docs/design/religion-restoration.md):
  culture line -> the commented `#culture = Y` value when present;
                  otherwise, when the religion field holds a known sub-culture
                  that differs from the live culture, that sub-culture;
                  otherwise unchanged.
  religion line -> the commented `#religion = Z` value when present;
                  otherwise a fallback (explicit override, then the modal
                  religion of the same culture in the same file, then the
                  modal religion of the same culture mod-wide).

Default mode is a DRY RUN: it prints the inventory and the pops with no
recoverable religion and touches nothing. Pass --apply to rewrite.

Encoding: files are read and written as cp1252 with newline='' and CRLF line
endings are preserved verbatim. Never use sed on these files.
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "CoE_RoI_R")
POPDIR = os.path.join(MOD, "history", "pops", "1821.9.1")
CULTURES = os.path.join(MOD, "common", "cultures.txt")
RELIGIONS = os.path.join(MOD, "common", "religion.txt")

# Sub-cultures that live in the religion field. Those without a commented
# `#culture =` twin (anglo_canadian, australian, anglo_african) are recovered
# from the religion field itself.
SUBCULTURES = {
    "north_german", "south_german",
    "north_italian", "south_italian",
    "occitan", "picard",
    "yankee", "dixie",
    "anglo_canadian", "australian", "anglo_african",
}

# Pops whose real religion was overwritten by an earlier pass and can no longer
# be read from a comment. Values recovered from git (commit a3a51224).
# key: (filename, live culture) -> religion
EXPLICIT = {
    ("India.txt", "tamil"): "sunni",
    ("Persia Afghanistan Baluchistan.txt", "tabari"): "shiite",
}

CULTURE_RE = re.compile(
    r"^(?P<ind>\s*)culture\s*=\s*(?P<live>\w+)\s*(?:#\s*culture\s*=\s*(?P<com>\w+)\s*)?$")
RELIGION_RE = re.compile(
    r"^(?P<ind>\s*)religion\s*=\s*(?P<live>\w+)\s*(?:#\s*religion\s*=\s*(?P<com>\w+)\s*)?$")


def read_text(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.replace(b"\r\n", b"").find(b"\n") != -1:
        raise SystemExit("ERROR: %s contains bare LF line endings; aborting." % path)
    return raw.decode("cp1252")


def write_text(path, text):
    with open(path, "wb") as fh:
        fh.write(text.encode("cp1252"))


def parse_blocks(path):
    """Return (lines, entries). entry = dict with line indexes and values."""
    lines = read_text(path).split("\r\n")
    entries = []
    pending = None
    for i, line in enumerate(lines):
        m = CULTURE_RE.match(line)
        if m:
            if pending is not None:
                entries.append(dict(pending, rel_i=None, rel_live=None, rel_com=None))
            pending = {"cul_i": i, "cul_ind": m.group("ind"),
                       "cul_live": m.group("live"), "cul_com": m.group("com")}
            continue
        m = RELIGION_RE.match(line)
        if m:
            if pending is None:
                entries.append({"cul_i": None, "cul_ind": None, "cul_live": None,
                                "cul_com": None, "rel_i": i, "rel_ind": m.group("ind"),
                                "rel_live": m.group("live"), "rel_com": m.group("com")})
                continue
            pending.update(rel_i=i, rel_ind=m.group("ind"),
                           rel_live=m.group("live"), rel_com=m.group("com"))
            entries.append(pending)
            pending = None
    if pending is not None:
        entries.append(dict(pending, rel_i=None, rel_live=None, rel_com=None))
    return lines, entries


def parse_defs(path):
    """Top-level group -> members, for cultures.txt / religion.txt."""
    text = "\n".join(l.split("#")[0] for l in read_text(path).splitlines())
    skip = {"leader", "unit", "union", "color", "first_names", "last_names",
            "radicalism", "icon", "pagan"}
    groups, depth, cur = {}, 0, None
    for m in re.finditer(r"([A-Za-z_0-9]+)\s*=\s*\{|\}", text):
        if m.group(0) == "}":
            depth -= 1
            if depth == 0:
                cur = None
        else:
            name = m.group(1)
            if depth == 0:
                cur = name
                groups[name] = []
            elif depth == 1 and cur and name not in skip:
                groups[cur].append(name)
            depth += 1
    return groups


def resolve(entry, fname, by_file_modal, global_modal):
    """Return (new_culture, new_religion, reason)."""
    cul, rel = entry["cul_live"], entry["rel_live"]
    if cul is None or rel is None:
        return cul, rel, "orphan"
    if entry["cul_com"]:
        new_cul = entry["cul_com"]
    elif rel in SUBCULTURES and rel != cul:
        new_cul = rel
    else:
        new_cul = cul
    if entry["rel_com"]:
        return new_cul, entry["rel_com"], "comment"
    key = (fname, cul)
    if key in EXPLICIT:
        return new_cul, EXPLICIT[key], "explicit"
    if by_file_modal.get(key):
        return new_cul, by_file_modal[key], "modal-file"
    if global_modal.get(new_cul):
        return new_cul, global_modal[new_cul], "modal-global"
    return new_cul, None, "unresolved"


REAL_RELIGIONS = frozenset("""catholic protestant mormon orthodox coptic sunni ibadi shiite
druze jewish zoroastrian mahayana gelugpa theravada hindu shinto sikh animist
fetishist""".split())


def _has_transposed_pops():
    """True while the transposition this tool undoes is still in place, i.e. while
    no *live* pop religion line holds a real religion. (Do not test for `#religion`
    comments: the fully-commented dead pop blocks in Russia.txt carry them for
    ever.)"""
    for fname in sorted(f for f in os.listdir(POPDIR) if f.endswith(".txt")):
        for line in read_text(os.path.join(POPDIR, fname)).splitlines():
            m = re.match(r"\s*religion\s*=\s*(\w+)", line.split("#")[0])
            if m and m.group(1) in REAL_RELIGIONS:
                return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="rewrite the pop files (default: dry run)")
    ap.add_argument("--verbose", action="store_true",
                    help="print the per-file breakdown and every fallback pop")
    ap.add_argument("--file", metavar="NAME",
                    help="limit to one pop file (basename)")
    args = ap.parse_args()

    # The restoration was applied on 2026-09-06 (see docs/CHANGELOG.md). Once the
    # pops carry real religions there is nothing left to recover from a `#religion`
    # comment, and re-running the resolver would fall back on the coarse EXPLICIT /
    # modal tables and mangle good data. Refuse rather than pretend.
    if not _has_transposed_pops():
        raise SystemExit(
            "nothing to do: the pop files already carry real religions.\n"
            "This tool is a one-shot migration; it was applied on 2026-09-06.\n"
            "Use 'python scripts/audit_religion.py check' to verify the state instead.")

    names = sorted(f for f in os.listdir(POPDIR) if f.endswith(".txt"))
    if args.file:
        names = [f for f in names if f == args.file]
        if not names:
            raise SystemExit("no such pop file: %s" % args.file)

    parsed = {}
    for fname in names:
        parsed[fname] = parse_blocks(os.path.join(POPDIR, fname))

    # -- pass 1: statistics + modal religion tables -------------------------
    live_rel, com_rel, live_cul, com_cul = Counter(), Counter(), Counter(), Counter()
    per_culture = defaultdict(Counter)          # culture -> religion counts
    per_file_culture = defaultdict(Counter)     # (file, culture) -> religion counts
    orphans = []
    for fname, (_, entries) in parsed.items():
        for e in entries:
            if e["cul_live"] is None or e["rel_live"] is None:
                orphans.append((fname, e))
                continue
            live_cul[e["cul_live"]] += 1
            live_rel[e["rel_live"]] += 1
            if e["cul_com"]:
                com_cul[e["cul_com"]] += 1
            if e["rel_com"]:
                com_rel[e["rel_com"]] += 1
                target = e["cul_com"] or e["cul_live"]
                per_culture[target][e["rel_com"]] += 1
                per_file_culture[(fname, e["cul_live"])][e["rel_com"]] += 1
    global_modal = {c: r.most_common(1)[0][0] for c, r in per_culture.items()}
    by_file_modal = {k: v.most_common(1)[0][0] for k, v in per_file_culture.items()}

    # -- pass 2: resolve every entry ---------------------------------------
    after_cul, after_rel, reasons = Counter(), Counter(), Counter()
    unresolved, fallbacks, changes = [], [], defaultdict(list)
    for fname, (lines, entries) in parsed.items():
        for e in entries:
            new_cul, new_rel, why = resolve(e, fname, by_file_modal, global_modal)
            reasons[why] += 1
            if why == "orphan":
                continue
            after_cul[new_cul] += 1
            if new_rel is None:
                unresolved.append((fname, e))
                continue
            after_rel[new_rel] += 1
            if why != "comment":
                fallbacks.append((fname, e, new_cul, new_rel, why))
            if new_cul != e["cul_live"] or e["cul_com"]:
                changes[fname].append((e["cul_i"], "%sculture = %s" % (e["cul_ind"], new_cul)))
            if new_rel != e["rel_live"] or e["rel_com"]:
                changes[fname].append((e["rel_i"], "%sreligion = %s" % (e["rel_ind"], new_rel)))

    # -- validation ---------------------------------------------------------
    cul_groups = parse_defs(CULTURES)
    rel_groups = parse_defs(RELIGIONS)
    known_cultures = {c for v in cul_groups.values() for c in v}
    known_religions = {r for v in rel_groups.values() for r in v}
    undef_cul = sorted(c for c in after_cul if c not in known_cultures)
    undef_rel = sorted(r for r in after_rel if r not in known_religions)

    # -- report -------------------------------------------------------------
    w = sys.stdout.write
    w("== pop inventory: %s (%d files) ==\n" % (
        os.path.relpath(POPDIR, ROOT).replace("\\", "/"), len(names)))
    w("pop entries                    %6d\n" % sum(live_rel.values()))
    w("with commented #religion       %6d\n" % sum(com_rel.values()))
    w("with commented #culture        %6d\n" % sum(com_cul.values()))
    w("religion field != culture      %6d\n" % sum(
        1 for f, (_, es) in parsed.items() for e in es
        if e["cul_live"] and e["rel_live"] and e["cul_live"] != e["rel_live"]))
    w("orphan culture/religion lines  %6d\n" % len(orphans))
    w("\nrecovery source:\n")
    for k, v in reasons.most_common():
        w("  %-14s %6d\n" % (k, v))

    w("\n== commented real religions (become live) ==\n")
    for k, v in com_rel.most_common():
        w("  %-14s %6d\n" % (k, v))

    w("\n== sub-culture moves (religion field -> culture field) ==\n")
    moves = Counter()
    for fname, (_, entries) in parsed.items():
        for e in entries:
            if e["cul_live"] is None or e["rel_live"] is None:
                continue
            new_cul = e["cul_com"] or (e["rel_live"]
                                       if e["rel_live"] in SUBCULTURES
                                       and e["rel_live"] != e["cul_live"] else e["cul_live"])
            if new_cul != e["cul_live"]:
                moves[(e["cul_live"], new_cul, "comment" if e["cul_com"] else "religion-field")] += 1
    for (old, new, src), v in moves.most_common():
        w("  %-16s -> %-16s %6d  (%s)\n" % (old, new, v, src))

    w("\n== culture population before -> after (changed only) ==\n")
    for c in sorted(set(live_cul) | set(after_cul)):
        if live_cul[c] != after_cul[c]:
            flag = "  <-- EMPTIED" if after_cul[c] == 0 else ""
            w("  %-18s %6d -> %6d%s\n" % (c, live_cul[c], after_cul[c], flag))

    w("\n== validation ==\n")
    w("  cultures used after restore not in common/cultures.txt: %s\n"
      % (", ".join(undef_cul) if undef_cul else "none"))
    w("  religions used after restore not in common/religion.txt: %s\n"
      % (", ".join(undef_rel) if undef_rel else "none"))

    w("\n== pops with no recoverable religion (%d) ==\n" % len(unresolved))
    for fname, e in unresolved:
        w("  %s:%d  culture=%s religion=%s\n"
          % (fname, (e["rel_i"] or 0) + 1, e["cul_live"], e["rel_live"]))

    nonc = [f for f in fallbacks if f[4] != "comment"]
    w("\n== pops restored from a fallback rather than a comment (%d) ==\n" % len(nonc))
    for fname, e, nc, nr, why in (nonc if args.verbose else nonc[:40]):
        w("  %s:%d  %s -> culture=%s religion=%s  [%s]\n"
          % (fname, (e["rel_i"] or 0) + 1, e["cul_live"], nc, nr, why))
    if not args.verbose and len(nonc) > 40:
        w("  ... %d more (use --verbose)\n" % (len(nonc) - 40))

    if args.verbose:
        w("\n== per-file line changes ==\n")
        for fname in names:
            if changes[fname]:
                w("  %-50s %5d lines\n" % (fname, len(changes[fname])))

    total_lines = sum(len(v) for v in changes.values())
    w("\n%d lines in %d files would change.\n"
      % (total_lines, sum(1 for v in changes.values() if v)))

    if not args.apply:
        w("DRY RUN - nothing written. Re-run with --apply to rewrite.\n")
        return 0

    if unresolved:
        w("REFUSING to apply: %d pops have no recoverable religion. "
          "Add them to EXPLICIT first.\n" % len(unresolved))
        return 2
    if undef_cul or undef_rel:
        w("REFUSING to apply: undefined culture/religion values would be written.\n")
        return 2

    for fname in names:
        if not changes[fname]:
            continue
        lines, _ = parsed[fname]
        for idx, newline in changes[fname]:
            lines[idx] = newline
        write_text(os.path.join(POPDIR, fname), "\r\n".join(lines))
        w("wrote %s (%d lines)\n" % (fname, len(changes[fname])))
    w("applied.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
