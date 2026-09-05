#!/usr/bin/env python3
"""Checks and helpers for the CoE_RoI_R Victoria 2 mod.

Subcommands
  hook-pre                 PreToolUse hook: block Edit/Write on localisation .csv (stdin JSON)
  hook-post                PostToolUse hook: brace/CRLF/encoding/province check on edited file (stdin JSON)
  braces  <file>...        brace balance + CRLF + encoding check for script .txt files
  encoding [path]          report files that are not ASCII/Windows-1252 with CRLF
  ids                      list duplicate event ids (top-level country_event/province_event)
  next-id <lo> <hi>        lowest unused event id in [lo, hi]
  provinces <file>...      verify province ids referenced in files exist in map/definition.csv
  tags <file>...           verify country tags referenced in files exist in common/countries.txt
  loc-find <key>           find a localisation key across all .csv files
  loc-add <csv> <key> <text> [--force]   append a key (Windows-1252, CRLF); refuses text.csv unless --force
  loc-check <csv>          validate a localisation csv (encoding, CRLF, terminator column)

All output is one problem per line; exit code 1 when problems were found, 2 for hook blocks.
"""
import contextlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "CoE_RoI_R"
LOC = MOD / "localisation"
DEFINITION = MOD / "map" / "definition.csv"
COUNTRIES = MOD / "common" / "countries.txt"


def rel(p):
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def read_cp1252(path):
    return Path(path).read_bytes().decode("cp1252", errors="replace")


def strip_comment(line):
    """Remove a # comment, ignoring # inside double quotes."""
    out = []
    in_str = False
    for ch in line:
        if ch == '"':
            in_str = not in_str
        elif ch == "#" and not in_str:
            break
        out.append(ch)
    return "".join(out)


# ---------------------------------------------------------------- encoding
def encoding_issues(path):
    path = Path(path)
    raw = path.read_bytes()
    issues = []
    if b"\n" in raw and raw.count(b"\n") != raw.count(b"\r\n"):
        issues.append("not CRLF (LF or mixed line endings)")
    if b"\x85" in raw and path.suffix.lower() == ".csv":
        issues.append("contains 0x85 (NEL) bytes, which break line splitting in some tools")
    try:
        raw.decode("ascii")
        return issues
    except UnicodeDecodeError:
        pass
    try:
        raw.decode("utf-8")
        if raw.startswith(b"\xef\xbb\xbf"):
            issues.append("UTF-8 with BOM (must be Windows-1252)")
        else:
            issues.append("UTF-8 multi-byte text (must be Windows-1252)")
    except UnicodeDecodeError:
        try:
            raw.decode("cp1252")
        except UnicodeDecodeError as e:
            issues.append(f"invalid Windows-1252 byte 0x{raw[e.start]:02x} at offset {e.start}")
    return issues


def cmd_encoding(root):
    root = Path(root)
    bad = 0
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() not in (".txt", ".csv", ".lua", ".map"):
            continue
        iss = encoding_issues(p)
        if iss:
            bad += 1
            print(f"{rel(p)}: {', '.join(iss)}")
    print(f"{bad} file(s) with encoding/line-ending issues")
    return 1 if bad else 0


# ---------------------------------------------------------------- braces
def brace_check(path):
    """Return a list of problems (encoding, CRLF, brace balance) for a script file."""
    problems = list(encoding_issues(path))
    text = read_cp1252(path)
    depth = 0
    first_neg = None
    for lineno, ln in enumerate(text.split("\n"), 1):
        in_str = False
        for ch in ln:
            if ch == '"':
                in_str = not in_str
            elif in_str:
                continue
            elif ch == "#":
                break
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0 and first_neg is None:
                    first_neg = lineno
    if first_neg is not None:
        problems.append(f"extra '}}' at line {first_neg} closes more blocks than were opened")
    if depth > 0:
        problems.append(f"{depth} unclosed '{{' at end of file")
    return problems


def cmd_braces(files):
    bad = 0
    for f in files:
        for p in brace_check(f):
            print(f"{rel(f)}: {p}")
            bad += 1
    if not bad:
        print(f"{len(files)} file(s) ok")
    return 1 if bad else 0


# ---------------------------------------------------------------- event ids
EVENT_HEAD = re.compile(r"^\s*(country_event|province_event)\s*=\s*\{")


