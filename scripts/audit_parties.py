#!/usr/bin/env python3
"""Audit party blocks in CoE_RoI_R/common/countries/*.txt.

Checks ideology names, party-issue groups and options, date sanity, per-year
coverage between 1821 and 1947 (the mod's start and end dates), dead/duplicate
parties, ideology availability, and countries.txt <-> file consistency.

Usage
  python scripts/audit_parties.py   report to stdout, exit 1 if any [high]

The latest snapshot of the output lives in docs/audit/parties.md.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refcheck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "CoE_RoI_R"
COMMON = MOD / "common"
START_YEAR, END_YEAR = 1821, 1947

findings = []  # (severity, path, line, problem, fix)


def add(sev, path, line, problem, fix):
    try:
        rel = Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        rel = str(path)
    findings.append((sev, rel, line, problem, fix))


def parse_date(s):
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", (s or "").strip())
    if not m:
        return None
    y, mo, d = (int(x) for x in m.groups())
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        return None
    return (y, mo, d)


def load_ideologies():
    ideo, dates = set(), {}
    for grp in refcheck.tree(COMMON / "ideologies.txt"):
        for node in grp.children or []:
            if node.key and node.children is not None:
                ideo.add(node.key.lower())
                dt = parse_date(node.first("date"))
                dates[node.key.lower()] = dt[0] if dt else None
    return ideo, dates


def load_party_issues():
    groups = {}
    for node in refcheck.tree(COMMON / "issues.txt"):
        if node.key and node.key.lower() == "party_issues":
            for grp in node.children or []:
                if grp.key and grp.children is not None:
                    groups[grp.key.lower()] = {
                        o.key.lower() for o in grp.children or [] if o.key and o.children is not None
                    }
    return groups


def load_registry():
    """TAG -> countries/<file> from common/countries.txt (skips dynamic tags)."""
    reg = {}
    text = refcheck.read(COMMON / "countries.txt")
    for i, line in enumerate(text.splitlines(), 1):
        line = line.split("#")[0].strip()
        m = re.match(r'^([A-Z0-9]{3})\s*=\s*"([^"]+)"$', line)
        if m and not line.startswith("dynamic"):
            reg[m.group(1)] = (m.group(2), i)
    return reg


def enable_events():
    """ideology -> True if some event can enable it (IdeologyEnabling.txt)."""
    out = set()
    p = MOD / "events" / "IdeologyEnabling.txt"
    if p.exists():
        for m in re.finditer(r"enable_ideology\s*=\s*(\w+)", refcheck.read(p)):
            out.add(m.group(1).lower())
    return out


def party_blocks(path):
    """Yield (line, dict of key -> value, name) for each party block."""
    text = refcheck.read(path)
    lines = text.splitlines()
    for node in refcheck.tree(path):
        if node.key and node.key.lower() == "party" and node.children is not None:
            fields, order = {}, []
            for c in node.children:
                if c.key and c.value is not None:
                    k = c.key.lower()
                    fields[k] = (c.value, c.line)
                    order.append(k)
            yield node.line, fields, lines
    return


def main():
    ideologies, ideo_dates = load_ideologies()
    issue_groups = load_party_issues()
    registry = load_registry()
    enabled_by_event = enable_events()

    files = sorted((COMMON / "countries").glob("*.txt"))
    referenced = {}
    for tag, (rel, line) in registry.items():
        p = COMMON / rel.replace("\\", "/")
        referenced.setdefault(p.resolve(), []).append((tag, line))
        if not p.exists():
            add("high", COMMON / "countries.txt", line,
                f"{tag} points at missing file {rel}",
                "create the file or drop the entry")

    unreferenced = [f for f in files if f.resolve() not in referenced]
    for f in unreferenced:
        add("low", f, 1, "file not referenced by common/countries.txt",
            "add a TAG entry or delete the file")

    stats = dict(files=len(files), parties=0, tags=len(registry))
    missing_groups = 0
    per_ideology = defaultdict(int)

    for f in files:
        parties = list(party_blocks(f))
        stats["parties"] += len(parties)
        tags = referenced.get(f.resolve(), [])
        if not parties and tags and tags[0][0] != "REB":
            add("high", f, 1, f"no party blocks but referenced by {tags[0][0]}",
                "add at least one conservative party covering 1821-1947")
        active = defaultdict(list)   # year -> [ideology]
        names = defaultdict(list)
        for line, fields, _ in parties:
            name = (fields.get("name") or ("?", line))[0]
            names[name].append(line)
            ideo = (fields.get("ideology") or ("", line))[0].lower()
            iline = (fields.get("ideology") or ("", line))[1]
            if ideo not in ideologies:
                add("high", f, iline, f"party '{name}' has unknown ideology '{ideo}'",
                    "use an ideology defined in common/ideologies.txt")
            else:
                per_ideology[ideo] += 1
            sd = parse_date((fields.get("start_date") or ("", 0))[0])
            ed = parse_date((fields.get("end_date") or ("", 0))[0])
            if sd is None or ed is None:
                add("high", f, line, f"party '{name}' has an unparsable start/end date",
                    "use YYYY.M.D for both dates")
            elif sd >= ed:
                add("medium", f, line,
                    f"party '{name}' start_date {sd[0]} >= end_date {ed[0]}",
                    "give the party a non-empty window")
            else:
                if ed[0] < START_YEAR:
                    add("low", f, line,
                        f"party '{name}' window ends {ed[0]}, before the 1821 start",
                        "extend end_date past 1821 or remove the party")
                for y in range(max(sd[0], START_YEAR), min(ed[0], END_YEAR) + 1):
                    active[y].append(ideo)
                first = ideo_dates.get(ideo)
                if first and sd[0] < first and ideo in enabled_by_event:
                    add("low", f, line,
                        f"party '{name}' ({ideo}) starts {sd[0]}, ideology not "
                        f"available before {first}",
                        "informational: the party is inert until the ideology is enabled")
            # issues
            present = set()
            for k, (v, kline) in fields.items():
                if k in ("name", "ideology", "start_date", "end_date"):
                    continue
                if k not in issue_groups:
                    add("high", f, kline, f"party '{name}' sets unknown party issue '{k}'",
                        "use a group from party_issues in common/issues.txt")
                    continue
                present.add(k)
                if v.lower() not in issue_groups[k]:
                    add("high", f, kline,
                        f"party '{name}' sets {k} = {v}, not an option of that group",
                        "use one of: " + ", ".join(sorted(issue_groups[k])))
            for g in issue_groups:
                if g not in present:
                    missing_groups += 1

        for name, ls in names.items():
            if len(ls) > 1:
                add("low", f, ls[1], f"duplicate party name '{name}' ({len(ls)} blocks)",
                    "give each party a unique name key")

        if parties:
            gap = [y for y in range(START_YEAR, END_YEAR + 1) if not active[y]]
            nocons = [y for y in range(START_YEAR, END_YEAR + 1)
                      if active[y] and "conservative" not in active[y]]
            if gap:
                add("high", f, 1,
                    f"no party active in {fmt_years(gap)}",
                    "extend the neighbouring party's window to cover the gap")
            if nocons:
                add("medium", f, 1,
                    f"no conservative party in {fmt_years(nocons)}",
                    "extend or add a conservative party (engine ruling-party fallback)")

    stats["missing_group_settings"] = missing_groups
    stats["unreferenced_files"] = len(unreferenced)
    return stats, per_ideology


def fmt_years(ys):
    out, i = [], 0
    while i < len(ys):
        j = i
        while j + 1 < len(ys) and ys[j + 1] == ys[j] + 1:
            j += 1
        out.append(str(ys[i]) if i == j else f"{ys[i]}-{ys[j]}")
        i = j + 1
    return ", ".join(out)


if __name__ == "__main__":
    stats, per_ideology = main()
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda t: (order[t[0]], t[1], t[2]))
    counts = defaultdict(int)
    for sev, *_ in findings:
        counts[sev] += 1
    for sev, path, line, problem, fix in findings:
        print(f"[{sev}] {path}:{line} - {problem} - {fix}")
    print(f"\n{stats['files']} country files, {stats['tags']} tags, "
          f"{stats['parties']} parties; "
          f"high={counts['high']} medium={counts['medium']} low={counts['low']}")
    sys.exit(1 if counts["high"] else 0)
