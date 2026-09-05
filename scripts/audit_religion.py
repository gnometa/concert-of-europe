#!/usr/bin/env python3
"""Audit: pops carry culture names in the religion field; find dead religion tests."""
import re, sys, os
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "CoE_RoI_R")
def read(p):
    return open(p, 'rb').read().decode('cp1252', errors='replace')
def strip_comments(t):
    return "\n".join(l.split('#')[0] for l in t.splitlines())

# --- religion.txt: group -> members
rt = strip_comments(read(os.path.join(MOD, 'common', 'religion.txt')))
groups = {}
cur = None; depth = 0
for m in re.finditer(r'([A-Za-z_0-9]+)\s*=\s*\{|\}', rt):
    if m.group(0) == '}':
        depth -= 1
        if depth == 0: cur = None
    else:
        if depth == 0:
            cur = m.group(1); groups[cur] = []
        elif depth == 1 and cur:
            groups[cur].append(m.group(1))
        depth += 1
allrel = {r for v in groups.values() for r in v}
VANILLA = set("catholic protestant orthodox coptic sunni shiite jewish mahayana gelugpa theravada hindu sikh animist fetishist shinto".split())
REAL = allrel & VANILLA
cultures = set()
for f in os.listdir(os.path.join(MOD,'common','cultures.txt')) if False else []: pass
ct = strip_comments(read(os.path.join(MOD,'common','cultures.txt')))
depth=0
for m in re.finditer(r'([A-Za-z_0-9]+)\s*=\s*\{|\}', ct):
    if m.group(0)=='}': depth-=1
    else:
        if depth==1: cultures.add(m.group(1))
        depth+=1

# --- 1. pops
popdir = os.path.join(MOD,'history','pops','1821.9.1')
used = Counter(); commented = Counter()
for fn in os.listdir(popdir):
    t = read(os.path.join(popdir,fn))
    for line in t.splitlines():
        live, _, cm = line.partition('#')
        for mm in re.finditer(r'religion\s*=\s*([A-Za-z_0-9]+)', live): used[mm.group(1)]+=1
        for mm in re.finditer(r'religion\s*=\s*([A-Za-z_0-9]+)', cm): commented[mm.group(1)]+=1

# --- 2. history/countries state religion
cdir = os.path.join(MOD,'history','countries')
staterel = Counter(); statefiles = defaultdict(list)
for fn in os.listdir(cdir):
    for line in read(os.path.join(cdir,fn)).splitlines():
        live = line.split('#')[0]
        for mm in re.finditer(r'^\s*religion\s*=\s*([A-Za-z_0-9]+)', live):
            staterel[mm.group(1)]+=1; statefiles[mm.group(1)].append(fn)

# --- 3. scan script for religion tests
POP_KEYS = ['has_pop_religion','pop_majority_religion','dominant_issue']
targets = []
for sub, pats in [('events',['*.txt']),('decisions',['*.txt']),('inventions',['*.txt']),('technologies',['*.txt'])]:
    d = os.path.join(MOD,sub)
    for root,_,fs in os.walk(d):
        for f in fs:
            if f.endswith('.txt'): targets.append(os.path.join(root,f))
for f in ['issues.txt','rebel_types.txt','triggered_modifiers.txt','national_focus.txt','cb_types.txt']:
    p = os.path.join(MOD,'common',f)
    if os.path.exists(p): targets.append(p)

KEY_RE = re.compile(r'\b(religion|has_pop_religion|pop_majority_religion|religion_group|has_pop_religion_group|pop_majority_religion_group|state_religion|is_state_religion)\s*=\s*([A-Za-z_0-9]+)')
sites = []
for p in targets:
    txt = read(p)
    lines = txt.splitlines()
    # track NOT/NOR context crudely: look back for NOT = { on the same or preceding lines with brace depth
    depth = 0
    negstack = []
    for i,raw in enumerate(lines):
        line = raw.split('#')[0]
        for tok in re.finditer(r'\b(NOT|NOR)\s*=\s*\{|\{|\}', line):
            pass
        # compute per-line events in order
        pos = 0
        for m in re.finditer(r'\b(NOT|NOR)\s*=\s*\{|\{|\}|' + KEY_RE.pattern, line):
            g = m.group(0)
            if g.endswith('{') and (g.startswith('NOT') or g.startswith('NOR')):
                negstack.append(depth); depth += 1
            elif g == '{':
                depth += 1
            elif g == '}':
                depth -= 1
                while negstack and negstack[-1] >= depth: negstack.pop()
            else:
                key = m.group(2); val = m.group(3)
                if key and val:
                    sites.append((p, i+1, key, val, bool(negstack), raw.strip()))
sites = [s for s in sites if s[3] in allrel or s[3] in VANILLA or s[3] in groups]
real_sites = [s for s in sites if s[3] in REAL or (s[3] in VANILLA)]

if __name__ == '__main__':
    print("== religion.txt ==")
    print("groups:", len(groups), "religions:", len(allrel), "real vanilla religions still defined:", sorted(REAL))
    print("\n== pops 1821.9.1 (%d files) ==" % len(os.listdir(popdir)))
    print("distinct live religion values:", len(used), "; total entries:", sum(used.values()))
    print("live values that are real religions:", sorted(set(used)&VANILLA) or "NONE")
    print("live values that are culture names:", len(set(used)&cultures), "of", len(used))
    print("live values not a culture:", sorted(set(used)-cultures)[:20])
    print("commented-out (#religion=) real religions:", sum(v for k,v in commented.items() if k in VANILLA), "entries,", sorted(set(commented)&VANILLA))
    print("\n== history/countries religion = (state religion) ==")
    for k,v in staterel.most_common():
        print("  %-22s %4d  %s" % (k, v, "REAL" if k in VANILLA else ("culture-religion" if k in allrel else "UNDEFINED")))
    print("\n== script sites naming a real religion ==")
    per = Counter(); 
    for s in real_sites: per[os.path.relpath(s[0],ROOT).replace(chr(92),'/')]+=1
    for k,v in per.most_common(): print("  %-60s %d" % (k,v))
    print("TOTAL real-religion sites:", len(real_sites))
    ck = Counter((s[2], s[4]) for s in real_sites)
    for k,v in ck.most_common(): print("  key=%-24s negated=%-5s %d" % (k[0],k[1],v))
    print("\n-- sites --")
    for s in real_sites:
        print("%s:%d\t%s=%s\tneg=%s\t%s" % (os.path.relpath(s[0],ROOT).replace(chr(92),'/'), s[1], s[2], s[3], s[4], s[5][:90]))
