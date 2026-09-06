#!/usr/bin/env python
"""Read-only audit of CoE_RoI_R/common (+ technologies/inventions/units/poptypes).

Writes docs/audit/common.md. Usage: python scripts/audit_common.py
"""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refcheck as R
from pathlib import Path

MOD = R.MOD
VAN = R.VANILLA
out = collections.defaultdict(list)


def rep(sev, path, line, prob, fix):
    out[sev].append((str(path).replace('\\', '/'), line, prob, fix))


def rel(p):
    s = str(p).replace('\\', '/')
    i = s.find('CoE_RoI_R/')
    return s[i:] if i >= 0 else s


def T(p):
    p = Path(p)
    return R.tree(p) if p.exists() else []


# ---------------- valid modifier set
_wiki_raw = set(re.findall(r'^####\s+([A-Za-z0-9_()]+)', R.read(R.ROOT / 'docs/wiki/modifier-effects.md'), re.M))
_wiki_raw = {k.lower() for k in _wiki_raw}
wiki_keys = {k for k in _wiki_raw if '(' not in k}
wiki_pat = [re.compile('^' + re.sub(r'\\\((\w+)\\\)', '[a-z_]+', re.escape(k)) + '$')
            for k in _wiki_raw if '(' in k]
# families the wiki documents only as a pattern
wiki_pat += [re.compile(r'^(army|navy|commerce|culture|industry)_tech_research_bonus$'),
             re.compile(r'^max_.*$'), re.compile(r'^min_.*$')]


def known(k):
    # goods names are legal keys inside factory_goods_*/rgo_goods_*/national focus blocks
    return k in VALID or k in goods or any(p.match(k) for p in wiki_pat)
MODFILES = ['common/event_modifiers.txt', 'common/triggered_modifiers.txt', 'common/static_modifiers.txt',
            'common/issues.txt', 'common/national_focus.txt', 'common/crime.txt', 'common/nationalvalues.txt']
MODDIRS = ['technologies', 'inventions']


def collect_keys(base):
    ks = collections.Counter()
    files = [Path(base) / f for f in MODFILES]
    for d in MODDIRS:
        p = Path(base) / d
        if p.is_dir():
            files += sorted(p.glob('*.txt'))
    for f in files:
        if not f.exists():
            continue
        for n in R.parse(R.read(f)):
            for x in n.walk():
                if x.key and x.children is None:
                    ks[x.key.lower()] += 1
    return ks


van_keys = set(collect_keys(VAN))
mod_keys = collect_keys(MOD)
VALID = wiki_keys | van_keys

SKIP_BLOCKS = {'trigger', 'limit', 'allow', 'potential', 'ai_will_do', 'chance', 'effect',
               'on_execute', 'modifier', 'ai_chance', 'any_country', 'any_pop', 'any_owned_province',
               'war', 'has_country_flag', 'rebel', 'ideologies', 'issues', 'and', 'or', 'not',
               'ai', 'random_list', 'random', 'immediate', 'option', 'unit_names'}


def modifier_leaves(nodes):
    """Leaf key=value nodes that sit in a modifier position (not inside a trigger/effect)."""
    for n in nodes:
        if n.children is not None:
            if n.key and n.key.lower() in SKIP_BLOCKS:
                continue
            for y in modifier_leaves(n.children):
                yield y
        elif n.key:
            yield n


# ---------------- name sets
def topnames(path):
    return [(n.key, n.line) for n in T(path) if n.key and n.children is not None]


goods = set()
for cat in T(MOD / 'common/goods.txt'):
    for g in (cat.children or []):
        if g.key and g.children is not None:
            goods.add(g.key.lower())
poptypes = {p.stem.lower() for p in (MOD / 'poptypes').glob('*.txt')}
units = {p.stem.lower() for p in (MOD / 'units').glob('*.txt')}
for p in (MOD / 'units').glob('*.txt'):
    for n in T(p):
        if n.key and n.children is not None:
            units.add(n.key.lower())
buildings = {k.lower() for k, _ in topnames(MOD / 'common/buildings.txt')}
prodtypes = {k.lower() for k, _ in topnames(MOD / 'common/production_types.txt')}
cultures, culgroups = set(), set()
for cg in T(MOD / 'common/cultures.txt'):
    if cg.key and cg.children is not None:
        culgroups.add(cg.key.lower())
        for c in cg.children:
            if c.key and c.children is not None and c.key.lower() not in ('union', 'unit'):
                cultures.add(c.key.lower())
ideologies = set()
for grp in T(MOD / 'common/ideologies.txt'):
    for i in (grp.children or []):
        if i.key and i.children is not None:
            ideologies.add(i.key.lower())
governments = {k.lower() for k, _ in topnames(MOD / 'common/governments.txt')}
reform_opts = collections.defaultdict(set)
reforms = set()
for grp in T(MOD / 'common/issues.txt'):
    for iss in (grp.children or []):
        if iss.key and iss.children is not None:
            reforms.add(iss.key.lower())
            for o in iss.children:
                if o.key and o.children is not None and o.key.lower() not in ('next_step_only', 'administrative_multiplier'):
                    reform_opts[iss.key.lower()].add(o.key.lower())
allopts = set().union(*reform_opts.values()) if reform_opts else set()
techs = set()
for p in (MOD / 'technologies').glob('*.txt'):
    for n in T(p):
        if n.key and n.children is not None and n.key.lower() not in ('folders', 'schools'):
            techs.add(n.key.lower())
evmods = {k.lower() for k, _ in topnames(MOD / 'common/event_modifiers.txt')}

