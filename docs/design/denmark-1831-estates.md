# Bankruptcy and the Provincial Estates (1821-1836) - design

## Problem

`docs/design/1821-1836-coverage.md:43` lists DEN as **0 events**, with
"Aftermath of the 1813 bankruptcy, 1831 provincial estates" as missing. That is
correct. `events/DANFlavor.txt` is the only Danish flavour file and every event
in it is dated 1848 or later (36204 is 1848, the rest 1870-1898 -
`grep "year = 18" events/DANFlavor.txt`). `events/ScandinavianEvents.txt`
49501-49510 is the Kalmar/SCA machinery, all `is_triggered_only` off
`decisions/SCA.txt:115 reform_kalmar`, which needs `is_greater_power = yes` and
`state_n_government = 1` - unreachable for DEN before 1836.
`events/SWHFlavor.txt` 90050 is gated on `year = 1848`. Grepping the tree for
`lornsen`, `statsbankerot`, `staender`, `rigsbank` and `roskilde` returns
nothing. So the whole 1821-1836 window for Denmark is empty.

Two facts about the 1821 setup shape everything below, and both were verified by
reading the files:

**DEN does not own Schleswig or Holstein.** 369 Kiel
(`history/provinces/germany/369 - Kiel.txt`), 370 Flensburg and 371 Abenra
(`history/provinces/scandinavia/`) are all `owner = SWH`. SWH is a vassal of DEN
(`history/diplomacy/PuppetStates.txt:2`, 1773-1864) and in personal union with
it (`history/diplomacy/Unions.txt:2`, 1460-1863); the SWH capital is 369 and its
primary culture is `north_german`, with `culture = danish` and `culture = frisian`
accepted (`history/countries/SWH - Schleswig-Holstein.txt:1-4`). Consequences:
a DEN-scope `any_owned = { limit = { province_id = 369 } }` is exactly the silent
no-op `audit_owner_scope.py` exists to catch, so every Schleswig/Holstein effect
in this chain goes through `SWH = { any_owned = { ... } }`; and the Lornsen event
is triggered on `exists = SWH` plus `SWH = { vassal_of = THIS }`, the pattern
already used at `events/SWHFlavor.txt:22-27`. The separate `SCH` and `HOL` tags
exist (`common/countries.txt:334`, `:324`) but own nothing at 1821 and are
**not** touched: a consultative estate is not a partition.

**There are no `aristocrats` and effectively no `farmers` pops in this mod at
the 1821 start.** Counting every top-level pop block in
`history/pops/1821.9.1/*.txt` gives artisans 5843, labourers 5523, clergymen
4604, soldiers 1581, capitalists 1446, bureaucrats 871, officers 544, slaves 467,
craftsmen 92, clerks 52, **farmers 2, aristocrats 0** - tree-wide, not just in
Denmark. 366 Aarhus holds artisans, bureaucrats, clergymen and labourers only;
372 Copenhagen adds capitalists, clerks, officers and soldiers. So an
`aristocrats = { }` or `farmers = { }` block anywhere in this chain would be a
dead site. The Danish landowner (godsejer) grievance is therefore expressed
through the `rich_strata` / `middle_strata` / `poor_strata` scopes, which stay
correct if the RGO rework later promotes pops. Those strata scopes are absent
from `docs/wiki/list-of-scopes.md` but are documented in
`docs/wiki/list-of-effects.md:130` and used throughout the tree
(`events/ACW.txt:625,1317,1328`, `events/CHIFlavor.txt:594`).

The DEN start state (`history/countries/DEN - Denmark.txt`): capital 372,
`government = absolute_monarchy`, `vote_franschise = none_voting`,
`upper_house_composition = appointed`, `press_rights = censored_press`,
`political_parties = underground_parties`, `plurality = 0.0`, hand-set upper
house 70 conservative / 17 liberal / 13 reactionary. Home provinces, all
`owner = DEN`: 366 Aarhus, 367 Aalborg, 368 Vejle, 372 Copenhagen, 373 Odense,
374 Bornholm, 2557 **Roskilde** - all checked against `map/definition.csv` lines
367-375 and 2558. (The history file for 2557 is `scandinavia/2557 - Esbjerg.txt`,
the vanilla path, which must not be renamed; the mod renames it in localisation
only, `localisation/PDM_CE.csv:271 PROV2557;Roskilde`. That the Roskilde estate
has its own province id here is a small gift.)

