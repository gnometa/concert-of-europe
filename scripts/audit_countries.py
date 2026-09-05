#!/usr/bin/env python
"""Systematic audit of CoE_RoI_R/history/countries/*.txt against common/ + map data.

Read-only. Usage:  python scripts/audit_countries.py [--key]
  (no args)  full defect report to stdout
  --key      compact table for the key 1821 countries (plausibility pass)
"""
import os, re, sys, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, 'CoE_RoI_R')
VAN = os.path.join('D:' + os.sep, 'Steam', 'steamapps', 'common', 'Victoria 2')
START = (1821, 9, 1)


def rd(p):
    with open(p, 'rb') as f:
        return f.read().decode('latin-1')


def strip_comments(t):
    return re.sub(r'#[^\n]*', '', t)


def blocks(text, depth=1):
    """yield (name, body, lineno) for `name = { ... }` at the given nesting depth."""
    text = strip_comments(text)
    tok = re.compile(r'\s*([A-Za-z0-9_.\-]+)\s*=\s*\{|\{|\}|[^{}\n]+|\n')
    d = 0
    pos = 0
    line = 1
    starts = {}
    names = {}
    while pos < len(text):
        m = tok.match(text, pos)
        if not m:
            pos += 1
            continue
        s = m.group(0)
        if m.group(1) is not None:
            d += 1
            starts[d] = m.end()
            names[d] = (m.group(1), line)
        elif s == '{':
            d += 1
            starts[d] = m.end()
            names[d] = (None, line)
        elif s == '}':
            if d == depth and names.get(d, (None, 0))[0]:
                yield names[d][0], text[starts[d]:m.start()], names[d][1]
            d -= 1
        line += s.count('\n')
        pos = m.end()


def kv(text):
    """flat key=value pairs, as list of (key, value, lineno)"""
    out = []
    for i, ln in enumerate(strip_comments(text).split('\n'), 1):
        for m in re.finditer(r'([A-Za-z0-9_]+)\s*=\s*("[^"]*"|[A-Za-z0-9_.\-]+)', ln):
            out.append((m.group(1), m.group(2).strip('"'), i))
    return out


def load():
    D = {}
    ct = strip_comments(rd(os.path.join(MOD, 'common', 'countries.txt')))
    D['reg'] = {}
    for i, ln in enumerate(ct.split('\n'), 1):
        m = re.match(r'\s*([A-Z][A-Z0-9]{2})\s*=\s*"([^"]+)"', ln)
        if m:
            D['reg'][m.group(1)] = (m.group(2), i)

    cultures = set()
    for g, body, _ in blocks(rd(os.path.join(MOD, 'common', 'cultures.txt'))):
        for c, _b, _l in blocks(body):
            cultures.add(c)
    D['cultures'] = cultures

    rel = set()
    for g, body, _ in blocks(rd(os.path.join(MOD, 'common', 'religion.txt'))):
        for r, _b, _l in blocks(body):
            rel.add(r)
    D['religions'] = rel

    govs = {}
    for g, body, _ in blocks(rd(os.path.join(MOD, 'common', 'governments.txt'))):
        ids = set()
        for k, v, _l in kv(body):
            if v == 'yes' and k not in ('election', 'appoint_ruling_party', 'duration'):
                ids.add(k)
        govs[g] = ids
    D['govs'] = govs

    reforms = {}
    for grp, gbody, _ in blocks(rd(os.path.join(MOD, 'common', 'issues.txt'))):
        for rname, rbody, _l in blocks(gbody):
            opts = set(o for o, _b, _l2 in blocks(rbody))
            if opts:
                reforms[rname] = opts
    D['reforms'] = reforms

    D['nv'] = set(n for n, _b, _l in blocks(rd(os.path.join(MOD, 'common', 'nationalvalues.txt'))))

    techs = set()
    for f in glob.glob(os.path.join(MOD, 'technologies', '*.txt')):
        for t, body, _l in blocks(rd(f)):
            if re.search(r'\barea\s*=', body):
                techs.add(t)
    D['techs'] = techs

    inv = set()
    for f in glob.glob(os.path.join(MOD, 'inventions', '*.txt')):
        for t, body, _l in blocks(rd(f)):
            inv.add(t)
    D['inventions'] = inv

    D['parties'] = {}
    D['cfile_missing'] = []
    for tag, (relp, ln) in D['reg'].items():
        p = os.path.join(MOD, 'common', relp.replace('/', os.sep))
        if not os.path.isfile(p):
            D['cfile_missing'].append((tag, relp, ln))
            continue
        ps = []
        for b, body, _l in blocks(rd(p)):
            if b == 'party':
                ps.append(dict((k, v) for k, v, _ in kv(body)))
        D['parties'][tag] = ps

    D['provids'] = set()
    for ln in rd(os.path.join(MOD, 'map', 'definition.csv')).split('\n')[1:]:
        m = re.match(r'\s*(\d+);', ln)
        if m:
            D['provids'].add(int(m.group(1)))

    owner = {}
    owned = collections.defaultdict(set)
    for f in glob.glob(os.path.join(MOD, 'history', 'provinces', '*', '*.txt')):
        m = re.match(r'(\d+)', os.path.basename(f))
        if not m:
            continue
        pid = int(m.group(1))
        head = re.split(r'\n\s*\d{3,4}\.\d+\.\d+\s*=\s*\{', strip_comments(rd(f)))[0]
        o = re.search(r'\bowner\s*=\s*([A-Z]{2,3})', head)
        if o:
            owner[pid] = o.group(1)
            owned[o.group(1)].add(pid)
    D['owner'], D['owned'] = owner, owned

    D['flags'] = set()
    for d in (os.path.join(MOD, 'gfx', 'flags'), os.path.join(VAN, 'gfx', 'flags')):
        if os.path.isdir(d):
            D['flags'] |= set(x.lower() for x in os.listdir(d))
    return D


