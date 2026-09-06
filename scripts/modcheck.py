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
  province-paths           every mod history/provinces file must sit at the vanilla path for its id
  decisions                every decisions file is political_decisions = { name = { potential allow effect } }
  desync [file]...         effect-only scopes used as triggers / bare province_event: they eat a brace
  engine-counts            diff the engine's per-file decision and event counts in setup.log against a parse

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
GAME = Path(r"D:\Steam\steamapps\common\Victoria 2")


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
    odd_width = 0
    for lineno, ln in enumerate(read_cp1252(csv).split("\n"), 1):
        s = ln.rstrip("\r")
        if not s or s.startswith("#"):
            continue
        fields = s.split(";")
        if len(fields) < 3:
            problems.append(f"line {lineno}: fewer than 3 columns")
            continue
        if not any(f.rstrip(", ").strip() == "x" for f in fields[2:]):
            problems.append(f"line {lineno}: no 'x' terminator column")
        if len(fields) != 15:
            odd_width += 1
        # A ';' typed inside the English text splits it across the English and
        # French columns. Signature: French filled, every later language empty.
        term = next(
            (i for i, f in enumerate(fields) if i >= 2 and f.rstrip(", ").strip() == "x"),
            len(fields),
        )
        if term > 3 and fields[2].strip() and not any(
            f.strip() for f in fields[3:term]
        ):
            problems.append(
                f"line {lineno}: ';' inside the text splits it across columns [{fields[0]}]"
            )
    if odd_width:
        problems.append(
            f"{odd_width} row(s) do not have exactly 15 columns "
            "(usually harmless trailing/missing empty columns; see validate SKILL.md baseline)"
        )
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
        if "/decisions/" in p:
            problems += [l for l in capture(cmd_decisions) if l.startswith(rel(fp))]
        problems += [l for l in capture(cmd_desync, [fp]) if l.startswith(rel(fp))]
        if "/history/provinces/" in p:
            problems += [l for l in capture(cmd_province_paths) if l.startswith(f"province {fp.name.split(' ')[0]}:")]
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


def cmd_province_paths():
    """Vic2 overrides province history per FILE PATH, not per province id. A mod
    file for id N that is not at the same relative path as vanilla's file for N
    leaves the vanilla file live as well; both apply and the alphabetically later
    one wins (the 2637 Lanfang move crashed the game at Executing History)."""
    van = GAME / "history" / "provinces"
    if not van.is_dir():
        print(f"vanilla history/provinces not found at {van}; skipping")
        return 0

    def index(root):
        d = {}
        for f in root.rglob("*.txt"):
            m = re.match(r"(\d+)", f.name)
            if m:
                d.setdefault(int(m.group(1)), set()).add(f.relative_to(root).as_posix())
        return d

    v = index(van)
    m = index(MOD / "history" / "provinces")
    problems = 0
    for pid in sorted(m):
        if pid in v and not (m[pid] & v[pid]):
            problems += 1
            print(f"province {pid}: mod file {sorted(m[pid])} does not shadow vanilla {sorted(v[pid])}; "
                  f"move it to the vanilla path (name and folder)")
        if len(m[pid]) > 1:
            problems += 1
            print(f"province {pid}: {len(m[pid])} mod files {sorted(m[pid])}")
    print(f"{len(m)} mod province files, {problems} path problem(s)")
    return 1 if problems else 0


