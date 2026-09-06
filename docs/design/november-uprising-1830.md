# The November Uprising (1830-1832) — design

## Problem

Unlike most 1821-1836 gaps, this one is half-filled already. `events/RUSFlavor.txt:849-1140`
carries a four-event PDM chain, not the "single event gated `year = 1828`" the backlog
describes:

- **95070** (RUS, `year = 1830 month = 10`, `NOT = { year = 1832 }`, `CPL = { vassal_of = THIS }`,
  `NOT = { has_country_flag = cpl_uprising }`) — the outbreak. One option, no agency:
  sets `cpl_uprising`, forces `ruling_party_ideology = reactionary`, puts
  `nationalist_agitation` (730 d) on every RUS province that is `culture = polish` /
  `culture = lithuanian` / `is_core = POL` / `is_core = LIT`, `release_vassal = CPL`,
  relations -200, then `war = { target = CPL attacker_goal = annex_core_country }`.
- **95071** (CPL, triggered) — one option, `any_pop = { militancy = -6 }`, prestige +5, then
  fires 95072 at every greater power except RUS and TUR.
- **95072** (GP, triggered) — three options: back the Tsar / diplomatic support / military
  support (`treasury = 10000` to CPL).
- **95073** (RUS, 1831-1835, `fire_only_once`, needs `cpl_uprising`, `NOT = { war_with = CPL }`)
  — the Organic Statute. A: `inherit = CPL`, `nationalist_agitation` 3650 d on POL/CPL cores,
  `nicholas_reaction` 3650 d (guarded by `NOT = { has_country_modifier = nicholas_reaction }`),
  polish pops consciousness +2. B: restore the charter, prestige -10, militancy -3.

So the **outbreak, the Great Power reaction and the Organic Statute already exist and are not
re-scripted here**. What is missing is everything between them and after them: the Polish side
has no politics at all (95071 is a one-button notice), there is no dethronement of Nicholas, no
Ostroleka, no fall of Warsaw, no Prussian reaction, and no Great Emigration. This chain adds
exactly those, hanging off `RUS = { has_country_flag = cpl_uprising }` so it can never fire
without 95070 and can never duplicate it.

Verified starting state: `history/diplomacy/PuppetStates.txt:80-86` makes CPL a vassal of RUS
from 1815.9.1 to 1917.11.7, so CPL exists and is a vassal at the 1821.9.1 start (the only
bookmark, `common/bookmarks.txt`). CPL's capital is 706 Warsaw
(`history/countries/CPL - Congress Poland.txt:1`); ruling party "Moderate Faction", ideology
conservative (`common/countries/Congress Poland.txt:4-9`). CPL owns 13 provinces: 362, 706, 707,
708, 709, 710, 711, 712, 713, 715, 716, 717, 961. Posen 699 is `owner = PRU` with
`add_core = PZN` and `add_core = POL`, as are 700 Bromberg and 701 Gniezno. RUS owns the
Lithuanian cores 360, 361, 363, 364, 365. All ids re-checked against `map/definition.csv`. Only
706 is named literally in the script; the Posen and Lithuanian provinces are reached by
`is_core = POL` / `is_core = PZN` / `is_core = LIT` inside `any_owned`, which
`audit_owner_scope` can confirm actually match.

`events/POLflavor.txt` is a *restored-Poland* chain (99946-99957: choosing a king, union with
Saxony, a Habsburg or Hohenzollern candidacy; 99800 integrates Krakow), fired from elsewhere and
irrelevant before POL exists. No overlap. `events/LiberalRevolutions.txt` starts at `year = 1840`
and `year = 1847` (10000, 10001) and its 10050/10051 pair is gated on
`has_country_flag = liberal_revolution_fired`. No overlap. Grepping the tree for `ostroleka`,
`november_uprising` and `emigration` (as anything but a picture name) returns nothing.

## Chain — `events/POLNovemberGVG.txt`, ids 1002600-1002605

