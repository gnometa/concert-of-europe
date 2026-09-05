#!/usr/bin/env python
"""Audit the mod's localisation .csv files.

Read-only. Decodes each file as cp1252 with errors='replace' so broken bytes
surface as U+FFFD instead of raising.

Load order: docs/wiki/localisation.md says an override file's name must sort
BEFORE the file that already defines the key, i.e. the alphabetically FIRST
file that defines a key wins. Conflicts are reported winner-first.
"""
import os
import re
import json
from collections import defaultdict, Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MOD = os.path.join(ROOT, 'CoE_RoI_R')
LOC = os.path.join(MOD, 'localisation')
BASELINE = {'0000_economic_rework.csv', 'newCE.csv', 'PDM_CE.csv'}
REPL = '�'
ACIRC = 'Â'
ATILDE = 'Ã'
MOJI_AEURO = 'â€'


def csv_files():
    return sorted([f for f in os.listdir(LOC) if f.lower().endswith('.csv')],
                  key=str.lower)


def rows():
    for fn in csv_files():
        with open(os.path.join(LOC, fn), 'rb') as f:
            raw = f.read()
        text = raw.decode('cp1252', errors='replace')
        for i, line in enumerate(text.split('\n'), 1):
            yield fn, i, line.rstrip('\r')


def group_of(k):
    if k.startswith('EVTNAME'):
        return 'EVTNAME'
    if k.startswith('EVTDESC'):
        return 'EVTDESC'
    if k.startswith('EVTOPT'):
        return 'EVTOPT'
    if k.endswith('_title') or k.endswith('_desc'):
        return 'decision _title/_desc'
    if re.fullmatch(r'[A-Z]{3}(_ADJ)?', k):
        return 'country tags'
    if k.startswith('PROV'):
        return 'PROV'
    return 'other'


GROUPS = ['EVTNAME', 'EVTDESC', 'EVTOPT', 'decision _title/_desc',
          'country tags', 'PROV', 'other']

PLACE = re.compile(r'(\bTODO\b|PLACEHOLDER|lorem|\bxxx\b|test event)', re.I)
ACIRC_RE = re.compile(ACIRC + r'[A-Za-z -ÿ]')


def collect():
    defs = defaultdict(list)
    malformed, mojibake, placeholder, key_eq, y1836 = [], [], [], [], []
    for fn, ln, line in rows():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        cells = line.split(';')
        key = cells[0].strip()
        eng = cells[1] if len(cells) > 1 else ''
        reason = None
        if len(cells) < 3:
            reason = 'fewer than 3 columns (truncated row)'
        elif not any(re.fullmatch(r'x[,\s]*', c.strip()) for c in cells[1:]):
            reason = ("no 'x' terminator, full width" if len(cells) >= 14
                      else "no 'x' terminator, short row (<14 cols)")
        if reason:
            malformed.append((fn, ln, reason, line[:70]))
        if not key or len(cells) < 2:
            continue
        defs[key].append((fn, ln, eng))
        if REPL in eng:
            mojibake.append((fn, ln, key, 'U+FFFD replacement char', eng[:60]))
        elif MOJI_AEURO in eng:
            mojibake.append((fn, ln, key, 'a-circ euro (UTF-8 read as cp1252)', eng[:60]))
        elif ATILDE in eng:
            mojibake.append((fn, ln, key, 'A-tilde (UTF-8 read as cp1252)', eng[:60]))
        elif ACIRC_RE.search(eng):
            mojibake.append((fn, ln, key, 'A-circumflex + letter', eng[:60]))
        if PLACE.search(eng):
            placeholder.append((fn, ln, key, eng[:60]))
        if eng.strip() and eng.strip() == key:
            key_eq.append((fn, ln, key))
        if '1836' in eng:
            y1836.append((fn, ln, key, eng[:80]))
    return defs, malformed, mojibake, placeholder, key_eq, y1836


def conflict_scan(defs):
    conflicts = defaultdict(list)
    identical = 0
    for k, occ in defs.items():
        if len(occ) < 2:
            continue
        texts = defaultdict(list)
        for fn, ln, eng in occ:
            texts[eng].append(fn)
        identical += sum(len(v) - 1 for v in texts.values())
        if len(texts) > 1:
            conflicts[group_of(k)].append((k, occ))
    return conflicts, identical