unknown = {}
for f in [MOD / p for p in MODFILES] + [p for d in MODDIRS for p in sorted((MOD / d).glob('*.txt'))]:
    if not f.exists():
        continue
    for x in modifier_leaves(R.parse(R.read(f))):
        if not known(x.key.lower()):
            unknown.setdefault((rel(f), x.key.lower()), x.line)
SUGGEST = {
    'local_artisan_throughput': 'local_artisan_output (the only local artisan modifier the engine knows)',
    'artisan_throughput': 'artisan_throughput does not exist; use factory_throughput/rgo_throughput or drop it',
    'global_pop_militancy': 'global_pop_militancy_modifier',
    'mobilisation_impact': 'mobilisation_economy_impact',
    'factory_maintenance': 'factory_maintenance does not exist; vanilla uses factory_owner_cost / factory_cost',
    'pensions': 'pension_level (pensions is the issue name, not a modifier)',
}
for (f, k), ln in sorted(unknown.items()):
    fix = 'probably meant `%s`' % SUGGEST[k] if k in SUGGEST else         'verify the spelling against docs/wiki/modifier-effects.md; the engine ignores unknown keys silently'
    sev = 'high' if k in SUGGEST else 'medium'
    rep(sev, f, ln, "key `%s` is not a modifier the engine knows (absent from the wiki list and from vanilla's own files)" % k, fix)

# ---------------- (g) duplicate top-level definitions
for path in ['common/event_modifiers.txt', 'common/triggered_modifiers.txt', 'common/static_modifiers.txt',
             'common/buildings.txt', 'common/production_types.txt', 'common/governments.txt',
             'common/nationalvalues.txt', 'common/crime.txt', 'common/goods.txt', 'common/ideologies.txt']:
    seen = {}
    for k, ln in topnames(MOD / path):
        kl = k.lower()
        if kl in seen:
            rep('high', 'CoE_RoI_R/' + path, ln,
                'duplicate top-level definition `%s` (first at line %d); the engine silently keeps one' % (k, seen[kl]),
                'delete or rename one of the two blocks')
        else:
            seen[kl] = ln
for label, d, nested in (('tech', 'technologies', False), ('invention', 'inventions', False)):
    seen = {}
    for p in sorted((MOD / d).glob('*.txt')):
        for n in T(p):
            if not (n.key and n.children is not None):
                continue
            items = [c for c in n.children if c.key and c.children is not None] if nested else [n]
            for t in items:
                kl = t.key.lower()
                if kl in seen:
                    rep('high', rel(p), t.line, 'duplicate %s `%s` (also %s)' % (label, t.key, seen[kl]),
                        'remove the duplicate definition')
                else:
                    seen[kl] = '%s:%d' % (rel(p), t.line)


# ---------------- duplicate sibling keys inside a definition
def dup_siblings(path, label, collect=None):
    for n in T(path):
        if not (n.key and n.children is not None):
            continue
        for scope in [c for c in n.walk() if c.children is not None]:
            if scope.key and scope.key.lower() in SKIP_BLOCKS:
                continue
            seen = {}
            for c in (scope.children or []):
                if not c.key:
                    continue
                kl = c.key.lower()
                if kl in ('modifier', 'ai_chance', 'random_list', 'unit_names', 'party', 'option'):
                    continue
                if kl in seen:
                    if collect is not None:
                        collect.add(kl)
                    elif kl not in ALLOWED_DUPS and not re.search(r'_goods_(output|throughput|cost)$', kl):
                        rep('high', rel(path), c.line,
                            '%s `%s` sets `%s` twice (also line %d); the engine reads only one of them'
                            % (label, n.key, c.key, seen[kl]),
                            'merge the two blocks/values into one')
                else:
                    seen[kl] = c.line


ALLOWED_DUPS = set()
for d in ('technologies', 'inventions'):
    for p in sorted((VAN / d).glob('*.txt')):
        dup_siblings(p, d, collect=ALLOWED_DUPS)
for f in MODFILES:
    if (VAN / f).exists():
        dup_siblings(VAN / f, 'x', collect=ALLOWED_DUPS)

for d, label in (('technologies', 'tech'), ('inventions', 'invention')):
    for p in sorted((MOD / d).glob('*.txt')):
        dup_siblings(p, label)
for f, label in (('common/event_modifiers.txt', 'modifier'), ('common/triggered_modifiers.txt', 'modifier'),
                 ('common/static_modifiers.txt', 'modifier'), ('common/crime.txt', 'crime'),
                 ('common/nationalvalues.txt', 'national value'), ('common/buildings.txt', 'building')):
    dup_siblings(MOD / f, label)

# ---------------- (b) goods references
GOODKEYS = {'goods_cost', 'build_cost', 'supply_cost', 'life_needs', 'everyday_needs', 'luxury_needs',
            'input_goods', 'efficiency'}
NONGOOD = {'cost', 'time', 'value', 'factor', 'money', 'throughput', 'output', 'input'}
for p in ([MOD / 'common/buildings.txt', MOD / 'common/production_types.txt']
          + sorted((MOD / 'units').glob('*.txt')) + sorted((MOD / 'poptypes').glob('*.txt'))):
    for n in T(p):
        for x in n.walk():
            if x.key and x.key.lower() in GOODKEYS and x.children:
                for g in x.children:
                    if g.key and g.children is None and g.key.lower() not in goods and g.key.lower() not in NONGOOD:
                        rep('high', rel(p), g.line, 'unknown good `%s` inside %s' % (g.key, x.key),
                            'use a good defined in common/goods.txt')
