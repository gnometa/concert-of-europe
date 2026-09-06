# Vila-Francada and the Abrilada (1823-1826) - design

## Problem

`docs/design/1821-1836-coverage.md:38` lists "Vila-Francada / Abrilada 1823-24"
as **missing** with no file citation. Grepping the whole tree for
`vila_francada` / `abrilada` / `amarante` returns nothing, so none of it is
scripted anywhere.

What *does* exist, verified by reading the files:

- `events/PORFlavor.txt:97021-97029` - the Brazilian independence chain. 97024
  ("End of the UKPBA") is what turns **UPB into POR**; until it fires the tag is
  UPB, which is why every Portuguese event in this period is gated
  `OR = { tag = POR tag = UPB }`.
- `events/PORFlavor.txt:97030` - "Death of John VI". Trigger is `year = 1825`,
  `NOT = { year = 1836 war_with = BRZ }`, `fire_only_once = yes`, MTTH 12 months.
  It reads **no country flags at all**. Option A sets `por_charter_granted`,
  option B sets `miguelist_usurpation` (`PORFlavor.txt:1910` and `:1958`, both
  with a comment naming `PORMiguelistGVG.txt` as the reader).
- `events/PORFlavor.txt:97031` - "Pedro seeks liberal support", a greater-power
  event from 1826 that needs `POR = { government = absolute_monarchy... }`.
- `events/PORMiguelistGVG.txt:1001000-1001003` - the Miguelist / Liberal Wars,
  1826-1834. 1001000's trigger (lines 29-38) requires
  `has_country_flag = por_charter_granted` and `NOT` of `miguelist_usurpation` /
  `por_cortes_resists` / `por_charter_upheld`.

So the period 1821-1825 has a Brazilian chain and a succession chain, and
nothing at all about the collapse of the Vintista regime that produced them.
Portugal at the start date is `history/countries/UPB - Portugal-Brazil.txt`:
`government = hms_government`, `ruling_party = POR_liberal`, `wealth_voting`,
`yes_meeting`, `state_press`, `non_secret_ballots` - i.e. the constitutional
regime of 1822 is already modelled. Nothing ever takes it away; the player is a
liberal constitutional monarchy in 1825 and then, out of nowhere, is asked
whether Miguel should abrogate a constitution that was never challenged.

**Negative constraint.** This chain must never set `por_charter_granted`,
`miguelist_usurpation`, `por_cortes_resists` or `por_charter_upheld`. Those four
belong to 97030 and `PORMiguelistGVG.txt`; setting the first would fire 1001000
in 1823, setting any of the other three would lock 1001000 out permanently. The
handoff is done with new flags of this chain's own plus one edit to 97030 (see
**Handoff**).

The 1826 Carta Constitucional is therefore *not* in this chain: it is already
scripted, as 97030's option A ("Pedro will give the crown to Maria and reaffirm
the constitution") and as `PORMiguelistGVG.txt:1001000`, which is literally
titled "The Constitutional Charter and Dom Miguel's Return". This chain
deliberately stops at the Abrilada in 1824 and hands the succession and the
Carta to those two.

Provinces used, all verified against `map/definition.csv`: 518 Oporto,
519 Vila Real, 520 Covilha, 2134 Azores. 519 is the historically correct site -
the Count of Amarante's rising of February 1823 was in Tras-os-Montes; 518 and
2134 are the liberal strongholds already used as such by
`PORMiguelistGVG.txt:1001001`. No province history file is touched.

Tags referenced, all verified in `common/countries.txt`: POR (:307), UPB (:18),
ENG (:525), RUS (:526), FRA (:527), AUS (:530), SPA (:535).

## Chain - `events/PORVilaFrancadaGVG.txt`, ids 1003000-1003003

