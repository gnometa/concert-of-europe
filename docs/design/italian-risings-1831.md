# The Italian risings of 1831 and the Austrian intervention

Fills gap 10 of `docs/design/1821-1836-coverage.md`: SAR/SIC/PAP/MOD have no
1820s-30s content at all. Scope kept deliberately small - the 1820-21 Naples and
Piedmont revolts are already over at the 1821.9.1 start, so they appear only as a
Carbonari undercurrent that can leave a `conservative_reaction` behind.

File: `events/ITARisingsGVG.txt`, ids 1001100-1001104 (range 1001100-1001199,
registered in `events/GVG Event IDs.txt`). Loc in `localisation/GVG_events.csv`.

## Start state (verified)

- MOD owns 739 Modena, 740 Massa; PAR owns 738 Parma; PAP owns 741 Bologna,
  742 Ferrara, 743 Ravenna (the Legations), 749 Rome, 752 Ancona.
- AUS owns Lombardy-Venetia (726-737), so the intervention is a march over the Po,
  not a landing. No alliance or guarantee ties AUS to the Italian minors in
  `history/diplomacy/` - relations are the only lever.
- No existing event touches 1830-31 in Italy: `PAPFlavor.txt` (35700, 35705) and
  `LOMFlavor.txt` (35400) are undated, `ITAFlavor.txt` is 1848+ / unification, and
  `decisions/NationalUnification.txt` is 1848+. No overlap.

## Chain

1. **1001100 The Carbonari** - SAR, SIC, PAP, TUS, MOD, PAR, LUC; 1821-1835, once.
   *Watch the lodges* (AI 40, consciousness +1, `liberal_agitation` in the capital)
   or *break them* (AI 60, `conservative_reaction`, militancy +1, prestige -1).
   Both set `carbonari_active`, which shortens the two risings below.
2. **1001101 Ciro Menotti's Conspiracy** - MOD, from 1830 (needs FRA's
   `july_revolution` flag or year 1831), once. *Hang Menotti* (AI 70: militancy,
   `conservative_reaction`, AUS relations) or *hesitate* (rising: consciousness +2,
   `liberal_agitation` on 739/740, sets global flag `italian_risings_1831`).
3. **1001102 Revolt in the Legations** - PAP, 1831, once; Bologna proclaims the
   United Italian Provinces. *Appeal to Vienna* (AI 80, sets `pap_called_austria`
   and fires 1001103) or *concede the Memorandum* (AI 20, `liberal_reaction`,
   militancy down, AUS relations down, FRA influence up).
4. **1001103 The Austrian Intervention** - AUS, `is_triggered_only` from 1001102,
   major + news. *Send Frimont over the Po* (AI 80: prestige +5, badboy +1,
   relations and influence with PAP/MOD/PAR, their militancy suppressed and
   `conservative_reaction` applied, sets `aus_intervened_1831`) or *let it burn*
   (prestige -5, PAP keeps `global_liberal_agitation` and militancy, FRA gains
   influence and relations in Rome).
5. **1001104 The Powers and the Legations** - ENG, FRA, RUS, PRU reaction, news
   only; *protest* or *accept the fait accompli*, AI weighted by
   `aus_intervened_1831`.

## Conventions

Flags written and read: `carbonari_active` (1-> 2,3), `italian_risings_1831`
(global, 2 -> 3), `pap_called_austria`, `aus_intervened_1831` (4 -> 5), plus the
one-shot guards `mod_menotti_resolved` and `pap_legations_revolt`. All events are
`fire_only_once`. No new pictures: `national_congress`, `streetriot`,
`DIM_pope_pius_ix`, `Oldsoldiers`, `greatpowers` already ship or are vanilla.
Suppression uses direct pop effects plus the country-scope `conservative_reaction`
because no province-scope occupation modifier with negative militancy exists in
`common/event_modifiers.txt`; `liberal_agitation` / `nationalist_agitation` are
pop_* modifiers and are used as province modifiers only.
