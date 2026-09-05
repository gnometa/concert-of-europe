#!/usr/bin/env python
"""Static audit of CoE_RoI_R province history, pops, regions and map data.

Read-only with respect to the mod.  Writes docs/audit/history-provinces.md.
Run:  python scripts/audit_provinces.py
"""
import os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, 'CoE_RoI_R')
START = (1821, 9, 1)


def rd(p):
    with open(p, 'rb') as f:
        return f.read().decode('cp1252', 'replace')


TOK = re.compile(r'"[^"\n]*"|[{}=]|[^\s{}=]+')


def tokens(text):
    out = []
    for ln, line in enumerate(text.split('\n'), 1):
        line = line.split('#', 1)[0]
        for m in TOK.finditer(line):
            out.append((m.group(0), ln))
    return out


def parse(text):
    """-> list of (key, value, line).  value is a str or a list of entries.
    Bare scalars come back as (None, token, line)."""
    tk = tokens(text)
    i = [0]

    def block():
        ents = []
        while i[0] < len(tk):
            t, ln = tk[i[0]]
            if t == '}':
                i[0] += 1
                return ents
            if t == '=' or t == '{':
                i[0] += 1
                continue
            if i[0] + 1 < len(tk) and tk[i[0] + 1][0] == '=':
                i[0] += 2
                if i[0] < len(tk) and tk[i[0]][0] == '{':
                    i[0] += 1
                    ents.append((t, block(), ln))
                else:
                    v = tk[i[0]][0] if i[0] < len(tk) else ''
                    i[0] += 1
                    ents.append((t, v, ln))
            else:
                i[0] += 1
                ents.append((None, t, ln))
        return ents

    return block()


def scalars(entries):
    return [e[1] for e in entries if e[0] is None and isinstance(e[1], str)]


# ------------------------------------------------------------------ map data
defn, dupdef = {}, []
for line in rd(os.path.join(MOD, 'map', 'definition.csv')).split('\n'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    f = line.split(';')
    if not f[0].isdigit():
        continue
    pid = int(f[0])
    if pid in defn:
        dupdef.append(pid)
    defn[pid] = f[4] if len(f) > 4 else ''

sea = set()
for k, v, ln in parse(rd(os.path.join(MOD, 'map', 'default.map'))):
    if k == 'sea_starts':
        sea = set(int(x) for x in scalars(v) if x.isdigit())
land = set(defn) - sea

cont_of = {}
for k, v, ln in parse(rd(os.path.join(MOD, 'map', 'continent.txt'))):
    if not isinstance(v, list):
        continue
    for k2, v2, _ in v:
        if k2 == 'provinces' and isinstance(v2, list):
            for p in scalars(v2):
                if p.isdigit():
                    cont_of[int(p)] = k

region_of = collections.defaultdict(list)
regions = {}
for k, v, ln in parse(rd(os.path.join(MOD, 'map', 'region.txt'))):
    if not isinstance(v, list):
        continue
    ids = [int(x) for x in scalars(v) if x.isdigit()]
    regions[k] = (ids, ln)
    for p in ids:
        region_of[p].append(k)

# ------------------------------------------------------------------ common
tags = set(re.findall(r'^\s*([A-Z0-9]{3})\s*=',
                      rd(os.path.join(MOD, 'common', 'countries.txt')), re.M))

goods = set()
for k, v, ln in parse(rd(os.path.join(MOD, 'common', 'goods.txt'))):
    if isinstance(v, list):
        for k2, v2, _ in v:
            if isinstance(v2, list):
                goods.add(k2)


def group_children(path, skip):
    out = set()
    for k, v, ln in parse(rd(os.path.join(MOD, 'common', path))):
        if not isinstance(v, list):
            continue
        for k2, v2, _ in v:
            if isinstance(v2, list) and k2 not in skip:
                out.add(k2)
    return out


cultures = group_children('cultures.txt', {'union', 'leader', 'unit', 'is_overseas'})
religions = group_children('religion.txt', set())
poptypes = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(MOD, 'poptypes'))}
poptypes |= {'slaves', 'soldiers', 'officers'}
histcountry_tags = {f[:3] for f in os.listdir(os.path.join(MOD, 'history', 'countries'))
                    if f.lower().endswith('.txt')}