| id | who | when | options |
|---|---|---|---|
| 1003000 | POR/UPB | `year = 1823`, `NOT = { year = 1824 }`, MTTH 3mo, flag-guarded, picture `Rebellion` | A march on Tras-os-Montes (AI 55) / B amnesty (AI 30) / C purge the officer corps (AI 15) |
| 1003001 | POR/UPB | triggered 70-110 days after 1003000 - the Vila-Francada, `major`, news, picture `carlists` | A abolish the Constitution of 1822 (AI 55) / B a charter granted from the throne (AI 30) / C stand with the Cortes (AI 15) |
| 1003002 | POR/UPB | triggered 300-330 days after 1003001 - the Abrilada, `major`, news, picture `DIM_army_disintegration` | A refuge aboard the British squadron (AI 55) / B yield to the Infante (AI 30) / C try the Infante for treason (AI 15) |
| 1003003 | ENG | triggered 5 days after 1003002 A, picture `HMS_Resolute` | A guarantee the House of Braganza (AI 70) / B Lisbon must settle its own affairs (AI 30) |

Only 1003000 is self-firing. It carries `fire_only_once = yes` *and* the flag
guard `NOT = { has_country_flag = por_vintismo_challenged }`, with
`set_country_flag = por_vintismo_challenged` in all three options - the
engine-wide `fire_only_once` pitfall costs nothing here (only one tag can ever
fire it) but the flag is what actually guards it, and 97030 reads it.

The window is deliberately one year wide (`year = 1823`, `NOT = { year = 1824 }`)
rather than "1823 to 1825". With MTTH 3 months it fires with near certainty
inside 1823, and the ~420 days of scheduled follow-ups then land the Abrilada in
the first half of 1824 - comfortably before 97030's 1825 window opens. Without
the tightening the chain could straddle John VI's death.

MTTH modifiers on 1003000, each verified against an existing scripted state:
`factor = 0.5` if `FRA = { has_country_flag = one_hunderd_thousand_sons }` (the
flag, typo included, is set by `SPAFlavor.txt:37762` and cleared by
`decisions/France.txt:546`); `factor = 0.75` if SPA has been pushed back to
`absolute_monarchy` (the outcome of `SPAFlavor.txt:37763`); `factor = 0.75` if
`ruling_party_ideology = reactionary`; `factor = 0.75` if
`average_militancy = 3`. Note that `spanish_restoration`
(`decisions/SPA.txt:77`) is **not** usable here - its potential requires
`has_country_flag = king_alfonso_rules`, so it is the 1874 Bourbon Restoration,
not 1823.

## What the options do

**1003000 - The Revolt in Tras-os-Montes.** The February 1823 royalist rising.
All three options set `por_vintismo_challenged` and schedule 1003001.

- **A, march on Vila Real.** `treasury = -5000` (the band the other GVG chains
  use; far under the int32-hundredths ceiling), `prestige = 1`,
  `add_country_modifier = { name = military_strife duration = 365 }` because the
  army splits over the order. `any_owned` limited to province ids 519 and 520
  raises `militancy = 2`, `consciousness = 1` and reactionary ideology 0.10 in
  those pops. Schedules 1003001 at 90 days.
- **B, amnesty.** John VI's actual instinct. `prestige = -2`,
  `add_country_modifier = { name = coup_risk duration = 730 }`, aristocrats and
  clergymen get reactionary ideology +0.10 and `militancy = -1`, while pops in
  518 and 2134 get liberal ideology +0.05 and `consciousness = 1`. Sets
  `por_amarante_pardoned`. Schedules 1003001 at 110 days.
- **C, purge the officer corps.** The Vintista hard line. `prestige = -1`,
  `add_country_modifier = { name = military_strife duration = 730 }`, officers
  and aristocrats get `militancy = 3`, `consciousness = 2` and reactionary
  ideology +0.15. Sets `por_army_purged`. Schedules 1003001 at 70 days - the
  purge brings the crisis forward.

**1003001 - The Vila-Francada.** May 1823, Miguel's proclamation at Vila Franca
de Xira. `is_triggered_only`, so no guard flag is needed. All three options
schedule 1003002.