def split_head(txt):
    """return (undated head, [(datetuple, lineno, body)])"""
    lines = strip_comments(txt).split('\n')
    head, dated, i = [], [], 0
    while i < len(lines):
        m = re.match(r'\s*(\d{3,4})\.(\d{1,2})\.(\d{1,2})\s*=\s*\{', lines[i])
        if m:
            depth = lines[i].count('{') - lines[i].count('}')
            body = []
            j = i + 1
            while j < len(lines) and depth > 0:
                depth += lines[j].count('{') - lines[j].count('}')
                body.append(lines[j])
                j += 1
            dated.append(((int(m.group(1)), int(m.group(2)), int(m.group(3))), i + 1, '\n'.join(body)))
            i = j
        else:
            head.append(lines[i])
            i += 1
    return '\n'.join(head), dated


NOT_TECH = set(['civilized', 'plurality', 'prestige', 'capital', 'literacy', 'consciousness',
                'nonstate_consciousness', 'non_state_culture_literacy', 'colonial_points',
                'is_releasable_vassal', 'ruling_party', 'oob', 'schools'])

KEY = 'ENG GBR FRA AUS PRU RUS TUR SPA POR NET SWE DEN SAR TWO PAP BAV USA MEX GCO BRZ UPB PEU PER CHI QNG JAP EGY GRE HAI'.split()


def dt(s):
    try:
        a, b, c = s.split('.')
        return (int(a), int(b), int(c))
    except Exception:
        return None