# ------------------------------------------------------------------ defects
D = collections.defaultdict(list)


def add(cls, sev, path, line, problem, fix):
    D[cls].append((sev, '%s:%s' % (os.path.relpath(path, ROOT).replace('\\', '/'), line),
                   problem, fix))


DATE = re.compile(r'^(\d{3,4})\.(\d{1,2})\.(\d{1,2})$')

files_by_id = collections.defaultdict(list)
provdir = os.path.join(MOD, 'history', 'provinces')
allprov = []
disabled = []
for dp, dn, fn in os.walk(provdir):
    for f in fn:
        if not f.lower().endswith('.txt'):
            continue
        p = os.path.join(dp, f)
        allprov.append(p)
        m = re.match(r'(\d+)', f)
        if m:
            files_by_id[int(m.group(1))].append(p)
        elif re.match(r'~\s*(\d+)', f):
            disabled.append(p)
        else:
            add('naming', 'high', p, 1,
                'filename does not start with a province id, so the engine cannot map it to a province',
                'rename to "<id> - Name.txt" or delete')

owner_of = {}
stats = collections.Counter()


def walk(p, pid, ents, dated=None):
    owner = controller = None
    for k, v, ln in ents:
        if k is None:
            continue
        if isinstance(v, list):
            m = DATE.match(k)
            if m:
                walk(p, pid, v, (tuple(int(x) for x in m.groups()), ln))
            continue
        if k == 'owner':
            owner = v
            if dated is None:
                owner_of[pid] = v
        elif k == 'controller':
            controller = v
        elif k == 'trade_goods':
            if v not in goods:
                add('goods', 'high', p, ln,
                    'trade_goods = %s is not defined in common/goods.txt' % v,
                    'use a good listed in goods.txt')
        elif k == 'life_rating':
            try:
                lr = int(float(v))
            except ValueError:
                lr = -1
            if not 0 <= lr <= 100:
                add('liferating', 'high', p, ln, 'life_rating = %s outside 0-100' % v,
                    'clamp the value to 0-100')
        elif k == 'railroad':
            try:
                r = int(float(v))
            except ValueError:
                r = 0
            if r > 0:
                stats['rail'] += 1
                when = 'game start' if dated is None else '%d.%d.%d' % dated[0]
                if dated is None or dated[0] < (1836, 1, 1):
                    add('railroad', 'high', p, ln,
                        'railroad = %s at %s, before any railway exists' % (v, when),
                        'remove it, or move it into a post-1840 dated block')
        elif k in ('fort', 'naval_base'):
            try:
                lvl = int(float(v))
            except ValueError:
                lvl = -1
            if not 0 <= lvl <= 6:
                add('forts', 'medium', p, ln,
                    '%s = %s outside the buildable range 0-6' % (k, v), 'clamp to 0-6')
            elif lvl > 0:
                stats['fort' if k == 'fort' else 'nb'] += 1
        if k in ('owner', 'controller', 'add_core'):
            if not re.fullmatch(r'[A-Z0-9]{3}', v):
                add('tagfmt', 'medium', p, ln, '%s = %s is not a 3-character tag' % (k, v),
                    'correct the tag')
            elif v not in tags:
                add('badtag', 'high', p, ln,
                    '%s = %s is not registered in common/countries.txt' % (k, v),
                    'register the tag in countries.txt or use an existing one')
            elif k == 'owner' and v not in histcountry_tags:
                add('nohistcountry', 'medium', p, ln,
                    'owner = %s has no history/countries/%s - *.txt file' % (v, v),
                    'add the country history file so the tag starts with a government')
    if controller and not owner and dated is None:
        add('ctrl', 'medium', p, 1,
            'controller = %s set with no owner at game start' % controller,
            'add a matching owner, or drop the controller line')