- **A, the Constitution is dissolved.** `government = absolute_monarchy`,
  `ruling_party_ideology = reactionary` (`POR_reactionary` exists from 1820.1.1
  in `common/countries/Portugal.txt` and `Portugal-Brazil.txt`, so the change is
  legal at this date), then `political_reform = appointed`,
  `political_reform = underground_parties`, `political_reform = state_press`,
  `political_reform = no_meeting`, `political_reform = none_voting` - in that
  order, copying 97030's option B, because `underground_parties` and the rest
  carry `allow = { NOT = { vote_franschise = none_voting } }` in
  `common/issues.txt:468-515` and `none_voting` must therefore be set last.
  `clr_country_flag = liberal_election_win`,
  `set_country_flag = reactionary_election_win` (both flags are live: POR's
  history file sets `liberal_election_win` and `PORMiguelistGVG.txt` swaps them
  the same way). `add_country_modifier = { name = conservative_reaction
  duration = 3650 }`. `add_province_modifier = { name = liberal_agitation
  duration = 1825 }` on 518 and 2134 plus liberal ideology and
  `scaled_militancy` there. `relation` AUS +15, RUS +10, FRA +10, ENG -10. Sets
  `por_absolutism_restored`. AI 55, weighted `factor = 1.5` on
  `por_amarante_pardoned` and `factor = 1.25` on
  `ruling_party_ideology = reactionary`.
- **B, a charter granted from the throne.** The commission John VI actually
  appointed and never let report. `government = prussian_constitutionalism`
  (verified in `common/governments.txt:196`),
  `ruling_party_ideology = conservative` (`POR_conservative`, 1820-1876),
  `political_reform = appointed`, `political_reform = harassment`,
  `political_reform = state_press` (an explicit no-op - POR already sits on the
  most restrictive press step and the charter branch does not loosen it; do not
  substitute `censored_press`, which in `common/issues.txt:405-424` is a step
  *towards* a free press), `political_reform = landed_voting`.
  `add_country_modifier = { name = national_instability duration = 1095 }`. Both
  wings are mildly annoyed: liberal ideology +0.05 with `scaled_militancy`
  factor 6, reactionary ideology +0.05 with `scaled_militancy` factor 6. Sets
  `por_carta_promised`. AI 30.
- **C, the King stands with the Cortes.** Counterfactual but a real player
  choice: nothing is reformed away. `prestige = -3`,
  `add_country_modifier = { name = military_strife duration = 1095 }`,
  `add_country_modifier = { name = coup_risk duration = 730 }`, reactionary pops
  get `scaled_militancy` factor 16 and aristocrats/clergymen/officers get
  `consciousness = 2`. `relation` AUS -15, RUS -15, FRA -15, ENG +10. Sets
  `por_vintismo_upheld`. AI 15, weighted `factor = 2` on `por_army_purged`.

Because Vic2 options cannot carry triggers, the fact that branch C leaves the
regime liberal is expressed only through `ai_chance` and through the state the
options leave behind - 1003002's text is written so that it reads correctly
whether the Infante is moving against a liberal Cortes or against his father's
own absolutist ministry.

**1003002 - The Abrilada.** April 1824. All three options set
`por_abrilada_done`, which is the flag 97030 waits on.

- **A, refuge aboard the British squadron.** The historical outcome: the
  diplomatic corps gets John VI onto a British warship in the Tagus and he
  dismisses and exiles his son. `prestige = -3`,
  `relation = { who = ENG value = 25 }`,
  `ENG = { diplomatic_influence = { who = THIS value = 25 } }`,
  `remove_country_modifier = coup_risk` and
  `remove_country_modifier = military_strife` (both are safe no-ops when absent;
  `PORMiguelistGVG.txt:1001002` removes modifiers unconditionally the same way),
  aristocrats/clergymen/officers get `militancy = 2` and reactionary ideology
  +0.05. Sets `por_miguel_exiled`. Fires 1003003 at Britain through
  `random_country = { limit = { tag = ENG exists = yes } country_event = { id =
  1003003 days = 5 } }`, copying 97030's `random_country` guard rather than a
  bare `ENG = { }`. AI 55, weighted `factor = 1.5` on `por_vintismo_upheld`.
