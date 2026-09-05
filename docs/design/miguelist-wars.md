# Miguelist / Portuguese Liberal Wars (1826-1834) - design

## Problem

`docs/design/1821-1836-coverage.md` line 37: the Portuguese chain stops at
`events/PORFlavor.txt:97030` (Death of John VI, 1825). Everything after it -
the Constitutional Charter of 1826, Dom Miguel's usurpation in 1828, the
liberal government-in-exile on Terceira, Pedro's landing at Mindelo (1832) and
the convention of Evora Monte (26 May 1834) - is missing. 97031 already exists
(a great power offers Pedro support once POR is an `absolute_monarchy`), but
nothing ever puts POR into that state after 1826, so it is nearly dead script.

Tag: after Brazilian independence 97024 does `change_tag = POR`, and 97030 is
already gated `tag = POR`. This chain is therefore **POR-only**; UPB never sees
it, which also satisfies the coverage note "only fire once UPB has lost Brazil".

## Hook into 97030

97030 set no flags, so its two outcomes were unobservable. Two
`set_country_flag` lines were added, nothing else:

- option A (Pedro crowns Maria, keeps the constitution) -> `por_charter_granted`
- option B (Miguel is made king at once) -> `miguelist_usurpation`

## Chain (`events/PORMiguelistGVG.txt`, ids 1001000-1001003)

| id | when | options |
|---|---|---|
| 1001000 The Constitutional Charter and Dom Miguel's Return | POR, 1826+, `por_charter_granted`, still an `hms_government*`, `fire_only_once`, MTTH 5 months, major + news | A accept the coup (ai 60): `miguelist_usurpation`, `government = absolute_monarchy`, reactionary ruling party (`POR_reactionary` is valid from 1820), none_voting / party_appointed / no_meeting / state_press / underground_parties, `conservative_reaction` 10 y + `national_instability` 5 y, liberal militancy in Oporto/Vila Real/Covilha/Azores, ENG and BRZ relations down / B the Cortes resists (ai 40): `por_cortes_resists`, keeps hms_government and the liberal party, reactionary militancy up, `national_instability` 3 y |
| 1001001 The Liberals at Terceira | POR, 1829+, `miguelist_usurpation`, not yet `por_liberal_war`, `fire_only_once`, MTTH 4 months | A blockade the islands (ai 55): heavier liberal militancy + `liberal_agitation` on 518/519/2134, prestige -3 / B let the exiles rot (ai 45): lighter version, no province modifier. Both set `por_liberal_war` |
| 1001002 Evora Monte | POR, 1833+ (not past 1838), `por_liberal_war`, `fire_only_once`, MTTH 4 months, major + news; `immediate` clears `por_liberal_war` | A Miguel abdicates (ai 70): clears `miguelist_usurpation`, sets `por_charter_upheld`, restores hms_government + liberal party + wealth_voting / state_equal_weight / yes_meeting / non_secret_ballots / censored_press, prestige +10, ENG relation +50 and influence, removes the reaction modifiers and `liberal_agitation` / B Miguel holds (ai 30): absolutism stays, prestige -10, ENG/FRA/SPA relations -50, `national_instability` refreshed 10 y, liberal militancy up |
| 1001003 The Miguelite Revolt | POR, 1828+, `por_cortes_resists`, `fire_only_once`, MTTH 6 months; `immediate` clears `por_cortes_resists` | A the Charter holds (ai 60): `por_charter_upheld`, prestige +5, `liberal_reaction` 5 y / B the army goes over to Miguel (ai 40): the same absolutist package as 1001000-A, sets `miguelist_usurpation` and so feeds 1001001 |

The civil war itself is **not** scripted as a `release` + `war`, following the
Carlist model in `events/SPAFlavor.txt` (37711/37712): the events only move pop
ideology and militancy and drop province modifiers, and the engine's own rebel
system fights the war. There is no `SPC`-style liberal tag for Portugal, and
inventing one would need a new tag, flags and cores; the Carlist pattern needs
none of that.

## Deliberate limits

- **No new modifiers**: `conservative_reaction`, `liberal_reaction`,
  `national_instability` and `liberal_agitation` all already exist in
  `common/event_modifiers.txt`. "International isolation" for 1001002-B is
  expressed as relation and prestige penalties plus `national_instability`
  rather than a new modifier.
- **No new pictures**: `carlists`, `streetriot` and `deliberation` ship in the
  mod; `Monarchy` falls back to vanilla.
- **No province edits, no war, no tag switch, no start-state change.** Provinces
  touched are only 518, 519, 520, 521 and 2134 (all Portuguese-owned in 1821;
  2136 Canary Islands is deliberately not used even though `POR_2134` contains it).
- **Every new flag is both written and read**: `por_charter_granted` (97030-A ->
  1001000), `miguelist_usurpation` (97030-B / 1001000-A / 1001003-B -> 1001001,
  1001002), `por_cortes_resists` (1001000-B -> 1001003), `por_liberal_war`
  (1001001 -> 1001002), `por_charter_upheld` (1001002-A / 1001003-A -> guards on
  1001000 and 1001002).
- 97031 is left untouched: it keys on `government = absolute_monarchy*`, which
  1001000-A and 1001003-B now actually produce.