for pid, paths in sorted(files_by_id.items()):
    if len(paths) > 1:
        add('dupfile', 'high', paths[0], 1,
            'province %d has %d history files (also %s)' % (
                pid, len(paths),
                ', '.join(os.path.relpath(x, ROOT).replace(os.sep, '/') for x in paths[1:])),
            'delete the duplicates; only one is applied and which one is undefined')
    if pid not in defn:
        add('orphanfile', 'high', paths[0], 1,
            'id %d does not exist in map/definition.csv' % pid,
            'delete the file or renumber it to a real province')
        continue
    if pid in sea:
        add('seafile', 'medium', paths[0], 1,
            'id %d is a sea province (listed in default.map sea_starts)' % pid,
            'delete; sea provinces take no history')
    p = paths[0]
    ents = parse(rd(p))
    walk(p, pid, ents)
    for k, v, ln in ents:
        if isinstance(v, list) and k and DATE.match(k):
            d = tuple(int(x) for x in DATE.match(k).groups())
            if d < START:
                stats['predate'] += 1
                add('predate', 'medium', p, ln,
                    'dated block %s is before the 1821.9.1 start and is never applied' % k,
                    'merge its contents into the top-level block, or delete it')
            elif (1836, 1, 1) <= d < (1837, 1, 1):
                stats['d1836'] += 1

for pid in sorted(land):
    if pid not in files_by_id:
        add('nofile', 'high', os.path.join(provdir, '%d - %s.txt' % (pid, defn[pid])), 1,
            'land province %d (%s) has no history file' % (pid, defn[pid]),
            'create it with owner/trade_goods/life_rating, or add the id to sea_starts')

# ------------------------------------------------------------------ regions
rgn = os.path.join(MOD, 'map', 'region.txt')
for pid in sorted(land):
    n = len(region_of.get(pid, []))
    if n == 0:
        add('noregion', 'high', rgn, 1,
            'land province %d (%s) belongs to no region, so it forms no state' % (pid, defn[pid]),
            'add the id to the appropriate region')
    elif n > 1:
        add('multiregion', 'high', rgn, 1,
            'province %d is listed in %d regions (%s)' % (pid, n, ', '.join(region_of[pid])),
            'keep the province in exactly one region')
for name, (ids, ln) in sorted(regions.items()):
    s = [i for i in ids if i in sea]
    if s:
        add('regionsea', 'high', rgn, ln,
            'region %s contains sea provinces %s' % (name, s[:6]), 'remove the sea ids')
    u = [i for i in ids if i not in defn]
    if u:
        add('regionunknown', 'high', rgn, ln,
            'region %s lists ids absent from definition.csv: %s' % (name, u[:6]),
            'remove or correct the ids')
    cs = collections.Counter(cont_of[i] for i in ids if i in land and i in cont_of)
    if len(cs) > 1:
        add('regioncont', 'medium', rgn, ln,
            'region %s spans continents %s' % (name, dict(cs)),
            'split the region, or fix map/continent.txt')
    miss = [i for i in ids if i in land and i not in cont_of]
    if miss:
        add('nocontinent', 'medium', os.path.join(MOD, 'map', 'continent.txt'), 1,
            'land provinces of region %s are on no continent: %s' % (name, miss[:6]),
            'add them to a continent block')

# ------------------------------------------------------------------ pops
popsroot = os.path.join(MOD, 'history', 'pops')
popdirs = sorted(d for d in os.listdir(popsroot) if os.path.isdir(os.path.join(popsroot, d)))
applied = [d for d in popdirs if DATE.match(d)
           and tuple(int(x) for x in DATE.match(d).groups()) <= START]
popdir = os.path.join(popsroot, sorted(applied)[-1] if applied else popdirs[0])