- **B, yield to the Infante.** Miguel governs in his father's name.
  `prestige = -5`, `government = absolute_monarchy`,
  `ruling_party_ideology = reactionary`, the same five `political_reform` lines
  in the same order, `add_country_modifier = { name = conservative_reaction
  duration = 3650 }`, `add_country_modifier = { name = national_instability
  duration = 1825 }`, `relation` ENG -25 and FRA -15,
  `add_province_modifier = { name = liberal_agitation duration = 1825 }` on 518,
  519 and 2134 with liberal ideology +0.25 and `scaled_militancy` factor 12
  there. Sets `por_miguel_ascendant`. AI 30, weighted `factor = 1.5` on
  `por_absolutism_restored`.
- **C, try the Infante for treason.** The harshest branch: Miguel is not merely
  sent abroad but arraigned. `prestige = 3`, `add_country_modifier = { name =
  national_instability duration = 1095 }`, aristocrats/clergymen/officers get
  `militancy = 4`, `consciousness = 2` and reactionary ideology +0.10, everyone
  else gets liberal ideology +0.05 and `militancy = -1`,
  `relation = { who = AUS value = -25 }` because Vienna is where Miguel actually
  went. Sets `por_miguel_exiled`. No British event - the court did this without
  the squadron. AI 15, weighted `factor = 2` on `por_vintismo_upheld` and
  `factor = 0.25` on `por_absolutism_restored`.

**1003003 - The Squadron in the Tagus.** ENG only, `is_triggered_only`, FROM is
Portugal (the `ZollvereinGVG.txt` pattern).

- **A, guarantee the House of Braganza.** `prestige = 2`, `treasury = -5000`,
  `relation = { who = FROM value = 50 }`,
  `diplomatic_influence = { who = FROM value = 40 }`,
  `relation = { who = AUS value = -10 }`, and
  `FROM = { prestige = 2 set_country_flag = por_british_guarantee }`. AI 70,
  `factor = 0.5` if `war = yes`.
- **B, Lisbon must settle its own affairs.** `prestige = -1`,
  `relation = { who = FROM value = -10 }`, and
  `FROM = { add_country_modifier = { name = coup_risk duration = 730 } }`. AI 30.

## Flags - every flag has a reader

| flag | set by | read by |
|---|---|---|
| `por_vintismo_challenged` | 1003000 A/B/C | 1003000 trigger; **97030 trigger (handoff edit 1)** |
| `por_amarante_pardoned` | 1003000 B | 1003001 `ai_chance` |
| `por_army_purged` | 1003000 C | 1003001 `ai_chance` |
| `por_absolutism_restored` | 1003001 A | 1003002 `ai_chance` |
| `por_carta_promised` | 1003001 B | 1003002 `ai_chance` |
| `por_vintismo_upheld` | 1003001 C | 1003002 `ai_chance` |
| `por_abrilada_done` | 1003002 A/B/C | **97030 trigger (handoff edit 1)** |
| `por_miguel_exiled` | 1003002 A, C | **97030 `ai_chance` (handoff edit 2)** |
| `por_miguel_ascendant` | 1003002 B | **97030 `ai_chance` (handoff edit 2)** |
| `por_british_guarantee` | 1003003 A (on FROM) | **97030 `ai_chance` (handoff edit 2)** |

`reactionary_election_win` / `liberal_election_win` are pre-existing flags of the
PDM election system and are only swapped here, not introduced.

## Handoff - two edits to `events/PORFlavor.txt` 97030

Both are additive; neither removes or rewrites anything. They are the only
legacy edits this chain needs, and they should be applied together - the second
is what gives three of this chain's flags a reader.