| id | who | when | options |
|---|---|---|---|
| 1002600 | CPL | `RUS = { has_country_flag = cpl_uprising }`, `year = 1830`, `NOT = { year = 1833 }`, `NOT = { has_country_flag = november_dictatorship }`, MTTH 1 mo | A Chlopicki's dictatorship (AI 35) / B the Patriotic Society arms the nation (AI 65) |
| 1002601 | CPL | triggered, +57 d from A, +30 d from B — the Act of Dethronement, 25 Jan 1831, `news` | A depose Nicholas (AI 85) / B leave the throne vacant and court Europe (AI 15) |
| 1002602 | PRU | triggered from 1002601 (+20 d / +40 d) — the Posen cordon | A seal the frontier and supply the Tsar (AI 60) / B strict neutrality (AI 30) / C look away at Kalisz (AI 10) |
| 1002603 | CPL | `war_with = RUS`, `has_country_flag = november_dethronement`, `NOT` ostroleka/warsaw flags, `year = 1831`, `NOT = { year = 1833 }`, MTTH 2 mo — Ostroleka | A save the cadre (AI 60) / B throw in the last reserves (AI 40) |
| 1002604 | CPL | `war_with = RUS`, `has_country_flag = november_dethronement`, `NOT = { has_country_flag = november_warsaw_fallen }`, `year = 1831`, `NOT = { year = 1834 }`, `RUS = { controls = 706 }`, MTTH 1 mo, `news` — the fall of Warsaw | A Krukowiecki treats with Paskevich (AI 70) / B the Sejm withdraws to Plock (AI 30) |
| 1002605 | RUS | `has_country_flag = cpl_uprising`, `NOT = { war_with = CPL }`, 95073's `OR = { NOT = { exists = CPL } / CPL = { vassal_of = THIS } / AND = { exists = CPL truce_with = CPL } }` victory gate, `year = 1831`, `NOT = { year = 1836 }`, `NOT = { has_country_flag = great_emigration }`, MTTH 3 mo — the Great Emigration | A confiscations and courts-martial (AI 75) / B let them go, amnesty at home (AI 25) |

**1002600.** Option A gives Chlopicki dictatorial powers and opens talks: `prestige = -1`,
`relation = { who = RUS value = 50 }`,
`add_country_modifier = { name = military_strife duration = 180 }` (the December demobilisation:
leadership -0.5, land organisation -0.25), aristocrats and officers militancy -2, artisans and
clergymen consciousness +1, then `country_event = { id = 1002601 days = 57 }`. Option B is the
national levy: `add_country_modifier = { name = small_country_draft duration = 730 }`
(mobilisation size +0.25 at four times the economic impact), `treasury = -1000` for the plate
collection and the national loan, all pops militancy +2 consciousness +1, prestige +2, and
`country_event = { id = 1002601 days = 30 }`. Both set `november_dictatorship`, so the event
cannot re-fire, plus `november_chlopicki` / `november_levy`, which 1002603's MTTH reads.

**1002601.** Option A passes the act: prestige +5, pops militancy -3 consciousness +2, and the
spring risings east of the Bug —
`RUS = { any_owned = { limit = { is_core = LIT } add_province_modifier = { name = patriot_uprising duration = 365 } } }`.
`patriot_uprising` rather than `nationalist_agitation` deliberately: 95070 already put
`nationalist_agitation` on those same provinces for 730 days, and identical modifiers stack.
Option B is Czartoryski's line, the throne declared vacant and offered abroad: prestige +1,
`any_greater_power = { limit = { NOT = { tag = RUS } NOT = { tag = TUR } } relation = { who = CPL value = 20 } }`,
aristocrats and bureaucrats militancy -1, soldiers and artisans militancy +1 consciousness +1,
and `add_country_modifier = { name = fight_the_power duration = 365 }` for the lost momentum — a
different modifier from A's branch precisely so nothing stacks with 1002600 A's
`military_strife`. Both set `november_dethronement`; B also sets `november_crown_offered`, which
1002602 reads. Both fire 1002602 through
`random_country = { limit = { tag = PRU exists = yes } country_event = { id = 1002602 days = N } }`
— the `random_country` / `limit = { tag = X }` idiom copied from 95070's own effect block, so a
partitioned PRU is a clean no-op rather than a scope error.

**1002602.** Berlin's real decision was whether the Posen corps was a cordon or a springboard.
Option A seals the frontier and opens the magazines: `treasury = -2000` for mobilising IV and V
corps, `relation = { who = RUS value = 50 }`, `relation = { who = CPL value = -50 }`, and
`any_owned = { limit = { is_core = PZN } add_province_modifier = { name = nationalist_agitation duration = 730 } }`
— Posen's Poles pay for the cordon. The limit is `is_core = PZN` alone, not `OR = { is_core = POL is_core = PZN }`:
ten PRU provinces carry a POL core (3258 Marienwerder, 684 Oppeln, 685 Kattowitz, 690 Danzig,
691 Tuchel, 694 Torun, 696 Allenstein, 699 Posen, 700 Bromberg, 701 Gniezno) but only 699/700/701
carry PZN, and only those three are the Grand Duchy the event text is about. Option B is strict
neutrality: prestige +1, RUS -10, CPL +10, the same province modifier at 365 days. Option C lets
powder and volunteers cross at Kalisz:
`relation = { who = RUS value = -50 }`, `badboy = 1`, `prestige = -2`,
`random_country = { limit = { tag = CPL exists = yes } war_exhaustion = -2 relation = { who = PRU value = 50 } }`,
the same modifier at 1095 days — the largest of the three, because arming the insurgents is what
actually inflames Posen; and `set_country_flag = posen_smuggling`, read by 1002604's `ai_chance`. A's `ai_chance` is
weighted up by `government = absolute_monarchy` (PRU's start government,
`history/countries/PRU - Prussia.txt:6`) and by `alliance_with = RUS`; C is zeroed by
`alliance_with = RUS` and weighted up by `CPL = { has_country_flag = november_crown_offered }`.