def cmd_decisions():
    """Structural check the brace counter cannot do: each decisions file must be
    a single political_decisions block whose children each carry potential,
    allow and effect. A file that lost its wrapper (Mexican Minors.txt, found
    in the 2026-09-06 playtest) makes the engine register `effect`, `NOT`, ...
    as decisions and shows raw effect_title strings to every country."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import refcheck  # noqa: E402
    problems = 0
    ctrl = {"potential", "allow", "effect", "ai_will_do", "not", "or", "and", "limit", "tag", "picture", "news"}
    for f in sorted((MOD / "decisions").glob("*.txt")):
        nodes = [n for n in refcheck.tree(f) if n.key]
        for n in nodes:
            if n.key.lower() != "political_decisions":
                problems += 1
                print(f"{rel(f)}:{n.line}: top-level `{n.key}` is not political_decisions (missing wrapper?)")
                continue
            for d in n.children or []:
                if not d.key:
                    continue
                kids = {c.key.lower() for c in (d.children or []) if c.key}
                if d.key.lower() in ctrl or d.key.lower().startswith(("any_", "random_")):
                    problems += 1
                    print(f"{rel(f)}:{d.line}: `{d.key}` parsed as a decision name (brace nesting broken above)")
                elif not {"potential", "allow", "effect"} <= kids:
                    problems += 1
                    print(f"{rel(f)}:{d.line}: decision {d.key} lacks {sorted({'potential','allow','effect'} - kids)}")
    print(f"decisions structure: {problems} problem(s)")
    return 1 if problems else 0


# ---------------------------------------------------------------- main
# Keys whose value is a block and whose contents the engine reads as triggers.
TRIGGER_BLOCKS = {"potential", "allow", "trigger", "limit", "mean_time_to_happen",
                  "ai_will_do", "ai_chance", "modifier", "factor",
                  # common/cb_types.txt, common/issues.txt, common/rebel_types.txt
                  "can_use", "is_valid", "can_build", "allowed_states",
                  "allowed_countries", "allowed_substate_regions",
                  "allowed_states_in_crisis", "spawn_chance", "will_get_access"}
EFFECT_BLOCKS = {"effect", "option", "immediate", "on_po_accepted",
                 "demands_enforced_effect", "demands_enforced_trigger"}
# Iterator scopes the engine only knows in effect context. Used as a trigger it
# consumes the opening brace as a scalar value, so the block's closing brace
# closes the PARENT: every sibling after it is promoted one level up. In a
# decision that turns `effect` / `ai_will_do` into top-level decisions with no
# potential, shown to every country as cards reading `effect_title`; in an event
# file it silently drops events.
#
# Each entry below was probed against the engine on 2026-09-06 (one decision per
# scope in a decisions file, reading the `Decisions loaded ... #N` count): these
# six load 3 decisions instead of 1, i.e. they desync. `any_pop`, `any_state`,
# `any_substate`, `any_sphere_member`, `any_greater_power`, `any_core`,
# `all_core`, `any_neighbor_country`, `any_neighbor_province`,
# `any_owned_province`, `war_countries`, `owner`, `controller`, `overlord`,
# `sphere_owner`, `capital_scope`, `upper_house`, `relation` and bare tag scopes
# all load 1 and are fine as triggers - do not add them here.
EFFECT_ONLY_SCOPES = {"any_country", "any_owned", "random_country",
                      "random_owned", "random_pop", "random_state",
                      "random_greater_power", "random_neighbor_country"}
_TOK = re.compile(r'#[^\n]*|"[^"\n]*"|[{}]|[^\s{}#=]+|=')


def _blocks(txt):
    """Yield (key, line, ancestors) for every `key = {` in a script file."""
    stack, prev = [], []
    for m in _TOK.finditer(txt):
        t = m.group(0)
        if t.startswith("#"):
            continue
        if t == "{":
            key = prev[-2] if len(prev) >= 2 and prev[-1] == "=" else None
            if key:
                yield key, txt.count("\n", 0, m.start()) + 1, list(stack)
            stack.append(key)
        elif t == "}":
            if stack:
                stack.pop()
        else:
            prev.append(t)
        if t in "{}":
            prev.append(t)


def cmd_desync(files=None):
    """Two constructs the brace counter cannot see, because the file is balanced
    and only the ENGINE's parser desyncs on it (2026-09-06 playtest: phantom
    `effect_title` decision cards, three chains silently missing):
      - an effect-only iterator scope inside a trigger block  -> eats one `}`
      - `province_event = <id>` without the block form        -> eats one `{`
    Cross-check the result with `modcheck.py engine-counts` after a launch."""
    paths = [Path(f) for f in files] if files else sorted(MOD.rglob("*.txt"))
    problems = 0
    for f in paths:
        try:
            txt = f.read_bytes().decode("cp1252")
        except (OSError, UnicodeDecodeError):
            continue
        for key, line, stack in _blocks(txt):
            if key not in EFFECT_ONLY_SCOPES:
                continue
            ctx = next((k for k in reversed(stack)
                        if k in TRIGGER_BLOCKS or k in EFFECT_BLOCKS), None)
            if ctx in TRIGGER_BLOCKS:
                problems += 1
                print(f"{rel(f)}:{line}: `{key}` is an effect-only scope but sits in "
                      f"`{ctx}`; the engine eats a brace here")
        for m in re.finditer(r"province_event\s*=\s*(\d+)", txt):
            problems += 1
            print(f"{rel(f)}:{txt.count(chr(10), 0, m.start()) + 1}: bare "
                  f"`province_event = {m.group(1)}`; needs the block form "
                  f"`province_event = {{ id = {m.group(1)} days = 0 }}`")
        # The mirror image: a scalar effect handed a block. The engine reads `{`
        # as the value, so the matching `}` closes the parent (00_CoE_RoI.txt
        # event 99985 swallowed 99984 this way).
        for m in re.finditer(r"\b((?:set|clr)_(?:country|global)_flag|change_tag|"
                             r"prestige|badboy|treasury|money)\s*=\s*\{\s*([^{}\s]+)\s*\}", txt):
            problems += 1
            print(f"{rel(f)}:{txt.count(chr(10), 0, m.start()) + 1}: "
                  f"`{m.group(1)} = {{ {m.group(2)} }}` takes a scalar, not a block; "
                  f"the engine eats a brace here")
    print(f"parser desync: {problems} problem(s)")
    return 1 if problems else 0


def cmd_engine_counts():
    """The engine logs how many decisions/events it got out of each file. Any
    file where that disagrees with a local parse desynced its parser, whatever
    the cause. Needs a launch first (scripts/gametest.ps1 is enough)."""
    log = (Path(r"E:\OneDrive\Documents\Paradox Interactive\Victoria II")
           / "CoE_RoI_R" / "logs" / "setup.log")
    if not log.exists():
        print(f"{log} not found; run scripts/gametest.ps1 first")
        return 0
    text = log.read_text(errors="replace")
    problems = 0
    for kind, pat, depth in (("decisions", r"Decisions loaded decisions/(.+?)' #(\d+)", 1),
                             ("events", r"Events loaded events/(.+?)' #(\d+)", 0)):
        for m in re.finditer(pat, text):
            name, engine = m.group(1), int(m.group(2))
            f = MOD / kind / name
            if not f.exists():
                f = GAME / kind / name
            if not f.exists():
                continue
            body = f.read_bytes().decode("cp1252", "replace")
            mine = sum(1 for _, _, stack in _blocks(body) if len(stack) == depth)
            if mine != engine:
                problems += 1
                print(f"{kind}/{name}: engine loaded {engine}, file defines {mine} "
                      f"({engine - mine:+d}) - the engine's parser desynced")
    print(f"engine counts: {problems} mismatched file(s)")
    return 1 if problems else 0


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
        if cmd == "province-paths":
            return cmd_province_paths()
        if cmd == "decisions":
            return cmd_decisions()
        if cmd == "desync":
            return cmd_desync(args)
        if cmd == "engine-counts":
            return cmd_engine_counts()
    except IndexError:
        print(f"missing argument for {cmd}\n{__doc__}", file=sys.stderr)
        return 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