for n in T(MOD / 'common/production_types.txt'):
    for x in n.walk():
        if x.key and x.key.lower() == 'output_goods' and x.children is None and x.value and x.value.lower() not in goods:
            rep('high', 'CoE_RoI_R/common/production_types.txt', x.line,
                'unknown output_goods `%s`' % x.value, 'use a good from goods.txt')

# activate_* in technologies/inventions
for d in ('technologies', 'inventions'):
    for p in sorted((MOD / d).glob('*.txt')):
        for n in T(p):
            for x in n.walk():
                if not x.key or x.children is not None or not x.value:
                    continue
                k, v = x.key.lower(), x.value.lower()
                if k == 'activate_unit' and v not in units:
                    rep('high', rel(p), x.line, 'activate_unit `%s` has no definition in units/' % x.value,
                        'add the unit file or fix the name')
                if k == 'activate_building' and v not in buildings:
                    rep('high', rel(p), x.line, 'activate_building `%s` is not in common/buildings.txt' % x.value,
                        'fix the building name')
                if k == 'activate_production' and v not in prodtypes:
                    rep('medium', rel(p), x.line, 'activate_production `%s` is not in production_types.txt' % x.value,
                        'fix the production type name')

# ---------------- (e) production types / buildings
for n in T(MOD / 'common/production_types.txt'):
    if not (n.key and n.children is not None):
        continue
    for x in n.walk():
        if x.key and x.key.lower() == 'poptype' and x.children is None and x.value and x.value.lower() not in poptypes:
            rep('high', 'CoE_RoI_R/common/production_types.txt', x.line,
                'production type `%s` uses poptype `%s`, which has no poptypes/ file' % (n.key, x.value),
                'add the pop type or fix the name')
for n in T(MOD / 'common/buildings.txt'):
    if not (n.key and n.children is not None):
        continue
    pt = n.first('production_type')
    if pt and pt.lower() not in prodtypes:
        rep('high', 'CoE_RoI_R/common/buildings.txt', n.line,
            'building `%s` references production_type `%s`, which is not defined' % (n.key, pt),
            'define it in production_types.txt or fix the name')

# ---------------- (c) cultures / ideologies
def scan_refs(paths, keyset, valid, label, sev='high'):
    for p in paths:
        for n in T(p):
            for x in n.walk():
                if x.key and x.children is None and x.key.lower() in keyset and x.value and x.value.lower() not in valid:
                    rep(sev, rel(p), x.line, '%s `%s` referenced via %s is not defined' % (label, x.value, x.key),
                        'fix the name or define it')


scan_refs([MOD / 'common/rebel_types.txt', MOD / 'common/governments.txt', MOD / 'common/issues.txt',
           MOD / 'common/on_actions.txt'], {'culture'}, cultures | culgroups, 'culture')
scan_refs([MOD / 'common/rebel_types.txt', MOD / 'common/issues.txt'], {'ideology'}, ideologies, 'ideology')
for n in T(MOD / 'common/governments.txt'):
    if n.key and n.children is not None:
        for c in (n.children or []):
            if c.key and c.key.lower() == 'ideology' and c.value and c.value.lower() not in ideologies:
                rep('high', 'CoE_RoI_R/common/governments.txt', c.line,
                    'government `%s` allows undefined ideology `%s`' % (n.key, c.value), 'fix the name')
for p in sorted((MOD / 'poptypes').glob('*.txt')):
    for n in T(p):
        for x in n.walk():
            if x.key and x.key.lower() == 'ideologies' and x.children:
                for i in x.children:
                    if i.key and i.key.lower() not in ideologies:
                        rep('high', rel(p), i.line, 'unknown ideology `%s` in ideologies block' % i.key, 'fix the name')
            if x.key and x.key.lower() == 'rebel' and x.children:
                for u in x.children:
                    if u.key and u.key.lower() not in units:
                        rep('medium', rel(p), u.line, 'rebel unit `%s` has no units/ definition' % u.key, 'fix the name')

# ---------------- (d) reform options used by events/decisions
for f in R.script_files('events', 'decisions', recursive=True):
    for n in R.tree(f):
        for x in n.walk():
            if x.key and x.children is None and x.value:
                k = x.key.lower()
                if k in reform_opts and x.value.lower() not in reform_opts[k]:
                    rep('high', rel(f), x.line, 'reform `%s = %s` is not an option of that issue' % (k, x.value),
                        'use one of: ' + ', '.join(sorted(reform_opts[k])))

# ---------------- (h) triggered_modifiers
gflags, cflags = set(), set()
for f in list(R.script_files('events', 'decisions', recursive=True)) + list(R.script_files('common', recursive=True)):
    for n in R.tree(f):
        for x in n.walk():
            if x.key and x.children is None and x.value:
                k = x.key.lower()
                if k in ('set_country_flag', 'clr_country_flag'):
                    cflags.add(x.value.lower())
                if k in ('set_global_flag', 'clr_global_flag'):
                    gflags.add(x.value.lower())
for n in T(MOD / 'common/triggered_modifiers.txt'):
    if not (n.key and n.children is not None):
        continue
    trg = n.get('trigger')
    if not trg:
        rep('medium', 'CoE_RoI_R/common/triggered_modifiers.txt', n.line,
            'triggered modifier `%s` has no trigger block, so it applies to every country permanently' % n.key,
            'add a trigger = { ... }')
        continue
    for x in trg[0].walk():
        if not (x.key and x.children is None and x.value):
            continue
        k, v = x.key.lower(), x.value.lower()
        if k == 'has_country_flag' and v not in cflags:
            rep('medium', 'CoE_RoI_R/common/triggered_modifiers.txt', x.line,
                '`%s` tests country flag `%s`, which no event or decision sets' % (n.key, x.value),
                'set the flag somewhere or drop the condition')
        if k == 'has_global_flag' and v not in gflags:
            rep('medium', 'CoE_RoI_R/common/triggered_modifiers.txt', x.line,
                '`%s` tests global flag `%s`, which nothing sets' % (n.key, x.value),
                'set the flag somewhere or drop the condition')
        if k == 'has_country_modifier' and v not in evmods:
            rep('high', 'CoE_RoI_R/common/triggered_modifiers.txt', x.line,
                '`%s` tests country modifier `%s`, which is not in event_modifiers.txt' % (n.key, x.value),
                'define the modifier or fix the name')