**1002603.** Ostroleka was a defeat either way, so the choice is what to spend. Option A saves
the cadre: prestige -3, `war_exhaustion = 3`, soldiers militancy +1, and
`any_owned = { add_province_modifier = { name = war_torn duration = 730 } }`. Option B feeds in
the reserves: prestige +1, `war_exhaustion = 6`, all pops militancy +2,
`add_country_modifier = { name = military_collapse duration = 730 }` (org regain and land
organisation -0.33), and
`random_country = { limit = { tag = RUS exists = yes } war_exhaustion = 2 prestige = -1 }` —
Diebitsch's army was wrecked too, and cholera finished him within a month. Both set
`november_ostroleka`. Neither branch touches `military_strife`, so nothing stacks with 1002600 A.

**1002604.** Gated on Warsaw actually having fallen (`RUS = { controls = 706 }`), so a CPL that is
winning never sees it. Its trigger is spelled out rather than inherited from 1002603: it must *not*
carry 1002603's `NOT = { has_country_flag = november_ostroleka }` clause, which would make the fall
of Warsaw reachable only in games where Ostroleka never happened. Option A capitulates: prestige -5, pops militancy -2, and
`random_country = { limit = { tag = RUS exists = yes } end_war = CPL create_vassal = CPL war_exhaustion = -3 set_country_flag = november_capitulation }`.
The re-vassalisation matters mechanically as well as historically: `end_war` explicitly does not
create a truce (`docs/wiki/list-of-effects.md:252`), and 95073 needs CPL to be non-existent, a
vassal, or under truce, so a bare `end_war` would strand the Organic Statute in every game where
the player chooses to surrender. `create_vassal` "makes the specified country a vassal of the
scoped country, even if they are already a vassal" (`list-of-effects.md:249`). Option B fights on
from Plock: prestige +2, `war_exhaustion = 5`, pops militancy +3 consciousness +2,
`any_owned = { add_province_modifier = { name = patriot_uprising duration = 730 } }`,
`military_collapse` for 365 days wrapped in the same
`random_owned = { limit = { owner = { NOT = { has_country_modifier = military_collapse } } } owner = { add_country_modifier = ... } }`
guard used for `nicholas_reaction` below, because 1002603 B may already have granted it for 730
days; and RUS war exhaustion +2. The engine war continues and the `annex_core_country` CB
resolves it. B's `ai_chance` is doubled
by `PRU = { has_country_flag = posen_smuggling }`. Both set `november_warsaw_fallen`.

**1002605.** Self-firing on RUS rather than triggered from 1002604, because CPL is a
thirteen-province AI facing an annexation CB and is usually gone before the chain reaches Warsaw;
keying the closing beat to `cpl_uprising` + `NOT = { war_with = CPL }` makes it fire however the
war ended — but only once Russia has actually won, so the trigger carries 95073's own
`OR = { NOT = { exists = CPL } CPL = { vassal_of = THIS } AND = { exists = CPL truce_with = CPL } }`
gate. Without it an outright Polish victory - CPL alive, independent and not even under truce -
satisfies `NOT = { war_with = CPL }`, and Russia would collect the confiscation payout for
losing. A white peace still passes the new gate, because it leaves a truce; that is exactly how
95073 behaves.
Option A confiscates: prestige +2, `treasury = 5000` from sequestrated estates, polish
pops consciousness +2 militancy +1,
`any_country = { limit = { OR = { tag = FRA tag = ENG } exists = yes } relation = { who = RUS value = -25 } }`.
It deliberately does **not** apply `nicholas_reaction`: 95073 owns that consequence for 3650
days in the same window and at MTTH 3 mo on the same tag, so a copy here (even behind the
`NOT = { has_country_modifier = ... }` guard) would win the race roughly half the time and
silently shorten the Organic Statute's reaction. Option B lets the emigres go and
amnesties those who stayed: prestige -2, `treasury = -2000`, polish pops militancy -4
consciousness -1, FRA and ENG relations +10. A's `ai_chance` is weighted up by
`has_country_flag = november_capitulation` — a hard-won capitulation invites reprisals. No
`any_owned` block touches CPL's old provinces here, because whether RUS owns them yet depends on
when 95073's `inherit` has landed.

## New modifiers