**1. Sequencing gate (required).** Added to 97030's `trigger` block, after
`NOT = { year = 1836 war_with = BRZ }`:

```
		OR = {
			NOT = { has_country_flag = por_vintismo_challenged }
			has_country_flag = por_abrilada_done
		}
```

Read as: if the Vila-Francada chain never started, behave exactly as today; if
it started, wait until the Abrilada has resolved. This cannot deadlock - 1003002
sets `por_abrilada_done` in every option, and 97030's window runs to 1836.

**2. AI weighting (required for flag hygiene).** Four `modifier` blocks inside
97030's two existing `ai_chance` blocks, which today are a bare `factor = 80`
and `factor = 20`:

```
		ai_chance = {
			factor = 80
			modifier = { factor = 1.5 has_country_flag = por_miguel_exiled }
			modifier = { factor = 1.5 has_country_flag = por_british_guarantee }
		}
```

on option A ("Pedro will give the crown to Maria"), and

```
		ai_chance = {
			factor = 20
			modifier = { factor = 3 has_country_flag = por_miguel_ascendant }
			modifier = { factor = 0.25 has_country_flag = por_miguel_exiled }
		}
```

on option B ("Miguel will become king"). If only edit 1 lands,
`por_miguel_exiled`, `por_miguel_ascendant` and `por_british_guarantee` become
set-but-never-read and `refcheck flags` will name all three.

Nothing is changed in `PORMiguelistGVG.txt`. 1001000 continues to key off
`por_charter_granted`, which only 97030 grants.

## New modifiers

**None.** Everything this chain applies already exists in
`common/event_modifiers.txt` and is already localised (`text.csv` /
`00_PDM_events.csv`, checked with `modcheck loc-find`): `military_strife`
(:1686), `coup_risk` (:1678), `national_instability` (:2017),
`conservative_reaction` (:81), `liberal_agitation` (:19, province scope). No
`docs/design/_pending/` file is produced.

`reactionary_stronghold` (:2280) was rejected deliberately: it is owned by the
dynamic system in `events/Ideology_Strongholds.txt`, which adds and removes it
on its own schedule, so hand-placing it would fight that system. The reactionary
north is expressed with direct pop ideology and militancy effects instead.
`carlist_sympathies` (:2024) was rejected as Spanish-specific (icon 91) and far
too heavy (`local_RGO_throughput -0.50`) for a provincial rising.

## Localisation - `localisation/GVG_vilafrancada.csv`

New file, created and written only through
`python scripts/modcheck.py loc-add GVG_vilafrancada.csv KEY "text"` (the
Edit/Write hook blocks `.csv` because those tools save UTF-8). ASCII only, so
"Tras-os-Montes", "Vila Franca de Xira" and "Joao VI" are spelled without
diacritics. 27 keys:

- 1003000: `EVTNAME1003000`, `EVTDESC1003000`, `EVTOPTA/B/C1003000`
- 1003001: the same five, plus `EVTNAME1003001_NEWS_TITLE` and
  `EVTDESC1003001_NEWS_LONG` / `_NEWS_MEDIUM` / `_NEWS_SHORT`
- 1003002: the same nine
- 1003003: `EVTNAME1003003`, `EVTDESC1003003`, `EVTOPTA/B1003003`

No modifier or country keys are needed.

## Pictures

Existing art only; nothing is downloaded or created, and
`python scripts/gfxtool.py missing` prints nothing today and must keep doing so.

| event | `picture` | where it lives |
|---|---|---|
| 1003000 | `Rebellion` | vanilla only: `D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\Rebellion.tga` |
| 1003001 | `carlists` | mod: `CoE_RoI_R/gfx/pictures/events/carlists.tga` (already the Iberian legitimist picture, used by 97030 and 1001000) |
| 1003002 | `DIM_army_disintegration` | mod: `CoE_RoI_R/gfx/pictures/events/DIM_army_disintegration.tga` (shipped by the DIM submod, currently referenced by no event) |
| 1003003 | `HMS_Resolute` | mod: `CoE_RoI_R/gfx/pictures/events/HMS_Resolute.tga` |