# ---------------- (i) cb_types
van_cb = {n.key.lower() for n in T(VAN / 'common/cb_types.txt') if n.key and n.children is not None}
granted = set()
for f in R.script_files('events', 'decisions', recursive=True):
    for n in R.tree(f):
        for x in n.walk():
            if x.key and x.key.lower() in ('add_casus_belli', 'casus_belli') and x.children:
                for c in x.children:
                    if c.key and c.key.lower() == 'type' and c.value:
                        granted.add(c.value.lower())
cb_seen = {}
for n in T(MOD / 'common/cb_types.txt'):
    if not (n.key and n.children is not None) or n.key.lower() == 'peace_order':
        continue
    k = n.key.lower()
    if k in cb_seen:
        rep('high', 'CoE_RoI_R/common/cb_types.txt', n.line,
            'duplicate casus belli `%s` (first at line %d)' % (n.key, cb_seen[k]), 'remove one of the two blocks')
    cb_seen[k] = n.line
    if n.first('sprite_index') is None:
        rep('medium', 'CoE_RoI_R/common/cb_types.txt', n.line,
            'cb `%s` has no sprite_index; vanilla sets one on every cb' % n.key, 'add sprite_index = N')
    if n.first('badboy_factor') is None:
        rep('low', 'CoE_RoI_R/common/cb_types.txt', n.line, 'cb `%s` has no badboy_factor' % n.key,
            'add badboy_factor = 1.0 or confirm zero infamy is intended')
    av = n.first('available')
    if av and av.lower() == 'no' and k in granted:
        rep('high', 'CoE_RoI_R/common/cb_types.txt', n.line,
            'cb `%s` is `available = no` but events/decisions still add it as a wargoal' % n.key,
            're-enable the cb or remove the add_casus_belli calls')
for cb in sorted(granted - set(cb_seen)):
    rep('high', 'CoE_RoI_R/common/cb_types.txt', 1,
        'events/decisions add casus belli `%s`, which cb_types.txt does not define' % cb,
        'define the cb or fix the add_casus_belli type')
missing_van = sorted(van_cb - set(cb_seen))

# ---------------- (f) defines.lua
def parse_defines(path):
    d, dups = {}, []
    for i, ln in enumerate(R.read(path).split('\n'), 1):
        s = ln.split('--')[0]
        m = re.match(r'\s*([A-Za-z0-9_]+)\s*=\s*(.+?),?\s*$', s)
        if m and m.group(2).strip() not in ('{',):
            k, v = m.group(1), m.group(2).rstrip(',').strip()
            if not re.match(r'^[A-Z0-9_]+$', k):
                continue
            if k in d:
                dups.append((k, i, d[k][1]))
            d[k] = (v, i)
    return d, dups


md, mdups = parse_defines(MOD / 'common/defines.lua')
vd, _ = parse_defines(VAN / 'common/defines.lua')
def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


changed = []
for k, (v, ln) in sorted(md.items()):
    if not v:
        continue
    if k in vd and vd[k][0] != v:
        a, b = num(vd[k][0]), num(v)
        if a is not None and b is not None and a == b:
            continue  # cosmetic reformatting only (0.2 vs 0.20)
        changed.append((k, vd[k][0], v, ln))
    elif k not in vd:
        changed.append((k, '(absent)', v, ln))
missing_def = sorted(set(vd) - set(md))
for k, ln, prev in mdups:
    rep('high', 'CoE_RoI_R/common/defines.lua', ln,
        'duplicated key `%s` (also line %d); Lua silently keeps the last value' % (k, prev),
        'delete one of the two assignments')

# curated plausibility notes on individual defines
DEFNOTES = {
    'MAX_BUREAUCRACY_PERCENTAGE': ('medium', 'cut 10x (0.01 -> 0.001): at most 0.1% of a pop may be bureaucrats, '
                                   'while BUREAUCRACY_PERCENTAGE_INCREMENT is 0, so admin efficiency is effectively '
                                   'frozen at BASE_COUNTRY_ADMIN_EFFICIENCY',
                                   'confirm the trio MAX_BUREAUCRACY_PERCENTAGE / BUREAUCRACY_PERCENTAGE_INCREMENT / '
                                   'BASE_COUNTRY_ADMIN_EFFICIENCY is intended, otherwise restore a non-zero increment'),
    'BUREAUCRACY_PERCENTAGE_INCREMENT': ('medium', 'set to 0, so bureaucrats add no administrative efficiency at all',
                                         'restore a small positive increment or document the flat-admin design'),
    'INFAMY_STATUS_QUO': ('medium', 'raised from 0 to 1: a white peace now costs infamy, which vanilla never does',
                          'set back to 0 unless charging infamy for status quo is deliberate'),
    'INFAMY_COLONY': ('low', 'raised from 0 to 1 (colonial wargoals now cost infamy)', 'confirm intended'),
    'SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT': ('medium', 'raised from 1500 to 10000000, i.e. effectively unlimited loans '
                                           'from shadowy financiers', 'cap it at a value the AI cannot exploit'),
    'CB_DETECTION_CHANCE_BASE': ('low', 'raised from 15 to 1000: CB justification is always detected',
                                 'confirm intended; it disables covert CB fabrication'),
    'SUPPLY_RANGE': ('low', 'cut from 250 to 50, which shrinks overseas supply reach sharply',
                     'sanity-check colonial campaigns with this value'),
    'BADBOY_LIMIT': ('medium', 'doubled from 25 to 50, so containment coalitions almost never form',
                     'confirm intended for a Concert-of-Europe game where infamy is the main brake'),
    'TECH_YEAR_SPAN': ('low', 'cut from 140 to 50 while the mod runs 1821-1936, so the year-based tech cost ramp '
                       'ends around 1871', 'widen it or confirm the intended late-game pacing'),
    'PROMOTION_ASSIMILATION_CHANCE': ('low', 'set to 0, disabling assimilation on promotion (ASSIMILATION_SCALE was '
                                      'raised 0.004 -> 0.03 instead)', 'confirm the two changes are meant together'),
}
for k, (sev, prob, fix) in DEFNOTES.items():
    if k in md and k in dict((c[0], c) for c in changed):
        rep(sev, 'CoE_RoI_R/common/defines.lua', md[k][1], '%s %s' % (k, prob), fix)