`common/governments.txt` gives `absolute_monarchy` `election = no`, so granting
`landed_voting` does not start election events - the franchise only feeds the
upper house, which is exactly the consultative reading this chain wants. The
`CleanUp.txt` events that watch `vote_franschise` (60050 at :994, 60029 at
:1032) fire only on dictatorship governments, so they cannot fire on DEN.

## Chain - `events/DENEstatesGVG.txt`, ids 1003200-1003204

| id | who | when | options |
|---|---|---|---|
| 1003200 | DEN | year >= 1822, not yet 1830, `war = no`, MTTH 20mo, flag-guarded | A hold the silver standard (AI 45) / B relieve the mortgages (AI 30) / C new land assessment (AI 25) |
| 1003201 | DEN | year >= 1830, not yet 1836, needs 1003200 done, `exists = SWH` plus `SWH = { vassal_of = THIS }`, MTTH 4mo, news | A gaol Lornsen (AI 65, up under a reactionary ministry) / B hear the Holstein knighthood (AI 35) |
| 1003202 | DEN | year >= 1831, not yet 1839, needs 1003201 done (or SWH already gone), absolute monarchy, MTTH 6mo, major, news | A grant the four estates (AI 55, up if B was taken at 1003201 or militancy is high) / B the King consults whom he pleases (AI 45, up under a reactionary ministry) |
| 1003203 | DEN | year >= 1835, not yet 1845, `has_country_flag = dan_estates_granted`, MTTH 5mo, news | A let them petition (AI 60) / B advice, and no more (AI 40) |
| 1003204 | DEN | year >= 1834, not yet 1842, `has_country_flag = dan_estates_refused`, MTTH 12mo | A relent, the estates shall meet (AI 40) / B order is kept (AI 60) |

Every event is self-firing with a `mean_time_to_happen`, and every option sets a
country flag that its own trigger negates - `fire_only_once` is engine-wide, not
per country, so it is not used anywhere in this file. Flags:
`dan_bankerot_settled`, `dan_lornsen_answered`, `dan_estates_decided`,
`dan_estates_met`, `dan_estates_petition_answered` (guards), and
`dan_hard_money`, `dan_landowner_relief`, `dan_land_tax`, `dan_lornsen_gaoled`,
`dan_holstein_heard`, `dan_estates_granted`, `dan_estates_refused` (branch
state). None of these names exist in the tree today: grepping
events/decisions/common/history for `dan_[a-z_]*` returns only
`dan_incorporated` and `dan_organized`, both unrelated.

Every branch flag is read somewhere later, so none of them is the dead flag that
`refcheck.py flags` hunts. `dan_hard_money` and `dan_land_tax` each weight
1003202 option A upward (`factor = 1.5`), and `dan_land_tax` also shortens the
1003202 MTTH (`factor = 0.7`): a crown that kept its word on silver, or that has
just reassessed the countryside, has both the credit and the pressure to consult.
`dan_lornsen_gaoled` weights 1003202 option B upward and 1003203 option B upward
(a ministry that gaoled the pamphleteer keeps the estates decorative).
`dan_landowner_relief` weights 1003204 option A upward - estates that were
relieved in the 1820s are owed a hearing in the 1830s. `dan_holstein_heard`
weights 1003202 option A upward; `dan_estates_granted` gates 1003203;
`dan_estates_refused` gates 1003204.

**1003200 - The Shadow of the Statsbankerot.** The 1813 default and the 1818
Nationalbank are done; what is live in the 1820s is the deflation needed to bring
the rigsbankdaler back to silver, on top of a collapsing grain price.
Option A holds the line: `add_country_modifier = { name = central_bank_established
duration = 3650 }` (existing, `common/event_modifiers.txt:813` - `loan_interest
-0.03`, `prestige 0.05`), `prestige = 2`, and a three-year
`local_economic_downturn` (existing province modifier, `local_RGO_output -0.2`,
`pop_consciousness_modifier 0.15`) on the two Jutland farm provinces 366 and 368
via `any_owned = { limit = { OR = { province_id = ... } } }`, plus
`rich_strata = { militancy = 1 consciousness = 1 }`. Option B buys the landowners
off: `treasury = -5000` (well inside the int32-hundredths ceiling), no central
bank, `prestige = 1`, `rich_strata = { militancy = -2 consciousness = -1 }`,
`poor_strata = { militancy = -1 }`, and a token downturn (730 days, 366 only).
Option C taxes the countryside instead: `treasury = 8000`,
`add_country_modifier = { name = tax_reforms duration = 3650 }`
(existing, `tax_efficiency 0.05`), the same three-year two-province downturn, and
`poor_strata = { militancy = 1 }`.