pop_provs, pop_total, npops = set(), 0, 0
for f in sorted(os.listdir(popdir)):
    if not f.lower().endswith('.txt'):
        continue
    p = os.path.join(popdir, f)
    for pid_s, v, ln in parse(rd(p)):
        if not pid_s or not pid_s.isdigit() or not isinstance(v, list):
            continue
        pid = int(pid_s)
        if pid not in defn:
            add('popbadprov', 'high', p, ln,
                'pops defined for province %d which is not in definition.csv' % pid,
                'delete the block or correct the id')
            continue
        if pid in sea:
            add('popsea', 'high', p, ln, 'pops defined in sea province %d' % pid,
                'delete the block')
            continue
        if pid not in owner_of:
            add('popunowned', 'low', p, ln,
                'pops in province %d (%s) which has no owner at start '
                '(normal for uncolonised land - review only if it should be owned)' % (pid, defn[pid]),
                'no change needed unless the province is meant to start owned')
        pop_provs.add(pid)
        for pt, pv, pln in v:
            if not isinstance(pv, list):
                continue
            npops += 1
            if pt not in poptypes:
                add('poptype', 'high', p, pln, 'unknown pop type "%s"' % pt,
                    'use a type defined in poptypes/')
            d = {k: x for k, x, _ in pv if isinstance(x, str)}
            try:
                sz = int(float(d.get('size', '0')))
            except ValueError:
                sz = 0
            pop_total += sz
            if sz <= 0:
                add('popsize', 'medium', p, pln,
                    '%s pop with size = %s' % (pt, d.get('size')),
                    'delete the pop or give it a positive size')
            c = d.get('culture')
            if c and c not in cultures:
                add('popculture', 'high', p, pln,
                    'culture "%s" is not defined in common/cultures.txt' % c,
                    'use a defined culture')
            r = d.get('religion')
            if r and r not in religions:
                add('popreligion', 'high', p, pln,
                    'religion "%s" is not defined in common/religion.txt' % r,
                    'use a defined religion')

for pid in sorted(land):
    if pid not in pop_provs and pid not in owner_of:
        add('nopopsany', 'medium', files_by_id[pid][0] if files_by_id.get(pid) else popdir, 1,
            'land province %d (%s) has no pops at all in history/pops/%s'
            % (pid, defn[pid], os.path.basename(popdir)),
            'add a pop block, or confirm the province is meant to be empty wasteland')

for pid in sorted(owner_of):
    if pid in land and pid not in pop_provs:
        add('nopops', 'high', files_by_id[pid][0], 1,
            'owned by %s but has no pops in history/pops/%s' % (owner_of[pid], os.path.basename(popdir)),
            'add a pop block for province %d (%s)' % (pid, defn.get(pid, '?')))

# ------------------------------------------------------------------ report
SEV = {'high': 0, 'medium': 1, 'low': 2}
TITLES = [
    ('nofile', 'Land provinces with no history file'),
    ('orphanfile', 'History files for unknown province ids'),
    ('dupfile', 'Duplicate history files for one id'),
    ('seafile', 'History files for sea provinces'),
    ('naming', 'Badly named history files'),
    ('nopopsany', 'Land provinces with no pops at all'),
    ('badtag', 'owner/controller/add_core tag not in countries.txt'),
    ('tagfmt', 'Malformed tags'),
    ('ctrl', 'controller without owner'),
    ('nohistcountry', 'owner tag with no history/countries file'),
    ('goods', 'Unknown trade_goods'),
    ('liferating', 'life_rating out of range'),
    ('noregion', 'Land provinces in no region'),
    ('multiregion', 'Provinces in more than one region'),
    ('regionsea', 'Regions containing sea provinces'),
    ('regionunknown', 'Regions listing unknown ids'),
    ('regioncont', 'Regions spanning two continents'),
    ('nocontinent', 'Land provinces on no continent'),
    ('popbadprov', 'Pops for unknown province ids'),
    ('popsea', 'Pops in sea provinces'),
    ('popunowned', 'Pops in unowned provinces'),
    ('nopops', 'Owned land provinces with zero pops'),
    ('poptype', 'Unknown pop types'),
    ('popculture', 'Unknown pop cultures'),
    ('popreligion', 'Unknown pop religions'),
    ('popsize', 'Pops with size <= 0'),
    ('predate', 'Dated blocks before the 1821.9.1 start'),
    ('railroad', 'railroad > 0 before railways exist'),
    ('forts', 'fort/naval_base out of range'),
]