None. The chain reuses `military_strife`, `small_country_draft`, `fight_the_power` and
`military_collapse` (country) and `patriot_uprising`, `nationalist_agitation` and `war_torn`
(province), all defined in `common/event_modifiers.txt` and all already localised
(`00_PDM_events.csv`, `00_PDM_misc.csv`, `00_CoE_RoI_definitions.csv`). `nicholas_reaction`
(`event_modifiers.txt:3522`) is left entirely to 95073.
`rights_suspended` was considered and rejected: `decisions/Political.txt:272` gates a player
decision on `NOT = { has_country_modifier = rights_suspended }`, so granting it by event would
silently disable that decision for five years.

## Localisation

New file `localisation/GVG_november.csv`, written only through
`python scripts/modcheck.py loc-add GVG_november.csv KEY "text"`. Keys:
`EVTNAME/EVTDESC/EVTOPTA/EVTOPTB` for 1002600, 1002601, 1002603, 1002604 and 1002605;
`EVTNAME/EVTDESC/EVTOPTA/EVTOPTB/EVTOPTC` for 1002602; and the news keys
`EVTNAME1002601_NEWS_TITLE` plus `EVTDESC1002601_NEWS_LONG/MEDIUM/SHORT`, and the same four for
1002604 — 33 keys. ASCII only, so "Chlopicki", "Ostroleka", "Krukowiecki", "Lodz" and "emigres"
go in unaccented. No modifier names are added; all seven reused modifiers are already localised.

## Pictures

No new art. Verified present in `CoE_RoI_R/gfx/pictures/events/`: `streetriot` (1002600, the
Belweder night), `polski_sejm` (1002601, the Sejm; already used by `POLflavor.txt`) and
`slaughter` (1002604, the storming of Wola). Verified present in the vanilla folder
`D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\`: `patrol.tga` (1002602),
`Artillery.tga` (1002603) and `emigration.tga` (1002605).
`python scripts/gfxtool.py missing` is currently silent and must stay so.

## Risks

- **The entry gate depends on 95070 actually producing a war.** 95070 calls `release_vassal = CPL`
  on a CPL that already exists as a vassal and then declares war in the same option block.
  `list-of-effects.md:259` confirms `release_vassal` frees an existing vassal, but PDM wrote that
  option for a start where CPL did not yet exist, and the release-then-declare sequence has never
  been observed in this repo. 1002600 therefore gates on the `cpl_uprising` flag and the year
  window only, never on `war_with = RUS`, so the political half of the chain survives even if the
  war never materialises. 1002603 and 1002604 do require `war_with = RUS`; if 95070's war fails,
  those two silently do not fire and 1002605 still closes the chain.
- **CPL is short-lived.** Thirteen provinces against Russia with an `annex_core_country` CB
  usually means annexation within a year, so Ostroleka (MTTH 2 mo) and the fall of Warsaw may both
  be skipped in an AI game. That is exactly why 1002605 is self-firing on RUS.
- **A victorious CPL skips the closing events by design.** A player holding Warsaw never sees
  1002604, and 1002605 does not fire either: its victory gate requires CPL to be gone, a
  vassal, or under truce. A surviving independent Poland simply ends the chain at 1002603.
- **Modifier stacking** is the failure mode this chain is most exposed to, because 95070 and 95073
  already blanket the same provinces and the same country. Every reuse above is either a modifier no
  other event in the window applies, or is wrapped in the `NOT = { has_country_modifier = X }` guard
  (`military_collapse` on the 1002603 B -> 1002604 B path). Run
  `refcheck modifiers` and `audit_events` after the script lands.
- **1002605 and 95073 are both MTTH 3 mo on RUS after the war.** Either can fire first, so no
  effect either one applies may depend on the other having gone first. That is why 1002605 A
  applies no `nicholas_reaction` at all: an ordering-dependent 1825 vs 3650 day reaction is
  invisible to the player and to every static check.
- `war_torn` and `military_collapse` are defined in `common/event_modifiers.txt` but used nowhere
  else in the tree, so their keys have never been exercised by the engine in this mod.
- All ten country flags this chain sets (`november_dictatorship`, `november_chlopicki`,
  `november_levy`, `november_dethronement`, `november_crown_offered`, `posen_smuggling`,
  `november_ostroleka`, `november_warsaw_fallen`, `november_capitulation`, `great_emigration`)
  are read somewhere within it, so `refcheck flags` should stay clean.
- The 1836 history block of `history/countries/RUS - Russia.txt:100` presets `cpl_uprising`. The
  mod ships only the 1821 bookmark, but every *self-firing* event here (1002600, 1002603, 1002604,
  1002605) carries a `NOT = { year = 1833 }`, `NOT = { year = 1834 }` or `NOT = { year = 1836 }`
  upper bound, so a later start date could not replay the chain. 1002601 and 1002602 are
  `is_triggered_only` and need no bound.