# plausibility of key defines
def dval(k):
    try:
        return float(md.get(k, ('nan',))[0])
    except ValueError:
        return None


start = md.get('START_DATE', ('?',))[0]
if '1821' not in str(start) and start != '?':
    rep('medium', 'CoE_RoI_R/common/defines.lua', md.get('START_DATE', ('', 0))[1],
        'START_DATE is %s but bookmarks.txt starts the mod at 1821.9.1' % start,
        'set START_DATE to "1821.9.1" (or confirm the engine ignores it)')
for k, lo, hi in (('MAX_WAR_EXHAUSTION', 10, 100), ('COLONIAL_LIFERATING', 0, 40),
                  ('BASE_COUNTRY_TAX_EFFICIENCY', 0.1, 2.0), ('MAX_CRIMEFIGHT_PERCENT', 0, 100)):
    v = dval(k)
    if k in md and v is not None and not (lo <= v <= hi):
        rep('medium', 'CoE_RoI_R/common/defines.lua', md[k][1],
            '%s = %s is outside the plausible range %s-%s' % (k, md[k][0], lo, hi), 'review the value')

# ---------------- report
L = []
A = L.append
A('# common/ audit')
A('')
A('Read-only audit produced by `scripts/audit_common.py` (re-runnable). Vanilla reference: `%s`.' % VAN)
A('')
A('## Counts')
A('')
A('| set | mod | vanilla |')
A('|---|---|---|')
A('| goods | %d | - |' % len(goods))
A('| pop types | %d | - |' % len(poptypes))
A('| unit files | %d | - |' % len(list((MOD / 'units').glob('*.txt'))))
A('| buildings | %d | - |' % len(buildings))
A('| production types | %d | - |' % len(prodtypes))
A('| cultures / culture groups | %d / %d | - |' % (len(cultures), len(culgroups)))
A('| ideologies | %d | - |' % len(ideologies))
A('| governments | %d | - |' % len(governments))
A('| issues / reform options | %d / %d | - |' % (len(reforms), len(allopts)))
A('| technologies | %d | - |' % len(techs))
A('| event modifiers | %d | - |' % len(evmods))
A('| casus belli | %d | %d |' % (len(cb_seen), len(van_cb)))
A('| defines.lua keys | %d | %d |' % (len(md), len(vd)))
A('| distinct modifier keys used | %d | %d |' % (len(mod_keys), len(van_keys)))
A('')
A('Valid modifier vocabulary = %d wiki entries + %d keys vanilla itself uses = %d accepted names.' %
  (len(wiki_keys), len(van_keys), len(VALID)))
A('Vanilla `defines.lua` keys absent from the mod copy: %d%s' %
  (len(missing_def), (' (' + ', '.join(missing_def[:10]) + ')') if missing_def else ''))
A('Vanilla casus belli absent from the mod override: %d%s' %
  (len(missing_van), (' (' + ', '.join(missing_van[:10]) + ')') if missing_van else ''))
A('')
A('## defines.lua diff (vanilla -> mod)')
A('')
A('| key | vanilla | mod | line |')
A('|---|---|---|---|')
for k, o, n_, ln in changed:
    A('| %s | %s | %s | %d |' % (k, o, n_, ln))
A('')
A('%d changed or mod-only values.' % len(changed))
A('')
A('## Checks that came back clean')
A('')
for t in ['goods referenced by buildings/production_types/units/poptypes all exist in goods.txt (308 refs)',
          'activate_unit / activate_building / activate_production in technologies+inventions all resolve',
          'production_types poptype/owner entries all have a poptypes/ file (30 refs); every building '
          'production_type is defined',
          'cultures and ideologies referenced by rebel_types, governments, issues, on_actions and poptypes all exist',
          'every `reform = option` used by events/decisions is a real option of that issue',
          'triggered_modifiers triggers reference only flags that are set somewhere and modifiers that exist',
          'no casus belli is added by an event/decision without being defined, and none marked `available = no` '
          'is still granted; every cb has sprite_index and badboy_factor',
          'no duplicate tech, invention, building, production type, government, good or ideology names']:
    A('- ' + t)
A('')
A('Repeated `rgo_goods_*` / `factory_goods_*` blocks inside one tech are vanilla idiom (vanilla industry_tech.txt '
  'does the same) and are not reported.')