Rebalanced 2026-09-06 after review: `pop_consciousness_modifier` is a *monthly*
consciousness gain, so the original `duration = 1825` on four provinces holding
roughly two thirds of Denmark's pops was worth about +9 CON nationally on every
branch. Durations are now inside the 545-1095 band every other use of this
modifier in the tree sits in, and the province set is two rather than four.
Option B was strictly dominated at `treasury = -15000` for `rich_strata`
militancy alone (rich strata at 1821 is about 1% of Danish pops), so it now costs
5000 and pays in nationwide militancy relief and prestige - money for stability.
`central_bank_established` is time-limited to ten years rather than permanent so
that DEN does not carry a late-game economic modifier from 1823 onward. Vic2 options cannot carry triggers, so "the
treasury is already empty" is expressed as an `ai_chance` modifier on B and C,
not as a conditional option.

Reusing `central_bank_established` temporarily suppresses
`decisions/Political.txt:53 institute_central_bank`, whose `potential` is
`NOT = { has_country_modifier = central_bank_established }` and whose only effect
is that same modifier. Denmark got its note-issuing bank in 1818; the decision is
blocked only while the ten-year modifier is live, which ends long before DEN could
research `modern_central_bank_system` anyway.
`recession` and `economic_trend` were considered and rejected: both are added
*and removed* on a schedule by the business-cycle chain in
`events/EconomicalEvents.txt` (`:87, :116, :769, :1098, :1238, :1398, :1738,
:1774, :1805, :1841`), so a five-year `recession` set here would be cleared by
the next pulse. `local_economic_downturn` is only ever added with a duration
(`events/EconomicalEvents.txt:544`, `events/DIM_flores.txt:300`), so it is safe.

**1003201 - Uwe Jens Lornsen and the Pamphlet.** November 1830: the Landvogt of
Sylt publishes *Ueber das Verfassungswerk in Schleswigholstein*, demanding one
constitution and one assembly for the two duchies together. Option A is the
historical answer - arrest, and a year in the fortress: `prestige = -1`,
`set_country_flag = dan_lornsen_gaoled`, and
`SWH = { any_owned = { limit = { OR = { province_id = 369 province_id = 370
province_id = 371 } } add_province_modifier = { name = nationalist_agitation
duration = 1825 } } }` (existing province modifier, `pop_consciousness_modifier
0.1`, `pop_militancy_modifier 0.2`, used the same way at
`events/1german_revolution_1848.txt:416`), plus `SWH = { any_pop = { limit =
{ has_pop_culture = north_german } consciousness = 1 militancy = 1 } }` -
`has_pop_culture` is pop-scope and this is inside `any_pop`, matching
`events/SWHFlavor.txt:39-41`. Option B refuses to make a martyr and receives the
Holstein knighthood instead: `SWH = { any_pop = { consciousness = 1 } }`, a
three-year `underground_newspaper` (existing, mild province modifier) on 369, no
militancy, and `set_country_flag = dan_holstein_heard`, which is what later
weights the AI toward granting the estates. Neither option releases, annexes or
re-cores anything.