def defined_event_ids():
    """Yield (id, file, line) for every top-level country_event/province_event definition."""
    for folder in ("events", "decisions"):
        for f in sorted((MOD / folder).glob("*.txt")):
            depth = 0
            in_event = False
            for lineno, ln in enumerate(read_cp1252(f).split("\n"), 1):
                code = strip_comment(ln)
                if depth == 0 and EVENT_HEAD.match(code):
                    in_event = True
                if in_event and depth == 1:
                    m = re.match(r"\s*id\s*=\s*(\d+)", code)
                    if m:
                        yield int(m.group(1)), f, lineno
                        in_event = False
                depth += code.count("{") - code.count("}")
                if depth <= 0:
                    depth = 0
                    in_event = False


def cmd_ids():
    seen = {}
    dups = 0
    for eid, f, ln in defined_event_ids():
        if eid in seen:
            dups += 1
            pf, pl = seen[eid]
            print(f"duplicate event id {eid}: {rel(pf)}:{pl} and {rel(f)}:{ln}")
        else:
            seen[eid] = (f, ln)
    print(f"{len(seen)} event ids defined, {dups} duplicate(s)")
    return 1 if dups else 0


def cmd_next_id(lo, hi):
    used = {eid for eid, _, _ in defined_event_ids()}
    for i in range(lo, hi + 1):
        if i not in used:
            print(i)
            return 0
    print(f"no free event id in {lo}-{hi}", file=sys.stderr)
    return 1


# ---------------------------------------------------------------- provinces
PROV_KEYS = r"(?:province_id|owns|controls|capital|state_province_id|change_province_name)"
PROV_REF = re.compile(r"\b" + PROV_KEYS + r"\s*=\s*(\d+)\b|^\s*(\d+)\s*=\s*\{")


def valid_provinces():
    ids = set()
    for ln in read_cp1252(DEFINITION).splitlines()[1:]:
        m = re.match(r"(\d+);", ln)
        if m:
            ids.add(int(m.group(1)))
    return ids


def cmd_provinces(files):
    valid = valid_provinces()
    bad = 0
    for f in files:
        f = Path(f)
        for lineno, ln in enumerate(read_cp1252(f).split("\n"), 1):
            code = strip_comment(ln)
            for m in PROV_REF.finditer(code):
                pid = int(m.group(1) or m.group(2))
                if pid not in valid:
                    bad += 1
                    print(f"{rel(f)}:{lineno}: province {pid} is not in map/definition.csv")
        if f.parent.parent.name == "provinces":
            m = re.match(r"(\d+) - ", f.name)
            if m and int(m.group(1)) not in valid:
                bad += 1
                print(f"{rel(f)}: file-name province {m.group(1)} is not in map/definition.csv")
    print(f"{bad} bad province reference(s)")
    return 1 if bad else 0


# ---------------------------------------------------------------- tags
TAG_KEYS = r"(?:owner|controller|add_core|remove_core|tag|owned_by|controlled_by|exists|country|is_core|from|who|target|change_tag|inherit|annex_to|release|release_vassal|war_with|alliance_with|in_sphere|sphere_owner|vassal_of|is_our_vassal|truce_with|casus_belli|add_casus_belli|add_accepted_culture)"
TAG_REF = re.compile(r"\b" + TAG_KEYS + r"\s*=\s*([A-Z][A-Z0-9]{2})\b")
SPECIAL_TAGS = {"THIS", "FROM", "REB"}


def valid_tags():
    tags = set()
    for ln in read_cp1252(COUNTRIES).splitlines():
        m = re.match(r"\s*([A-Z][A-Z0-9]{2})\s*=", ln)
        if m:
            tags.add(m.group(1))
    return tags


def cmd_tags(files):
    valid = valid_tags() | SPECIAL_TAGS
    bad = 0
    for f in files:
        f = Path(f)
        for lineno, ln in enumerate(read_cp1252(f).split("\n"), 1):
            for m in TAG_REF.finditer(strip_comment(ln)):
                tag = m.group(1)
                if tag not in valid:
                    bad += 1
                    print(f"{rel(f)}:{lineno}: tag {tag} is not registered in common/countries.txt")
    print(f"{bad} unknown tag reference(s)")
    return 1 if bad else 0


# ---------------------------------------------------------------- localisation
def loc_files():
    return sorted(LOC.glob("*.csv"))


def cmd_loc_find(key):
    hits = 0
    pat = re.compile(r"^" + re.escape(key) + r";")
    for f in loc_files():
        for lineno, ln in enumerate(read_cp1252(f).split("\n"), 1):
            if pat.match(ln):
                hits += 1
                print(f"{rel(f)}:{lineno}: {ln.rstrip()[:160]}")
    if not hits:
        print(f"{key}: not found in any localisation csv")
    return 0 if hits else 1


