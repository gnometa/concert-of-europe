#!/usr/bin/env python
"""Read-only mechanical audit of diplomacy / wars / units / technologies / inventions / poptypes
for The Concert of Europe: Roar of Industry - Reignited (start date 1821.9.1).

Usage: python scripts/audit_diplomacy.py
Writes findings to stdout as "[severity] path:line -- problem".
"""
import os
import re
import glob
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, 'CoE_RoI_R')
WIKI = os.path.join(ROOT, 'docs', 'wiki')
VANILLA = r"D:\Steam\steamapps\common\Victoria 2"
START = (1821, 9, 1)


def rd(p):
    with open(p, 'rb') as f:
        return f.read().decode('cp1252', 'replace')


def strip_comments(t):
    return '\n'.join(l.split('#')[0] for l in t.split('\n'))


TOKEN = re.compile(r'"[^"]*"|[^\s{}=]+|[{}=]')


def parse(text):
    """Parse Clausewitz script into a list of (key, value); value is str, list, or None."""
    toks = TOKEN.findall(strip_comments(text))
    pos = [0]

    def block():
        out = []
        while pos[0] < len(toks):
            t = toks[pos[0]]
            if t == '}':
                pos[0] += 1
                return out
            if t == '=':
                pos[0] += 1
                continue
            if t == '{':
                pos[0] += 1
                out.append((None, block()))
                continue
            pos[0] += 1
            if pos[0] < len(toks) and toks[pos[0]] == '=':
                pos[0] += 1
                if pos[0] < len(toks) and toks[pos[0]] == '{':
                    pos[0] += 1
                    out.append((t, block()))
                else:
                    out.append((t, toks[pos[0]]))
                    pos[0] += 1
            else:
                out.append((t, None))
        return out
    return block()


def walk(node):
    for k, v in node:
        yield k, v
        if isinstance(v, list):
            for x in walk(v):
                yield x


def parse_date(s):
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', s or '')
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def def_lines(text):
    d = {}
    for m in re.finditer(r'^(\w+)\s*=\s*\{', strip_comments(text), re.M):
        d.setdefault(m.group(1), []).append(text.count('\n', 0, m.start()) + 1)
    return d


findings = []


def add(sev, path, line, problem):
    findings.append((sev, os.path.relpath(path, ROOT).replace('\\', '/'), line, problem))


# ---------------- reference data ----------------
TAGS = set(re.findall(r'^\s*([A-Z]{3})\s*=',
                      strip_comments(rd(os.path.join(MOD, 'common', 'countries.txt'))), re.M))

GOODS = set()
for cat, body in parse(rd(os.path.join(MOD, 'common', 'goods.txt'))):
    if isinstance(body, list):
        for g, gb in body:
            if isinstance(gb, list):
                GOODS.add(g)

CBS = {}
for k, v in parse(rd(os.path.join(MOD, 'common', 'cb_types.txt'))):
    if isinstance(v, list):
        CBS[k] = dict((a, b) for a, b in v if isinstance(b, str))

IDEOLOGIES = set()
for grp, body in parse(rd(os.path.join(MOD, 'common', 'ideologies.txt'))):
    if isinstance(body, list):
        for i, ib in body:
            if isinstance(ib, list):
                IDEOLOGIES.add(i)

POPTYPES = set(os.path.splitext(os.path.basename(p))[0]
               for p in glob.glob(os.path.join(MOD, 'poptypes', '*.txt')))
UNITS = set(os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(MOD, 'units', '*.txt')))
BUILDINGS = set(k for k, v in parse(rd(os.path.join(MOD, 'common', 'buildings.txt')))
                if isinstance(v, list))

# province ownership at the 1821.9.1 start
OWNERS = collections.Counter()
PROV_IDS = set()
for p in glob.glob(os.path.join(MOD, 'history', 'provinces', '*', '*.txt')):
    m = re.match(r'[^0-9]*(\d+)', os.path.basename(p))
    if not m:
        continue
    PROV_IDS.add(int(m.group(1)))
    owner = None
    depth = 0
    ok = True
    for line in strip_comments(rd(p)).split('\n'):
        dm = re.match(r'\s*(\d+)\.(\d+)\.(\d+)\s*=\s*\{', line)
        if dm:
            ok = (int(dm.group(1)), int(dm.group(2)), int(dm.group(3))) <= START
            depth += 1
            continue
        om = re.search(r'\bowner\s*=\s*([A-Z]{3})\b', line)
        if om and ok:
            owner = om.group(1)
        if depth:
            depth -= line.count('}') - line.count('{')
            if depth <= 0:
                depth = 0
                ok = True
    if owner:
        OWNERS[owner] += 1