**1003202 - The Rescript of 28 May 1831.** The hinge of the chain, `major = yes`.
Option A creates the four consultative estates - Roskilde for the islands,
Viborg for Norrejylland, Slesvig, and Itzehoe for Holstein: `political_reform =
landed_voting` **then** `political_reform = state_equal_weight` (that order
matters; the `allow` on `state_equal_weight` in `common/issues.txt:352-356` is
`NOT = { vote_franschise = none_voting }`), the new permanent country modifier
`danish_provincial_estates`, `prestige = 5`, `plurality = 5`,
`any_pop = { militancy = -1 consciousness = 1 }`, and the same two reforms
mirrored into the vassal, `SWH = { political_reform = landed_voting
political_reform = state_equal_weight any_pop = { militancy = -2 consciousness =
1 } }` - half the estates sit on SWH soil, so the vassal has to get them too.
Government stays `absolute_monarchy`: a landed franchise feeding a
state-weighted upper house under a king who still appoints his ministry is
precisely what the 1831 rescript was. Option B refuses: `press_rights` is pushed
down a step to `state_press` (the `next_step_only = yes` on
`common/issues.txt:406` constrains the reform UI, not the `political_reform`
effect - `events/PORMiguelistGVG.txt:66` does exactly this from `censored_press`),
a ten-year `conservative_reaction` (existing country modifier,
`global_pop_consciousness_modifier -0.1`, `global_pop_militancy_modifier 0.02`),
`prestige = -2`, five years of `liberal_agitation` on 372 and 2557 and of
`nationalist_agitation` on the three SWH provinces, and
`middle_strata = { militancy = 1 consciousness = 1 }`.

**1003203 - The Estates Assemble.** The Roskilde and Viborg assemblies first sat
in October 1835 and the Slesvig and Itzehoe ones in 1836, so this fires from
1835. Option A treats the petitions seriously: `prestige = 3`, `plurality = 5`,
`any_pop = { consciousness = 1 militancy = -1 }`, and a ten-year
`educational_reform` (existing, `research_points_modifier 0.15`,
`global_pop_consciousness_modifier 0.05`) - school and poor-law petitions were
the real business of the estates. Option B keeps them decorative: a five-year
`conservative_reaction`, `prestige = 1`,
`middle_strata = { militancy = 1 consciousness = 1 }`.

**1003204 - The Petition of the Landowners.** The refusal branch is not a dead
end. Option A relents: `clr_country_flag = dan_estates_refused`,
`set_country_flag = dan_estates_granted`, `remove_country_modifier =
conservative_reaction`, the same reform grant as 1003202A but `prestige = 2`
instead of 5 - and because 1003203 triggers on `dan_estates_granted`, the chain
rejoins its own closing event. Option B holds: a ten-year `growing_unrest`
(existing, `global_pop_consciousness_modifier 0.03`,
`global_pop_militancy_modifier 0.02`), `prestige = -1`, five years of
`liberal_agitation` on 372 and 2557.

## New modifiers - one, in `docs/design/_pending/DENEstatesGVG_modifiers.txt`

`common/event_modifiers.txt` is not edited by this chain; the block in that
scratch file is the paste-ready text for the GVG section at the end of it.

- `danish_provincial_estates` (country, `duration = -1`):
  `administrative_efficiency_modifier 0.05`, `tax_efficiency 0.05`,
  `issue_change_speed 0.10`, `global_pop_consciousness_modifier 0.02`,
  `global_pop_militancy_modifier -0.02`, `prestige 0.02`, icon 7.
  Every key checked against `docs/wiki/modifier-effects.md` (:9, :640, :213, :165,
  :506) and against country modifiers that already use the same set:
  `kolowrat_administration` (administrative efficiency, tax efficiency,
  consciousness) and `metternich_system` (issue_change_speed, prestige), both in
  `common/event_modifiers.txt`.

Everything else is reused: `central_bank_established`, `tax_reforms`,
`conservative_reaction`, `educational_reform` and `growing_unrest` (country),
and `local_economic_downturn`, `nationalist_agitation`, `liberal_agitation` and
`underground_newspaper` (province). The four province modifiers all use
`pop_(trait)_modifier` / `local_RGO_output`, which
`docs/wiki/modifier-effects.md:800,854` documents as province-scope keys, so they
are only ever applied with `add_province_modifier`, never with
`add_country_modifier`.

## Localisation

New file `localisation/GVG_denmark.csv`, added key by key with
`python scripts/modcheck.py loc-add GVG_denmark.csv KEY "text"` (Edit/Write on
localisation csv is blocked by the PreToolUse hook). Keys: `EVTNAME1003200`
through `EVTNAME1003204`, `EVTDESC1003200` through `EVTDESC1003204`,
`EVTOPTA` and `EVTOPTB` for all five ids plus `EVTOPTC1003200`; news keys
`EVTNAME<id>_NEWS_TITLE` and `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT` for 1003201,
1003202 and 1003203; and `danish_provincial_estates` for the modifier. ASCII only
- "Abenra", "Slesvig", "Uwe Jens Lornsen", "Norrejylland", no accented
characters, no em dashes, no semicolons.