A('')
A('## Defects')
A('')
for sev in ('high', 'medium', 'low'):
    A('### [%s] (%d)' % (sev, len(out[sev])))
    A('')
    for p, ln, prob, fix in out[sev]:
        A('- `%s:%s` - %s - fix: %s' % (p, ln, prob, fix))
    A('')
A('## Fixed (2026-09-06)')
A('')
for t in ["`crime.txt` - `local_artisan_throughput` -> `local_artisan_output` (x2). Only province-scope "
          "artisan modifier the engine has; the same file already used it for `immoral_business`.",
          "`event_modifiers.txt` - `mobilisation_impact` -> `mobilisation_economy_impact` "
          "(dervish_dhaanto_modifier); vanilla nationalvalues.txt/event_modifiers.txt use the long name.",
          "`event_modifiers.txt` - `global_pop_militancy` -> `global_pop_militancy_modifier` (papal_rule).",
          "`event_modifiers.txt` - deleted the first of the two `silk_famine` blocks (was line 138); the one "
          "kept is under the `##### WORKPLACE EVENTS #####` header, matching events/WorkPlaceEvents.txt, "
          "which is the only user of the modifier.",
          "`triggered_modifiers.txt` - `factory_maintenance` -> `factory_owner_cost` in the ten "
          "`admin_found_*` blocks. No `factory_maintenance` exists; vanilla issues.txt uses "
          "`factory_owner_cost` for owner-borne factory cost, at comparable magnitudes (0.3-0.6).",
          "`triggered_modifiers.txt` - the four `pensions = 5.0 / 10 / 100 / 2500` lines in `money_hoarder_*` "
          "commented out rather than renamed. `pensions` is the issue name; the modifier is `pension_level`, "
          "a 0-1 fraction, so `pension_level = 2500` would be a 250,000% pension. The engine has always "
          "ignored these lines, and `min_social_spending = 0.50` in the same blocks already carries the "
          "intent, so commenting them out is behaviour-preserving.",
          "`issues.txt` - the four `artisan_throughput` lines (immigration_policy, diplomatic_reform) "
          "commented out. There is no national artisan modifier; each line was a twin of the "
          "`rgo_throughput` line beside it with the same value, which still applies.",
          "`defines.lua` - `CEASECOLONIZATION_DIPLOMATIC_COST` was assigned twice (448 and 473) with the "
          "same value; the earlier one was deleted, so the surviving value is **1**.",
          ]:
    A('- ' + t)
A('')