# modifier / trigger vocabularies
MODKEYS = set()
_wp = os.path.join(WIKI, 'modifier-effects.md')
if os.path.exists(_wp):
    _w = rd(_wp)
    for m in re.finditer(r'^#{3,5}\s+([a-z_()]+)\s*$', _w, re.M):
        MODKEYS.add(m.group(1))
    for m in re.finditer(r'^\s*([a-z_]+)\s*=\s*[-\dn]', _w, re.M):
        MODKEYS.add(m.group(1))

TRIGGERS = set()
for f in ('list-of-conditions.md', 'list-of-effects.md'):
    fp = os.path.join(WIKI, f)
    if os.path.exists(fp):
        t = rd(fp)
        for m in re.finditer(r'^#{2,5}\s+`?([a-z_]+)`?', t, re.M):
            TRIGGERS.add(m.group(1))
        for m in re.finditer(r'^\s*\*?\s*`?([a-z_]+)`?\s*=', t, re.M):
            TRIGGERS.add(m.group(1))
TRIGGERS |= set('''year month invention technology always tag exists war civilized
    is_greater_power is_secondary_power has_country_flag has_global_flag has_country_modifier
    government ruling_party_ideology primary_culture is_culture_group continent capital owns
    controls literacy money plurality blockade unemployment revolt_percentage average_militancy
    average_consciousness is_vassal part_of_sphere is_sphere_leader_of num_of_ports num_of_cities
    num_of_revolts num_of_substates has_pop_type has_building brigades_compare colonial_nation
    nationalvalue total_pops total_amount_of_ships total_amount_of_divisions crisis_exist
    value who which type limit'''.split())

LOGIC = set('''OR AND NOT NAND NOR any_owned_province any_neighbor_country any_country all_core
    war_countries any_greater_power any_pop any_state any_substate capital_scope THIS FROM'''.split())

STRUCT = set('''area year cost unciv_military ai_chance chance limit effect activate_unit
    activate_building activate_technology activate_invention army_base navy_base rule news group
    enable_crime invention technology ai_will_do picture'''.split())

UNIT_STATS = set('''attack defence discipline support maneuver siege hull gun_power fire_range
    evasion torpedo_attack reconnaissance default_organisation maximum_speed supply_consumption
    colonial_points build_time max_strength move_cost limit_per_port'''.split())


def collect_modkeys(paths, kind):
    out = set()
    for p in paths:
        for name, body in parse(rd(p)):
            if not isinstance(body, list):
                continue
            src = body
            if kind == 'inv':
                src = []
                for k, v in body:
                    if k == 'effect' and isinstance(v, list):
                        src = v
            for k, v in src:
                if isinstance(v, str) and k not in STRUCT:
                    out.add(k)
    return out


VANMODS = set()
for sub, kind in (('technologies', 'tech'), ('inventions', 'inv')):
    VANMODS |= collect_modkeys(sorted(glob.glob(os.path.join(VANILLA, sub, '*.txt'))), kind)
# vanilla event/static modifiers are the authoritative list of legal modifier keys
for _f in ('event_modifiers.txt', 'static_modifiers.txt', 'issues.txt', 'nationalvalues.txt', 'traits.txt', 'cb_types.txt'):
    _fp = os.path.join(VANILLA, 'common', _f)
    if os.path.exists(_fp):
        for _n, _b in parse(rd(_fp)):
            if isinstance(_b, list):
                for _k, _v in walk(_b):
                    if isinstance(_v, str):
                        VANMODS.add(_k)

KNOWN_MODS = MODKEYS | VANMODS | GOODS | UNIT_STATS