## Pictures

No new art. All five verified by listing the two directories:

- `Bankruptcy` (1003200) - vanilla, `D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\Bankruptcy.tga`.
- `publishers` (1003201) - vanilla, same folder.
- `Christiansborgs` (1003202) - vanilla, same folder; Christiansborg is where the
  rescript was drafted.
- `Upperhouse` (1003203) - vanilla, same folder.
- `deliberation` (1003204) - mod, `CoE_RoI_R/gfx/pictures/events/deliberation.tga`.

`danishgovernment` (vanilla) is the obvious alternative and is already used by
`events/DANFlavor.txt:35` and `events/ScandinavianEvents.txt:6`; it is left to
those. Names are written in the event file with the exact on-disk case, unlike
the `"Danishgovernment"` in DANFlavor, which only works because the filesystem is
case-insensitive. `python scripts/gfxtool.py missing` is silent today and must
stay silent.

## Risks

- The eight province ids (366, 368, 369, 370, 371, 372, 373, 2557) are the
  historical crash source in this repo; all are checked against
  `map/definition.csv` above and re-checked by `modcheck provinces`. No file under
  `history/provinces/` is created, moved or renamed by this chain.
- `state_equal_weight` makes the engine recompute the upper house from pop
  ideology per state, replacing the hand-set 70/17/13 of DEN. After 1831, reform
  passage becomes pop-driven and less predictable. That is the point of the
  branch, but it is a real balance change and worth watching in a test game.
- The chain must never set `danish_constitutionalism` and must never touch
  `government`, or it would lock out `decisions/DEN.txt:2 danmarks_riges_grundlov`
  (potential: absolute monarchy, `NOT = { has_country_flag =
  danish_constitutionalism }`). The `political_reform = landed_voting` inside that
  decision re-applies harmlessly after 1003202A.
- Likewise `annex_schleswig_holstein` and `schleswig_holstein_restored` are read
  by nothing in this chain and set by nothing in it; `events/SWHFlavor.txt`
  90050/90052 and `claim_schleswig` in `decisions/DEN.txt` keep working because
  SWH is never released, annexed or re-cored here.
- DEN forming SCA before 1836 is blocked by the `is_greater_power = yes` in
  `reform_kalmar`, so the triggers use `tag = DEN` alone rather than the
  `OR = { tag = DEN tag = SCA }` of `events/SWHFlavor.txt:12-15`. If DEN later
  becomes SCA the un-fired tail events simply never fire, which is acceptable.
- Five self-firing events on one tag inside fifteen years is a pacing load;
  `audit_pacing.py` should be run for DEN after the file lands. The MTTHs
  (20/4/6/5/12 months) and the sequential flag gates mean at most one is live at
  a time, except in the 1834-1836 overlap between 1003203 and 1003204, which the
  mutually exclusive `dan_estates_granted` / `dan_estates_refused` flags separate.
- 1003202 requires `dan_lornsen_answered`, which 1003201 can only set while
  `exists = SWH` and `SWH = { vassal_of = THIS }` hold. If a player or the AI has
  already broken the union before 1830 the core event of the chain never fires.
  The event file therefore gates 1003202 on `dan_bankerot_settled` plus
  `OR = { has_country_flag = dan_lornsen_answered NOT = { exists = SWH } }`, so a
  Denmark that has lost the duchies still gets its rescript.
- The rejoin from 1003204A into 1003203 has to survive the calendar: 1003204 can
  fire as late as 1841 on a 12-month MTTH from 1834, so 1003203 is capped at
  `NOT = { year = 1845 }` rather than 1842, and only 1003204 keeps the 1842 cap.
- `refcheck.py flags` should be run after the file lands. All twelve flags are
  read as well as set (see the flag paragraph above); the five guard flags are
  read by their own triggers and the seven branch flags by `ai_chance` and
  `mean_time_to_happen` modifiers in later events of the same file.