## Risks

- **Racing 97030.** The single largest risk, and the reason for both the
  one-year window on 1003000 and the handoff gate. If the gate is not applied, a
  late 1003000 can put the Abrilada after John VI is already dead.
- **1003001 branch C leaves a liberal Portugal into 1826.** 97031 then never
  fires (it needs `POR = { government = absolute_monarchy }`) and 97030 option A
  hands `por_charter_granted` to a country that already has a constitution. That
  is a coherent counterfactual, not a break: 1001000 still fires in 1826 and
  still offers the Miguelist usurpation. It is priced at AI 15 for that reason.
- **~~97030 option A does not restore a constitutional government.~~ Resolved by
  event 1003004 (review pass 2026-09-06).** Leaving it unresolved made the
  liberal ending mechanically identical to the reactionary one and killed every
  later `hms_government`-gated PORFlavor event (97000 Maria da Fonte, 97001,
  97003, 97020). The fix is a new event in this file rather than an
  unconditional effect block on 97030 option A, because 97030 option A also
  fires on the 1003001-C branch where POR is still `hms_government` with
  `wealth_voting`/`non_secret_ballots`: unconditional reform sets there would
  *demote* the branch that defended the constitution.

  1003004 "The Carta Constitucional" fires from 1825 on `por_charter_granted`
  only while POR is `absolute_monarchy*` or `prussian_constitutionalism*` and
  has not taken `miguelist_usurpation`; it is guarded by `por_carta_restored`,
  set in both options. Both options set `government = hms_government` - option A
  the court Carta (`landed_voting`, `harassment`, `censored_press`,
  `yes_meeting`, conservative ruling party), option B the old franchise
  (`wealth_voting`, `state_equal_weight`, `non_secret_ballots`, liberal ruling
  party, `liberal_reaction`). `mean_time_to_happen = 2 months` puts it ahead of
  1001000 (1826, 5 months) in the common case; if 1001000 wins the race and the
  usurpation is chosen, the way back is 1001002 option A as before.
- **97031 gate.** Making POR absolutist from 1823 newly opened PORFlavor 97031
  ("Pedro seeks liberal support", `money = -50000` for every liberal European
  GP) on branches with no Miguelist civil war. The `POR = { }` block now also
  requires `has_country_flag = miguelist_usurpation`, which is exactly the state
  97031 could reach before this chain existed. `NOT = { has_country_flag =
  por_absolutism_restored }` would have been the weaker gate: 1003002 option B
  (Miguel ascendant) never sets that flag.
- **97030 ai_chance on the Miguel-ascendant branch.** Option B's
  `por_miguel_ascendant` weight is 8 (was 3) and option A now carries a matching
  `factor = 0.25`, so a Portugal where Miguel already governs continues into
  `miguelist_usurpation` (~89%) instead of into 1001000's "return from exile in
  Vienna" text.
- **Pre-existing, not touched:** `PORMiguelistGVG.txt:57` uses
  `political_reform = party_appointed`, and `party_appointed` carries
  `allow = { always = no }` in `common/issues.txt:339`. That predates this chain;
  this chain uses `appointed`, as 97030 does.
- **Province ids** are the historical crash source in this repo. All four used
  here are listed in the Problem section and re-checked by `modcheck provinces`
  and the PostToolUse hook. No file under `history/provinces/` is created, moved
  or renamed.
- **UPB vs POR.** Every trigger uses `OR = { tag = POR tag = UPB }`. If a game
  somehow keeps the union past 1823 the chain still runs on UPB, which is
  correct - the Vila-Francada happened while Brazil was still nominally in the
  union.
- **Event load.** Three POR popups between 1823 and 1824, two of them
  `major = yes`, on a tag whose only other content in that window is the
  Brazilian chain. `audit_pacing.py` should be re-run after the file lands.