# Hand-written narrative, regenerated verbatim so a re-run cannot lose it.
FOLLOWUPS_2026_09 = """
## Follow-ups after the defines change (2026-09-06)

Owner decision, applied to `common/defines.lua`: `INFAMY_STATUS_QUO` 1 -> **0**,
`BADBOY_LIMIT` 50 -> **25**, `MAX_BUREAUCRACY_PERCENTAGE` 0.001 -> **0.01**,
`BUREAUCRACY_PERCENTAGE_INCREMENT` 0.000 -> **0.001**, and in the follow-up pass
`BASE_COUNTRY_ADMIN_EFFICIENCY` 1.0 -> **0.2**. All five are now the vanilla /
real-world values and all five therefore dropped out of the defines diff table above.
Each changed line carries a
`-- CoE 2026-09: real-world value, see docs/audit/common.md` trailing comment.

The script that was written against the old values has now been retuned. What was done,
and what was deliberately left, is below.

### Which `badboy` reading was verified

Two different things use the word `badboy`:

- As an **effect** (`badboy = 4` inside an `option` / `effect`) it is straight infamy
  points. Halving the limit doubles the sting of every one of these without touching a
  single number.
- As a **trigger** (`badboy = 0.8` inside a `trigger` / `limit` / `allow` /
  `ai_will_do` / `ai_chance` / `mean_time_to_happen` modifier) it is a *fraction of the
  infamy limit*.

The fraction reading is the correct one, verified two ways.
`docs/wiki/list-of-conditions.md:317` states it outright: "X in this case is not a
straight integer. It's a percentage of 25 (the 'infamy limit'). So 20 infamy is 0.8, and
50 infamy is 2.0." Vanilla usage agrees without a single exception: across
`events/` and `decisions/` in the base game every effect-scope `badboy` is an integer
1-10 and every trigger-scope `badboy` is a fraction 0.2-0.8 (e.g.
`decisions/France.txt:243` grants `badboy = 4` while the `ai_will_do` eight lines below
tests `badboy = 0.5`; `events/GreatPowers.txt:84` grants `badboy = 1` while the
`mean_time_to_happen` at :127-:131 tests 0.4 and 0.8). A third, mod-internal
confirmation: the twelve `badboy = -1000` / `badboy = 24.99` pairs in
`events/GreatWar_Events.txt` and `events/InfamyWar_Events.txt:511` are commented
"reduce infamy to 24.99" - they were written for a limit of **25** all along and are
correct again now.

So a trigger written `badboy = 15` never meant "15 infamy"; it meant 15x the limit
(375 infamy), which is unreachable. Those were bugs under the old limit too.

### Absolute infamy grants, halved (applied)

Every effect-scope grant above 10 was halved so it keeps the same share of the limit it
had at 50. 38 lines in 17 files:

| file | before -> after |
|---|---|
| `events/1german_revolution_1848.txt` (10 options) | 150 -> 75, 125 -> 63, 100 -> 50 (x2), 80 -> 40, 75 -> 38 (x2), 50 -> 25, 40 -> 20, 20 -> 10 |
| `events/Greater Germany.txt` (6 options) | 40 -> 20 (x2), 20 -> 10 (x4) |
| `events/ACW.txt` | 25 -> 13 (x2), 15 -> 8 |
| `events/2nd_grand_revolution.txt` | 30 -> 15 |
| `events/BELFlavor.txt` | 15 -> 8 (x2) |
| `events/CLMFlavor.txt`, `events/PERFlavour.txt` | 15 -> 8 |
| `events/ITAFlavor.txt:797` | 18 -> 9 |
| `events/PORFlavor.txt:1699` | 25 -> 13 |
| `decisions/BYZ_Expansion.txt` (4 effects) | 20 -> 10, 18 -> 9, 15 -> 8, 12 -> 6 |
| `decisions/AUS.txt`, `decisions/GRE.txt`, `decisions/SWI_neutrality.txt` | 25 -> 13 |
| `decisions/France.txt:570` (`fra_setup`), `decisions/Ottoman_Dec.txt:86` | 40 -> 20 |
| `decisions/KRA.txt:219` | 20 -> 10 |
| `decisions/NationalUnification.txt:153/:159` | 20 -> 10 and 10 -> 5 |

Halves were rounded to the nearest integer, ties up. `NationalUnification.txt:159` is
the one grant of 10 that was halved anyway: it is the other branch of the same
`random_owned` pair as :153, and leaving it would have flattened the vassal /
non-vassal distinction the effect exists to draw.

**Left alone on purpose:**

- **Grants of 10 and below** - 32 grants of exactly 10 and roughly 250 of 1-9. At a
  limit of 25 a grant of 10 is 40% of the limit, which is a heavy but defensible price
  for annexing a neighbour, and these were never "sized for 50" the way the 40-150 tier
  was. The 10s sit in `decisions/AUS.txt:146`, `GRE.txt:119`, `Irredentism.txt:464`,
  `Italy.txt:628`, `KRA.txt:563`, `TUR.txt:732`, `events/ACW.txt:2727`,
  `BELFlavor.txt:601, :1304`, `CLMFlavor.txt:683`, `ChileanEvents.txt:308`,
  `CrimeanWar.txt:561`, `Greater Germany.txt:239, :1606`,
  `NationalUnification.txt:84, :777, :1020, :1187, :1496`, `Oriental Crisis.txt:74`,
  `PERFlavour.txt:2296`, `POLflavor.txt:98, :153, :183, :236, :266, :319, :406`,
  `PanNationalists.txt:1262`, `SPAFlavor.txt:3521, :4515`. Revisit as a block if a
  play-test says expansion is now impossible.
- **The `badboy = -1000` wipes** (13 in `GreatWar_Events.txt` / `InfamyWar_Events.txt`)
  and the `badboy = 24.99` that follows each of them. That pair means "clamp infamy to
  just under the limit", and the limit it was written for is exactly the 25 now in
  force, so the pattern is correct for the first time in years.
- The negative grants `-50` / `-25` / `-15` / `-10` and below. They are relief, not
  cost; halving them would only make relief stingier.

### Trigger thresholds written as absolute infamy, converted (applied)

Twelve `ai_will_do` / `ai_chance` modifiers used integers where the engine wanted a
fraction, so they demanded 125-500 infamy and never fired. Converted to fractions of the
25 limit that preserve the infamy each author meant:

- `decisions/BYZ_Expansion.txt:77, :216, :303` - `badboy = 5` -> **0.2**
- `decisions/BYZ_Expansion.txt:143, :409, :477, :570, :644` - `badboy = 10` -> **0.4**
- `decisions/BYZ_Expansion.txt:356, :525` - `badboy = 15` -> **0.6**
- `events/RUSFlavor.txt:1897` - `badboy = 20` -> **0.8** (completes an
  `ai_chance` ladder whose other rungs are 0.2 / 0.4 / 0.6)
- `events/RUSFlavor.txt:3181` - `badboy = 15` -> **0.6**
- `inventions/culture_inventions.txt:1804` - the `expansionism` invention's `chance`
  modifier used `badboy = 5` (125 infamy, never true), so the intended "warmongers get
  this invention sooner" `factor = 2` never applied -> **0.4**. It is the only
  trigger-scope `badboy` anywhere in `inventions/` or `technologies/`.

Each of these was previously a dead `factor = 0` guard, so the AI took decisions it was
supposed to refuse at high infamy; they now bite.

**Not converted:** the containment thresholds in `events/InfamyWar_Events.txt`
(`badboy = 1.5` at :24, `badboy = 2` at :106, :145, :241, :255-:339, :375, :431) and
`events/crises.txt:625, :629` (1.5 / 2). These are already fractions and read as "at the
limit", "1.5x the limit", "2x the limit" - a coherent ladder. What changed is that they
now trip at 25 / 37.5 / 50 infamy instead of 50 / 75 / 100, which is the intended
consequence of the smaller limit and the first thing to watch in a play-test.
The roughly 200 other fractional triggers across `events/` and `decisions/` rescale by
themselves for the same reason and were not touched.

**[low] `INFAMY_STATUS_QUO` 1 -> 0.** No script reads the define and nothing tests for
"infamy from a white peace"; the 56 `casus_belli = status_quo` grants across 23 event
and decision files are unaffected. The status-quo wargoal is free again, as in vanilla.
Nothing to retune.

### Bureaucracy and administrative efficiency (applied)

**`BASE_COUNTRY_ADMIN_EFFICIENCY` 1.0 -> 0.2** (`defines.lua:11`, the vanilla value).
The 1.0 was set by the same 2021 commit that zeroed `BUREAUCRACY_PERCENTAGE_INCREMENT`
("disabled admin efficiency for now"); the pair was one switch-off, and leaving 1.0 in
place would have kept the restored cap and increment inert - every country would sit at
100% administrative efficiency no matter how few bureaucrats it employed. Lowering it is
what makes administrative efficiency something a country earns.

What this changes in game:

- **Administrative efficiency** now starts at 20% and climbs with the bureaucrat share
  of each state's population, capped at `MAX_BUREAUCRACY_PERCENTAGE` (1.0%) plus
  `BUREAUCRACY_PERCENTAGE_INCREMENT` (0.1%) per administrative reform level. The only
  administrative reform ladder is `admin_reform` (`common/issues.txt:1103`) and it has
  **three** steps - `no_admin_reform`, `yes_admin_reform`, `advanced_admin_reform` - the
  last of which is `allow = { year = 1850 }`. So the real cap is **1.1%** for a reformed
  country before 1850 and **1.2%** after it, never more. A 1821 state with no reform and
  no bureaucrats is at 20% efficiency; hiring to ~1% takes it to 100%.
- **Tax efficiency** is the visible consequence. `BASE_COUNTRY_TAX_EFFICIENCY` is 0.50
  in this mod and administrative efficiency multiplies on top of it, so an
  unadministered country collects far less than it did yesterday. Early-game budgets get
  tighter and the gap between a well-run and a badly-run state widens; this is the
  intended realism, but it is the single largest economic consequence of the whole
  defines pass and needs a play-test on a poor tag as well as on a great power.
- **Bureaucrat demand** rises by an order of magnitude relative to the 0.1% cap regime
  (there was no reason to hire past 0.1% before, and no reward for it either since
  efficiency was pinned at 100%). `common/national_focus.txt:42` (`promote_bureaucrats`)
  and the `bureaucrats` promotion effects in the education / RGO chain
  (`events/+education_RGO.txt:146, :183`, `events/00_CoE_RoI.txt:717`) now do something
  rather than nothing. Bureaucrats are `state_capital_only` middle-strata pops paid out
  of the administration budget, so the cost shows up as administrative spending.

**`common/triggered_modifiers.txt:872-1052` - the `admin_found_*` ladder re-cut.** The
ten tiers stepped `bureaucrats = 0.005 / 0.010 / ... / 0.050`, i.e. up to forty times the
useful ceiling; every rung above 0.012 rewarded hiring the engine ignores, and under the
old 0.1% cap every single rung did. They now step **0.001** at a time, 0.003 -> 0.012,
which is the whole reachable band: tier 8 sits at the base cap (1.0%), tier 9 at the
pre-1850 reformed cap (1.1%) and tier 10 at the post-1850 `advanced_admin_reform` cap
(1.2%). Nothing in the ladder is dead script any more, and the top tier is a genuine
end-state reward. Only the `trigger` blocks moved; every modifier payload is unchanged.

**[low] `common/issues.txt:1106, :1140, :1607, :1638`** - the four
`administrative_efficiency(_modifier)` reform effects (-0.05, +0.05, +0.025, +0.05) and
`common/event_modifiers.txt:3632` (+0.05) are relative and still need no edit, but they
were sized while admin efficiency was pinned at 1.0 and now apply to a number that
actually moves. Worth a second look after a play-test.
"""