def cmd_loc_add(csv, key, text, force=False):
    csv = Path(csv)
    if not csv.exists() and not csv.is_absolute():
        csv = LOC / csv.name
    if csv.name == "text.csv" and not force:
        print("refusing to edit text.csv (3.7 MB vanilla override); use a mod-specific csv or pass --force", file=sys.stderr)
        return 2
    if ";" in key or ";" in text:
        print("key and text must not contain ';'", file=sys.stderr)
        return 2
    try:
        text.encode("cp1252")
    except UnicodeEncodeError as e:
        print(f"text has a character not representable in Windows-1252: {text[e.start:e.end]!r}", file=sys.stderr)
        return 2
    for f in loc_files():
        if re.search(r"^" + re.escape(key) + r";", read_cp1252(f), re.M):
            print(f"key {key} already exists in {rel(f)}", file=sys.stderr)
            return 2
    raw = csv.read_bytes() if csv.exists() else b""
    if raw and not raw.endswith(b"\n"):
        raw += b"\r\n"
    elif raw.endswith(b"\n") and not raw.endswith(b"\r\n"):
        raw = raw[:-1] + b"\r\n"
    line = ";".join([key, text] + [""] * 12 + ["x"]) + "\r\n"
    csv.write_bytes(raw + line.encode("cp1252"))
    print(f"added {key} to {rel(csv)}")
    return 0


def cmd_loc_check(csv):
    csv = Path(csv)
    problems = list(encoding_issues(csv))
    for lineno, ln in enumerate(read_cp1252(csv).split("\n"), 1):
        s = ln.rstrip("\r")
        if not s or s.startswith("#"):
            continue
        fields = s.split(";")
        if len(fields) < 3:
            problems.append(f"line {lineno}: fewer than 3 columns")
        elif not any(f.rstrip(", ").strip() == "x" for f in fields[2:]):
            problems.append(f"line {lineno}: no 'x' terminator column")
    for p in problems:
        print(f"{rel(csv)}: {p}")
    if not problems:
        print(f"{rel(csv)}: ok")
    return 1 if problems else 0


# ---------------------------------------------------------------- hooks
def hook_file_path():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return None
    fp = (data.get("tool_input") or {}).get("file_path")
    return Path(fp) if fp else None


def capture(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args)
    return buf.getvalue().splitlines()


def cmd_hook_pre():
    fp = hook_file_path()
    if not fp:
        return 0
    p = str(fp).replace("\\", "/").lower()
    if p.endswith(".csv") and "/localisation/" in p:
        print(
            "BLOCKED: localisation .csv files must stay Windows-1252, and Edit/Write would save UTF-8.\n"
            f'Use instead:  python scripts/modcheck.py loc-add {fp.name} KEY "English text"\n'
            "or a Python snippet that reads/writes bytes with encoding cp1252 and CRLF (see the /loc-add skill).",
            file=sys.stderr,
        )
        return 2
    return 0


def cmd_hook_post():
    fp = hook_file_path()
    if not fp or not fp.exists():
        return 0
    p = str(fp).replace("\\", "/")
    if "/CoE_RoI_R/" not in p:
        return 0
    low = p.lower()
    problems = []
    if low.endswith(".txt"):
        problems += brace_check(fp)
        if any(s in p for s in ("/history/provinces/", "/history/countries/", "/events/", "/decisions/")):
            problems += [l for l in capture(cmd_provinces, [fp]) if "definition.csv" in l]
            problems += [l for l in capture(cmd_tags, [fp]) if "countries.txt" in l]
    elif low.endswith(".csv") and "/localisation/" in low:
        problems += [l for l in capture(cmd_loc_check, fp) if not l.endswith(": ok")]
    if problems:
        print(f"modcheck found problems in {rel(fp)}; fix them before moving on:", file=sys.stderr)
        for pr in problems:
            print("  " + pr, file=sys.stderr)
        return 2
    return 0


# ---------------------------------------------------------------- main
def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "hook-pre":
            return cmd_hook_pre()
        if cmd == "hook-post":
            return cmd_hook_post()
        if cmd == "braces":
            return cmd_braces(args)
        if cmd == "encoding":
            return cmd_encoding(args[0] if args else MOD)
        if cmd == "ids":
            return cmd_ids()
        if cmd == "next-id":
            return cmd_next_id(int(args[0]), int(args[1]))
        if cmd == "provinces":
            return cmd_provinces(args)
        if cmd == "tags":
            return cmd_tags(args)
        if cmd == "loc-find":
            return cmd_loc_find(args[0])
        if cmd == "loc-add":
            force = "--force" in args
            args = [a for a in args if a != "--force"]
            return cmd_loc_add(args[0], args[1], args[2], force)
        if cmd == "loc-check":
            return cmd_loc_check(args[0])
    except IndexError:
        print(f"missing argument for {cmd}\n{__doc__}", file=sys.stderr)
        return 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