# ---------------- 1. diplomacy ----------------
dip_files = sorted(glob.glob(os.path.join(MOD, 'history', 'diplomacy', '*.txt')))
dip_count = collections.Counter()
for p in dip_files:
    st = strip_comments(rd(p))
    for m in re.finditer(r'\b(alliance|vassal|substate|guarantee|sphere|union)\s*=\s*\{(.*?)\}',
                         st, re.S):
        kind, body = m.group(1), m.group(2)
        ln = st.count('\n', 0, m.start()) + 1
        dip_count[kind] += 1
        sdm = re.search(r'start_date\s*=\s*([\d.]+)', body)
        edm = re.search(r'end_date\s*=\s*([\d.]+)', body)
        sd = parse_date(sdm.group(1)) if sdm else None
        ed = parse_date(edm.group(1)) if edm else None
        for role in ('first', 'second'):
            mm = re.search(role + r'\s*=\s*(\w+)', body)
            if not mm:
                add('high', p, ln, '%s entry has no "%s"' % (kind, role))
                continue
            tag = mm.group(1)
            if tag not in TAGS:
                add('high', p, ln,
                    '%s %s = %s is not registered in common/countries.txt' % (kind, role, tag))
            elif OWNERS[tag] == 0 and (sd is None or sd <= START) and (ed is None or ed > START):
                add('high', p, ln,
                    '%s is active at start but %s owns no province at 1821.9.1' % (kind, tag))
        if sd is None:
            add('medium', p, ln, '%s entry has no parsable start_date' % kind)
        elif sd > START:
            add('medium', p, ln, '%s start_date %d.%d.%d is after the 1821.9.1 start' % ((kind,) + sd))
        if ed and ed <= START:
            add('low', p, ln, '%s end_date %d.%d.%d already passed at start (inert)' % ((kind,) + ed))

# ---------------- 2. wars ----------------
war_files = sorted(glob.glob(os.path.join(MOD, 'history', 'wars', '*.txt')))
active_wars = []
STATE_CBS = set(k for k, v in CBS.items()
                if any(v.get(x) == 'yes'
                       for x in ('po_demand_state',)))
for p in war_files:
    st = strip_comments(rd(p))
    dates = [d for d in (parse_date(x)
                         for x in re.findall(r'^\s*(\d+\.\d+\.\d+)\s*=\s*\{', st, re.M)) if d]
    if dates and min(dates) > START:
        add('low', p, 1, 'war begins %d.%d.%d, after the 1821.9.1 start' % min(dates))
    if dates and min(dates) <= START < max(dates):
        active_wars.append(os.path.basename(p))
    for m in re.finditer(r'\b(add_attacker|add_defender|rem_attacker|rem_defender)\s*=\s*(\w+)', st):
        tag = m.group(2)
        ln = st.count('\n', 0, m.start()) + 1
        if tag not in TAGS:
            add('high', p, ln,
                '%s = %s is not registered in common/countries.txt' % (m.group(1), tag))
        elif m.group(1).startswith('add') and OWNERS[tag] == 0:
            add('medium', p, ln, '%s = %s owns no province at 1821.9.1' % (m.group(1), tag))
    for m in re.finditer(r'war_goal\s*=\s*\{(.*?)\}', st, re.S):
        body = m.group(1)
        ln = st.count('\n', 0, m.start()) + 1
        for role in ('actor', 'receiver'):
            rm = re.search(role + r'\s*=\s*(\w+)', body)
            if rm and rm.group(1) not in TAGS:
                add('high', p, ln, 'war_goal %s = %s is not registered in common/countries.txt'
                    % (role, rm.group(1)))
        cbm = re.search(r'casus_belli\s*=\s*(\w+)', body)
        if not cbm:
            add('high', p, ln, 'war_goal has no casus_belli')
            continue
        cb = cbm.group(1)
        if cb not in CBS:
            add('high', p, ln, 'casus_belli = %s is not defined in common/cb_types.txt' % cb)
            continue
        pm = re.search(r'state_province_id\s*=\s*(\d+)', body)
        if pm and int(pm.group(1)) not in PROV_IDS:
            add('high', p, ln, 'state_province_id = %s has no province history file' % pm.group(1))
        if not pm and cb in STATE_CBS:
            add('high', p, ln, 'casus_belli = %s takes a state but the war_goal has no '
                               'state_province_id' % cb)