def option_scan(defs):
    """EVTOPT keys defined beyond an event's real option count."""
    opts = defaultdict(set)
    for k in defs:
        m = re.fullmatch(r'EVTOPT([A-Z])(\d+)', k)
        if m:
            opts[m.group(2)].add(m.group(1))
    ev_opts = {}
    for sub in ('events', 'decisions'):
        d = os.path.join(MOD, sub)
        for fn in os.listdir(d):
            if not fn.lower().endswith('.txt'):
                continue
            with open(os.path.join(d, fn), 'rb') as f:
                t = f.read().decode('cp1252', 'replace')
            for blk in re.split(r'\n(?=\s*(?:country_event|province_event)\b)', t):
                m = re.search(r'\bid\s*=\s*(\d+)', blk)
                if not m:
                    continue
                n = len(re.findall(r'^\s*option\s*=', blk, re.M))
                eid = m.group(1)
                ev_opts[eid] = max(ev_opts.get(eid, 0), n)
    extra = []
    for eid, letters in opts.items():
        if eid not in ev_opts:
            continue
        need = ev_opts[eid]
        surplus = sorted(l for l in letters if (ord(l) - 65) >= need)
        if surplus:
            extra.append((eid, need, ''.join(surplus)))
    return sorted(extra)


def tag_scan(defs):
    with open(os.path.join(MOD, 'common', 'countries.txt'), 'rb') as f:
        ct = f.read().decode('cp1252', 'replace')
    tags = []
    for line in ct.split('\n'):
        line = line.split('#')[0]
        m = re.match(r'\s*([A-Z]{3})\s*=\s*"', line)
        if m and m.group(1) != 'REB':
            tags.append(m.group(1))
    return (tags,
            [t for t in tags if t not in defs],
            [t for t in tags if t + '_ADJ' not in defs])


def trunc(s, n=60):
    s = s.replace('\t', ' ').replace('`', "'")
    return s[:n] + ('...' if len(s) > n else '')


MANUAL_MARKER = '<!-- MANUAL: hand-maintained below, preserved on regeneration -->'