def main():
    D = load()
    defects = []

    def add(sev, path, line, prob, fix):
        defects.append((sev, '%s:%s' % (path.replace('\\', '/'), line), prob, fix))

    hist = sorted(glob.glob(os.path.join(MOD, 'history', 'countries', '*.txt')))
    seen = {}
    counts = collections.Counter()
    keytab = {}
    for f in hist:
        base = os.path.basename(f)
        relp = os.path.relpath(f, ROOT)
        m = re.match(r'([A-Z][A-Z0-9]{2})(?:\s*-|\.txt$)', base)
        if not m:
            add('medium', relp, 1, 'filename does not start with "TAG - "', 'rename to "<TAG> - <Name>.txt"')
            continue
        tag = m.group(1)
        counts['files'] += 1
        seen[tag] = relp
        head, dated = split_head(rd(f))
        pairs = kv(head)
        H = dict((k, (v, l)) for k, v, l in pairs)
        flat = kv(re.sub(r'[A-Za-z0-9_]+\s*=\s*\{[^{}]*\}', '', head, flags=re.S))
        flatset = set((k, v, l) for k, v, l in flat)

        # `government`/`ruling_party` inside a sub-block (e.g. govt_flag = { government = ... })
        # is a flag override, not the country's own value; prefer the top-level occurrence.
        for _k in ('government', 'ruling_party'):
            _top = [(v, l) for kk, v, l in flat if kk == _k]
            if _top:
                H[_k] = _top[0]

        if tag not in D['reg']:
            counts['unregistered'] += 1
            add('high', relp, 1, 'history file for tag %s is not registered in common/countries.txt' % tag,
                'add %s = "countries/<Name>.txt" to common/countries.txt or delete the file' % tag)

        cap = H.get('capital')
        if not cap:
            add('medium', relp, 1, 'no capital defined', 'add capital = <province id>')
        else:
            try:
                cid = int(cap[0])
            except ValueError:
                cid = -1
            if cid not in D['provids']:
                counts['bad_capital'] += 1
                add('high', relp, cap[1], 'capital %s is not a province id in map/definition.csv' % cap[0],
                    'set capital to a valid province id')
            elif D['owned'].get(tag) and D['owner'].get(cid) != tag:
                counts['capital_not_owned'] += 1
                add('high', relp, cap[1],
                    'capital %d is owned by %s at start, not %s (tag owns %d provinces)'
                    % (cid, D['owner'].get(cid, 'nobody'), tag, len(D['owned'][tag])),
                    'move capital to a province the tag owns in 1821')

        for k, v, l in pairs:
            if k in ('primary_culture', 'culture') and v not in D['cultures']:
                counts['bad_culture'] += 1
                add('high', relp, l, '%s = %s is not defined in common/cultures.txt' % (k, v),
                    'fix the spelling or add the culture')
            elif k == 'religion' and v not in D['religions']:
                counts['bad_religion'] += 1
                add('high', relp, l, 'religion = %s is not in common/religion.txt' % v, 'use a defined religion')
            elif k == 'nationalvalue' and v not in D['nv']:
                counts['bad_nv'] += 1
                add('high', relp, l, 'nationalvalue = %s is not in common/nationalvalues.txt' % v,
                    'use an existing nv_*')
            elif k in D['reforms'] and v not in D['reforms'][k]:
                counts['bad_reform'] += 1
                add('high', relp, l, 'reform %s = %s is not an option of that reform' % (k, v),
                    'use one of: %s' % ', '.join(sorted(D['reforms'][k])[:6]))
            elif v == '1' and k not in NOT_TECH and k not in D['reforms'] and (k, v, l) in flatset:
                if k not in D['techs'] and k not in D['inventions']:
                    counts['bad_tech'] += 1
                    add('medium', relp, l, 'unknown technology/invention "%s"' % k,
                        'remove it or fix the spelling against technologies/*.txt')

        if 'primary_culture' not in H:
            counts['no_culture'] += 1
            add('medium', relp, 1, 'no primary_culture', 'add primary_culture')
        if 'religion' not in H:
            add('low', relp, 1, 'no religion', 'add religion')
        if 'nationalvalue' not in H:
            counts['no_nv'] += 1
            add('low', relp, 1, 'no nationalvalue', 'add nationalvalue = nv_*')

        gov = H.get('government')
        if not gov:
            counts['no_gov'] += 1
            add('medium', relp, 1, 'no government', 'add government = <type>')
        elif gov[0] not in D['govs']:
            counts['bad_gov'] += 1
            add('high', relp, gov[1], 'government = %s is not in common/governments.txt' % gov[0],
                'use a defined government type')

        ideo = None
        pname = None
        rp = H.get('ruling_party')
        if not rp:
            counts['no_party'] += 1
            add('medium', relp, 1, 'no ruling_party', 'add ruling_party = <party name>')
        elif tag in D['parties']:
            match = [p for p in D['parties'][tag] if p.get('name') == rp[0]]
            if not match:
                counts['party_undefined'] += 1
                add('high', relp, rp[1], 'ruling_party %s is not defined in common/%s' % (rp[0], D['reg'][tag][0]),
                    'point ruling_party at a party defined for the tag')
            else:
                p = match[0]
                pname = p.get('name')
                sd, ed = dt(p.get('start_date', '')), dt(p.get('end_date', ''))
                if sd and ed and not (sd <= START <= ed):
                    counts['party_inactive'] += 1
                    add('high', relp, rp[1],
                        'ruling_party %s is not active on 1821.9.1 (party runs %s..%s)'
                        % (rp[0], p.get('start_date'), p.get('end_date')),
                        'choose a party covering the start date or widen its start_date')
                ideo = p.get('ideology')
                if gov and gov[0] in D['govs'] and ideo and ideo not in D['govs'][gov[0]]:
                    counts['ideology_bad'] += 1
                    add('high', relp, rp[1],
                        'ruling_party %s has ideology %s but government %s does not allow it'
                        % (rp[0], ideo, gov[0]),
                        'change the government or pick a party with an allowed ideology')

        for d, l, _b in dated:
            if d < START:
                counts['early_dated'] += 1
                add('medium', relp, l,
                    'dated block %d.%d.%d is before the 1821.9.1 start date and never applies' % d,
                    'merge it into the undated head or delete it')

        if tag in KEY:
            keytab[tag] = dict(gov=(gov or ('-',))[0], ideo=ideo, party=pname,
                               civ=H.get('civilized', ('no',))[0], cap=H.get('capital', ('-',))[0],
                               cul=H.get('primary_culture', ('-',))[0],
                               slavery=H.get('slavery', ('-',))[0],
                               franchise=H.get('vote_franschise', ('-',))[0],
                               owned=len(D['owned'].get(tag, ())))

    for tag, (relp, ln) in sorted(D['reg'].items()):
        if tag == 'REB':
            continue
        if tag not in seen:
            counts['no_history'] += 1
            add('medium', 'CoE_RoI_R/common/countries.txt', ln,
                'tag %s is registered but has no history/countries file' % tag,
                'add history/countries/"%s - <Name>.txt" or drop the registration' % tag)
    for tag, relp, ln in D['cfile_missing']:
        counts['no_common_file'] += 1
        add('high', 'CoE_RoI_R/common/countries.txt', ln,
            'tag %s points at common/%s which does not exist' % (tag, relp),
            'create the country file or remove the registration')

    for tag in sorted(D['reg']):
        if tag == 'REB':
            continue
        miss = [s for s in ('', '_communist', '_fascist', '_monarchy', '_republic')
                if ('%s%s.tga' % (tag, s)).lower() not in D['flags']
                and ('%s%s.dds' % (tag, s)).lower() not in D['flags']]
        if miss:
            counts['flag_missing'] += 1
            if '' in miss:
                counts['flag_base_missing'] += 1
            add('high' if '' in miss else 'low', 'CoE_RoI_R/gfx/flags', 0,
                'tag %s missing flag(s): %s' % (tag, ', '.join('%s%s.tga' % (tag, s) for s in miss)),
                'add the missing 93x64 24-bit .tga to gfx/flags')

    if '--key' in sys.argv:
        for t in KEY:
            if t in keytab:
                k = keytab[t]
                print('%-4s gov=%-28s ideo=%-13s party=%-22s civ=%-3s cap=%-5s cul=%-14s slav=%-14s fran=%-22s prov=%d'
                      % (t, k['gov'], k['ideo'], k['party'], k['civ'], k['cap'], k['cul'],
                         k['slavery'], k['franchise'], k['owned']))
            else:
                print('%-4s ABSENT' % t)
        return

    order = {'high': 0, 'medium': 1, 'low': 2}
    defects.sort(key=lambda d: (order[d[0]], d[1]))
    print('COUNTS %s registered=%d history_files=%d'
          % (dict(counts), len(D['reg']), counts['files']))
    print('DATA cultures=%d religions=%d governments=%d reforms=%d techs=%d inventions=%d nv=%d provinces=%d'
          % (len(D['cultures']), len(D['religions']), len(D['govs']), len(D['reforms']),
             len(D['techs']), len(D['inventions']), len(D['nv']), len(D['provids'])))
    for sev, loc, prob, fix in defects:
        print('[%s] %s - %s - %s' % (sev, loc, prob, fix))


main()