A('## Deferred to balance pass')
A('')
A('Real balance decisions, not script errors - each was a deliberate edit during the Roar of Industry '
  'rework and needs a play-test, not a patch. Four of the five were decided on 2026-09-06; see '
  '"Follow-ups after the defines change" below.')
A('')
for t in ["~~**MAX_BUREAUCRACY_PERCENTAGE** 0.01 -> 0.001~~ **restored to 0.01 on 2026-09-06.** "
          "(c4a60eb3, 2020-12-16, \"more bureaucrats needed\") "
          "- lowering the cap on how much of a state's admin need one bureaucrat pop covers was meant to "
          "force players to keep far larger bureaucracies.",
          "~~**BUREAUCRACY_PERCENTAGE_INCREMENT** 0.001 -> 0~~ **restored to 0.001 on 2026-09-06.** "
          "(669e751c, 2021-10-16, \"disabled admin "
          "efficiency for now\") - explicitly a temporary switch-off while BASE_COUNTRY_ADMIN_EFFICIENCY "
          "was raised to 1.0; it was never switched back on.",
          "~~**INFAMY_STATUS_QUO** 0 -> 1~~ **restored to 0 on 2026-09-06.** "
          "(bf2f82c2, 2020-12-12, \"better cb fabrication\") - part of the CB "
          "rework; charging infamy for a white peace stops the AI from spamming wars it then walks away from.",
          "**SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT** 1500 -> 10000000 (a236e0a8, 2021-05-16, \"loans\") - "
          "raised alongside MAX_LOAN_CAP_FROM_BANKS 3 -> 10 and LOAN_BASE_INTEREST 0.02 -> 0.005 so the "
          "reworked economy could actually finance industrialisation on credit; effectively uncapped. "
          "**Still open.**",
          "~~**BADBOY_LIMIT** 25 -> 50~~ **restored to 25 on 2026-09-06.** "
          "(4182c8e5, 2018-11-26, \"higher badboy (will see)\") - doubled so a "
          "Concert-of-Europe game can tolerate sustained expansion before a containment coalition forms; "
          "the commit message says it was already provisional.",
          ]:
    A('- ' + t)
A('')
A(FOLLOWUPS_2026_09.strip('\n'))
A('')
os.makedirs(R.ROOT / 'docs/audit', exist_ok=True)
(R.ROOT / 'docs/audit/common.md').write_text('\n'.join(L), encoding='utf-8')
print('\n'.join(L[:26]))
print('DEFECTS high=%d medium=%d low=%d changed_defines=%d lines=%d' %
      (len(out['high']), len(out['medium']), len(out['low']), len(changed), len(L)))