# ---------------- 3. units ----------------
unit_active = {}
for p in sorted(glob.glob(os.path.join(MOD, 'units', '*.txt'))):
    text = rd(p)
    st = strip_comments(text)
    fname = os.path.splitext(os.path.basename(p))[0]
    defs = parse(text)
    name = defs[0][0] if defs else fname
    if name != fname:
        add('medium', p, 1, 'unit type "%s" does not match filename "%s"' % (name, fname))
    body = dict(defs).get(name) or []
    unit_active[name] = dict((k, v) for k, v in body if isinstance(v, str)).get('active', 'yes')
    for blk in ('build_cost', 'supply_cost'):
        for b in [v for k, v in body if k == blk and isinstance(v, list)]:
            for g, val in b:
                if g not in GOODS:
                    bm = re.search(r'\b' + re.escape(g) + r'\s*=', st)
                    add('high', p, st.count('\n', 0, bm.start()) + 1 if bm else 1,
                        '%s references "%s", not a good in common/goods.txt' % (blk, g))

activated = set()
for pat in (('technologies', '*.txt'), ('inventions', '*.txt'),
            ('events', '*.txt'), ('decisions', '*.txt')):
    for p in sorted(glob.glob(os.path.join(MOD, *pat))):
        st = strip_comments(rd(p))
        for m in re.finditer(r'activate_unit\s*=\s*(\w+)', st):
            activated.add(m.group(1))
            if m.group(1) not in UNITS:
                add('high', p, st.count('\n', 0, m.start()) + 1,
                    'activate_unit = %s has no definition in units/' % m.group(1))
        for m in re.finditer(r'activate_building\s*=\s*(\w+)', st):
            if m.group(1) not in BUILDINGS:
                add('high', p, st.count('\n', 0, m.start()) + 1,
                    'activate_building = %s is not in common/buildings.txt' % m.group(1))
unreachable_units = sorted(u for u in UNITS
                           if unit_active.get(u, 'yes') == 'no' and u not in activated)
for u in unreachable_units:
    add('high', os.path.join(MOD, 'units', u + '.txt'), 1,
        'unit "%s" has active = no and is never activate_unit-ed; it can never be built' % u)

# ---------------- 4. technologies ----------------
folders = {}
for k, v in parse(rd(os.path.join(MOD, 'common', 'technology.txt'))):
    if k == 'folders' and isinstance(v, list):
        for f, body in v:
            folders[f] = [a for a, b in body]
AREAS = set(a for lst in folders.values() for a in lst)

TECHS = {}
tech_years = {}
for p in sorted(glob.glob(os.path.join(MOD, 'technologies', '*.txt'))):
    text = rd(p)
    dl = def_lines(text)
    seen = collections.Counter()
    for name, body in parse(text):
        if not isinstance(body, list):
            continue
        lns = dl.get(name, [0])
        ln = lns[min(seen[name], len(lns) - 1)]
        seen[name] += 1
        if name in TECHS:
            add('high', p, ln, 'duplicate technology name "%s" (also at %s)' % (name, TECHS[name]))
        TECHS[name] = '%s:%d' % (os.path.basename(p), ln)
        scal = dict((k, v) for k, v in body if isinstance(v, str))
        if 'year' not in scal:
            add('high', p, ln, 'technology "%s" has no year' % name)
        else:
            try:
                y = int(scal['year'])
                tech_years[name] = y
                if y < 1821:
                    add('medium', p, ln,
                        'technology "%s" year = %d predates the 1821.9.1 start' % (name, y))
            except ValueError:
                add('high', p, ln, 'technology "%s" year = %s is not a number' % (name, scal['year']))
        if 'area' not in scal:
            add('high', p, ln, 'technology "%s" has no area' % name)
        elif scal['area'] not in AREAS:
            add('high', p, ln, 'technology "%s" area = %s is not a folder area in '
                               'common/technology.txt' % (name, scal['area']))
        if 'cost' not in scal:
            add('high', p, ln, 'technology "%s" has no cost' % name)
        for k, v in body:
            if isinstance(v, str) and k not in STRUCT and k not in KNOWN_MODS:
                add('medium', p, ln, 'technology "%s" sets "%s", a key no vanilla '
                                     'tech/invention uses' % (name, k))