L = ['# Province / pop history audit', '',
     'Generated by `scripts/audit_provinces.py` (read-only static check). Start date 1821.9.1.',
     '', '## Counts', '', '| metric | value |', '|---|---|']
for n, v in [
        ('provinces in definition.csv', len(defn)),
        ('duplicate rows in definition.csv', len(dupdef)),
        ('sea provinces (default.map sea_starts)', len(sea)),
        ('land provinces', len(land)),
        ('province history files', len(allprov)),
        ('disabled "~id - Name.txt" history files (ignored by the engine)', len(disabled)),
        ('distinct ids with a history file', len(files_by_id)),
        ('land provinces owned at start', len(owner_of)),
        ('regions in region.txt', len(regions)),
        ('land provinces placed in a region', sum(1 for p in land if region_of.get(p))),
        ('continents in continent.txt', len(set(cont_of.values()))),
        ('tags in common/countries.txt', len(tags)),
        ('history/countries files', len(histcountry_tags)),
        ('goods in common/goods.txt', len(goods)),
        ('cultures', len(cultures)),
        ('religions', len(religions)),
        ('pop folders present', ', '.join(popdirs)),
        ('pop folder applied at start', os.path.basename(popdir)),
        ('pop files', len([f for f in os.listdir(popdir) if f.lower().endswith('.txt')])),
        ('provinces with pops', len(pop_provs)),
        ('pop entries', npops),
        ('total starting population', pop_total),
        ('railroad entries anywhere', stats['rail']),
        ('starting forts / naval bases', '%d / %d' % (stats['fort'], stats['nb'])),
        ('dated blocks before 1821.9.1', stats['predate']),
        ('1836-dated blocks (vanilla-era leftovers)', stats['d1836'])]:
    L.append('| %s | %s |' % (n, v))

tot = sum(len(v) for v in D.values())
L += ['', '## Findings by class', '', '| class | count |', '|---|---|']
for key, title in TITLES:
    if D.get(key):
        L.append('| %s | %d |' % (title, len(D[key])))
L.append('| **total** | **%d** |' % tot)
L += ['', '## Defects', '',
      'Format: `path:line` — problem — proposed fix. Each class capped at 30 examples.']
for key, title in TITLES:
    items = D.get(key)
    if not items:
        continue
    items.sort(key=lambda x: (SEV[x[0]], x[1]))
    L += ['', '### %s (%d)' % (title, len(items)), '']
    for sev, loc, prob, fix in items[:30]:
        L.append('- [%s] `%s` — %s — %s' % (sev, loc, prob, fix))
    if len(items) > 30:
        L.append('- ... and %d more of this class' % (len(items) - 30))

out = os.path.join(ROOT, 'docs', 'audit', 'history-provinces.md')
os.makedirs(os.path.dirname(out), exist_ok=True)
# Everything from MANUAL_MARKER onwards is hand-written (the Fixed / Deferred log)
# and is carried over unchanged when this report is regenerated.
MANUAL_MARKER = '<!-- MANUAL: hand-maintained below, preserved on regeneration -->'
tail = ''
if os.path.exists(out):
    with open(out, encoding='utf-8') as f:
        prev = f.read()
    if MANUAL_MARKER in prev:
        tail = prev[prev.index(MANUAL_MARKER):]
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(L) + '\n')
    if tail:
        f.write(tail)
print('wrote %s (%d lines, %d defects)' % (out, len(L), tot))
for key, title in TITLES:
    if D.get(key):
        print('%-52s %d' % (title, len(D[key])))