def main():
    defs, malformed, mojibake, placeholder, key_eq, y1836 = collect()
    conflicts, identical = conflict_scan(defs)
    extra_opts = option_scan(defs)
    tags, missing_name, missing_adj = tag_scan(defs)
    base_ct = Counter(f for f, _, _, _ in malformed if f in BASELINE)
    others = [x for x in malformed if x[0] not in BASELINE]

    L = []
    A = L.append
    A('# Localisation audit')
    A('')
    A('Generated by `scripts/audit_loc.py` (read-only; csvs decoded cp1252, errors=replace).')
    A('Missing-key checks are covered by `scripts/refcheck.py` and not repeated here.')
    A('')
    A('Scanned **%d csv files**, **%s distinct keys**, in `CoE_RoI_R/localisation/`.'
      % (len(csv_files()), format(len(defs), ',')))
    A('')
    A('## Load order: which file wins')
    A('')
    A('`docs/wiki/localisation.md` (Common Modding Issues) says that to replace a key your csv')
    A('must sort **lexicographically before** the file that already defines it ("to replace')
    A('`small_arms_production_desc` defined in `beta1.csv`, your file name must be less than')
    A('`beta1.csv`"). So the **alphabetically first file defining a key wins**; later')
    A('definitions are dead text -- consistent with the mod naming overrides `00_PDM_*`,')
    A('`000_*`, `0000_*`. Conflicts below are listed winner-first.')
    A('')
    A('## 1. Keys defined in 2+ files with DIFFERENT English text')
    A('')
    tot = sum(len(v) for v in conflicts.values())
    A('**%d conflicting keys.**' % tot)
    A('')
    A('| group | conflicting keys |')
    A('|---|---|')
    for g in GROUPS:
        A('| %s | %d |' % (g, len(conflicts.get(g, []))))
    A('')
    for g in GROUPS:
        items = sorted(conflicts.get(g, []))
        if not items:
            continue
        A('### %s (%d, showing %d)' % (g, len(items), min(15, len(items))))
        A('')
        A('| key | winner (file:line -- text) | loser |')
        A('|---|---|---|')
        for k, occ in items[:15]:
            occ = sorted(occ, key=lambda o: o[0].lower())
            w, l = occ[0], occ[1]
            A('| `%s` | %s:%d -- %s | %s:%d -- %s |'
              % (k, w[0], w[1], trunc(w[2]), l[0], l[1], trunc(l[2])))
        A('')
    A('## 2. Suspect English cells')
    A('')
    A('- mojibake sequences: **%d**' % len(mojibake))
    A('- placeholder text (TODO/PLACEHOLDER/lorem/xxx/test event): **%d**' % len(placeholder))
    A('- English cell identical to the key name: **%d**' % len(key_eq))
    A('')
    if mojibake:
        by_file = Counter(x[0] for x in mojibake)
        A('### Mojibake (%d, by file)' % len(mojibake))
        A('')
        A('| file | rows |')
        A('|---|---|')
        for fn, n in by_file.most_common(20):
            A('| %s | %d |' % (fn, n))
        A('')
        A('First 15 rows:')
        A('')
        for fn, ln, k, why, eng in mojibake[:15]:
            A('- %s:%d `%s` (%s) -- `%s`' % (fn, ln, k, why, trunc(eng)))
        A('')
    if placeholder:
        A('### Placeholder text (%d, first 10)' % len(placeholder))
        A('')
        for fn, ln, k, eng in placeholder[:10]:
            A('- %s:%d `%s` -- `%s`' % (fn, ln, k, trunc(eng)))
        A('')
    if key_eq:
        A('### English == key name (%d, first 15)' % len(key_eq))
        A('')
        A(', '.join('`%s` (%s:%d)' % (k, fn, ln) for fn, ln, k in key_eq[:15]))
        A('')
    A('## 3. Rows with a bad column count / missing terminator')
    A('')
    A('**%d rows total.** Of those, **%d** are in the three known-baseline files (%s); '
      '**%d** are elsewhere.'
      % (len(malformed), sum(base_ct.values()),
         ', '.join('%s: %d' % kv for kv in sorted(base_ct.items())) or 'none',
         len(others)))
    A('')
    if others:
        A('By class (non-baseline files only):')
        A('')
        A('| reason | rows | files |')
        A('|---|---|---|')
        by_why = defaultdict(list)
        for fn, ln, why, prev in others:
            by_why[why].append(fn)
        for why, fns in sorted(by_why.items(), key=lambda kv: -len(kv[1])):
            top = ', '.join('%s (%d)' % kv for kv in Counter(fns).most_common(4))
            A('| %s | %d | %s |' % (why, len(fns), top))
        A('')
        A('The "full width" class is the dominant one: rows that have all 14 columns but end')
        A('`;;;;;` instead of `;x;`. The engine tolerates it (this is how most of the inherited')
        A('PDM files are written), so it is cosmetic. The short-row and <3-column classes are the')
        A('ones worth fixing -- a genuinely truncated row shifts the rest of the file.')
        A('')
        real = [x for x in others if 'full width' not in x[2]]
        if real:
            A('Short / truncated rows (%d, first 15):' % len(real))
            A('')
            for fn, ln, why, prev in real[:15]:
                A('- %s:%d (%s) -- `%s`' % (fn, ln, why, trunc(prev, 70)))
            A('')
    A('## 4. English text mentioning 1836 (mod starts 1821.9.1)')
    A('')
    A('**%d rows.** Most are legitimately about events dated 1836 or later; the ones to check'
      % len(y1836))
    A('are those describing 1836 as "the start" / "today" / the present situation.')
    A('')
    for fn, ln, k, eng in y1836[:20]:
        A('- %s:%d `%s` -- `%s`' % (fn, ln, k, trunc(eng, 80)))
    if len(y1836) > 20:
        A('- ... %d more' % (len(y1836) - 20))
    A('')
    A('## 5. Surplus EVTOPT keys and country tag names')
    A('')
    A('- Events with `EVTOPT<letter>` keys past their real option count: **%d** (harmless dead'
      ' localisation).' % len(extra_opts))
    if extra_opts:
        A('  - e.g. ' + ', '.join('%s(+%s)' % (e[0], e[2]) for e in extra_opts[:12]))
    A('- Tags registered in `common/countries.txt`: **%d**.' % len(tags))
    A('  - with no `TAG` name key: **%d**%s' %
      (len(missing_name),
       (' -- ' + ', '.join(missing_name[:40])) if missing_name else ''))
    A('  - with no `TAG_ADJ` key: **%d**%s' %
      (len(missing_adj),
       (' -- ' + ', '.join(missing_adj[:40])) if missing_adj else ''))
    A('')
    A('## 6. Identical duplicate rows')
    A('')
    A('**%d** redundant rows (same key, same English text, redefined in another file).'
      % identical)
    A('Harmless, but it is why a key search returns several hits; only the alphabetically')
    A('first file is read.')
    A('')

    dest = os.path.join(ROOT, 'docs', 'audit', 'localisation.md')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    # Everything from MANUAL_MARKER onwards is hand-written (the Fixed / Deferred
    # log) and is carried over unchanged when this report is regenerated.
    tail = ''
    if os.path.exists(dest):
        with open(dest, encoding='utf-8') as f:
            prev = f.read()
        if MANUAL_MARKER in prev:
            tail = prev[prev.index(MANUAL_MARKER):]
    with open(dest, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
        if tail:
            f.write(tail)
    print('wrote %s (%d lines)' % (dest, len(L) + 1))
    print(json.dumps({
        'files': len(csv_files()), 'keys': len(defs),
        'conflicts_total': tot,
        'conflicts_by_group': {g: len(conflicts.get(g, [])) for g in GROUPS},
        'mojibake': len(mojibake), 'placeholder': len(placeholder),
        'key_eq': len(key_eq), 'malformed_total': len(malformed),
        'malformed_baseline': dict(base_ct), 'malformed_other': len(others),
        'y1836': len(y1836), 'extra_opt_events': len(extra_opts),
        'tags': len(tags), 'missing_name': missing_name[:20],
        'missing_adj': len(missing_adj), 'identical_dupes': identical,
    }, indent=1))


if __name__ == '__main__':
    main()