# ---------------- 5. inventions ----------------
INVS = {}
inv_parsed = []
for p in sorted(glob.glob(os.path.join(MOD, 'inventions', '*.txt'))):
    text = rd(p)
    dl = def_lines(text)
    seen = collections.Counter()
    for name, body in parse(text):
        if not isinstance(body, list):
            continue
        lns = dl.get(name, [0])
        ln = lns[min(seen[name], len(lns) - 1)]
        seen[name] += 1
        if name in INVS:
            add('high', p, ln, 'duplicate invention name "%s" (also at %s)' % (name, INVS[name]))
        INVS[name] = '%s:%d' % (os.path.basename(p), ln)
        if name in TECHS:
            add('high', p, ln, 'invention "%s" collides with the technology of the same name (%s)'
                % (name, TECHS[name]))
        inv_parsed.append((p, ln, name, body))

for p, ln, name, body in inv_parsed:
    lim = [v for k, v in body if k == 'limit' and isinstance(v, list)]
    if not lim:
        add('medium', p, ln, 'invention "%s" has no limit block (available from game start)' % name)
    for lb in lim:
        for k, v in walk(lb):
            if k is None or isinstance(v, list) or k in LOGIC or k in TRIGGERS:
                continue
            if k in TECHS or k in INVS:
                continue
            add('high', p, ln, 'invention "%s" limit references "%s": not a technology, '
                               'invention, or documented trigger' % (name, k))
    for k, v in body:
        if k == 'effect' and isinstance(v, list):
            for k2, v2 in v:
                if isinstance(v2, str) and k2 not in STRUCT and k2 not in KNOWN_MODS:
                    add('medium', p, ln, 'invention "%s" effect sets "%s", a key no vanilla '
                                         'tech/invention uses' % (name, k2))

# ---------------- 6. poptypes ----------------
pop_count = 0
for p in sorted(glob.glob(os.path.join(MOD, 'poptypes', '*.txt'))):
    text = rd(p)
    pop_count += 1
    d = collections.defaultdict(list)
    for k, v in parse(text):
        d[k].append(v)
    for blk in ('life_needs', 'everyday_needs', 'luxury_needs'):
        if blk not in d:
            add('medium', p, 1, 'poptype has no %s block' % blk)
            continue
        for b in d[blk]:
            if isinstance(b, list):
                for g, val in b:
                    if g not in GOODS:
                        add('high', p, 1, '%s references "%s", not a good in '
                                          'common/goods.txt' % (blk, g))
    for b in d.get('rebel', []):
        if isinstance(b, list):
            for u, val in b:
                if u not in UNITS:
                    add('high', p, 1, 'rebel block references unit "%s" with no units/ '
                                      'definition' % u)
    for b in d.get('promote_to', []):
        if isinstance(b, list):
            for t, val in b:
                if t not in POPTYPES:
                    add('high', p, 1, 'promote_to references unknown pop type "%s"' % t)
    for b in d.get('ideologies', []):
        if isinstance(b, list):
            for i, val in b:
                if i not in IDEOLOGIES:
                    add('high', p, 1, 'ideologies references unknown ideology "%s"' % i)

# ---------------- output ----------------
print('=== COUNTS ===')
print('tags registered in common/countries.txt: %d' % len(TAGS))
print('tags owning >= 1 province at 1821.9.1:  %d' % len(OWNERS))
print('diplomacy files %d, entries: %s' % (len(dip_files), dict(dip_count)))
print('war files %d; ongoing at 1821.9.1: %s' % (len(war_files), active_wars))
print('cb types %d, goods %d, buildings %d, units %d, poptypes %d' % (
    len(CBS), len(GOODS), len(BUILDINGS), len(UNITS), pop_count))
print('technologies %d, inventions %d' % (len(TECHS), len(INVS)))
if tech_years:
    yc = collections.Counter(tech_years.values())
    print('tech years %d-%d; <1821: %d; earliest tiers: %s' % (
        min(tech_years.values()), max(tech_years.values()),
        sum(1 for v in tech_years.values() if v < 1821), sorted(yc.items())[:6]))
print('vanilla modifier vocabulary: %d keys' % len(KNOWN_MODS))
print()
order = {'high': 0, 'medium': 1, 'low': 2}
sev_count = collections.Counter(f[0] for f in findings)
print('=== FINDINGS: %d (high %d / medium %d / low %d) ===' % (
    len(findings), sev_count['high'], sev_count['medium'], sev_count['low']))
for sev, rel, ln, prob in sorted(findings, key=lambda f: (order[f[0]], f[1], f[2])):
    print('[%s] %s:%d -- %s' % (sev, rel, ln, prob))
