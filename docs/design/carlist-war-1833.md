# The First Carlist War (1830-1840) — design

## Problem

Spain's succession crisis exists in the mod but is **undated**. `events/SPAFlavor.txt`
ships a complete Carlist package — 37760 "Carlism", 37710 "Carlism Prevails",
37711 "The Carlist War", 37712 "The Carlists Defeated!", 37713 "Return of the
Carlists", 37714/37715/37743 (province-level sympathies and cells), 37716/37717
(the Christino mirror for SPC) — and `common/rebel_types.txt:2415` / `:2713`
define `carlist_rebels` and `christino_rebels` on top of it. None of it is
anchored to a date:

- 37760 (`SPAFlavor.txt:460`) is the opener. Trigger: `tag = SPA`, `year = 1830`,
  a monarchy government, `NOT = { has_country_flag = carlism_questioned }`,
  `mean_time_to_happen = { months = 12 }`. Its single option sets
  `carlism_questioned` and `national_instability` for 1095 days.
- 37711 (`SPAFlavor.txt:646`) is the outbreak. Trigger: `has_country_flag =
  carlism_questioned` and `NOT = { has_country_modifier = national_instability }`,
  `mean_time_to_happen = { days = 1 }`, `fire_only_once = yes`. So the war starts
  **exactly one day after `national_instability` lapses** - i.e. 37760's fire date
  plus three years, anywhere from 1833 to 1836 depending on the MTTH roll. Nothing
  connects it to Ferdinand VII's death.
- The province files agree with the dating gap: `history/provinces/spain/492 - BIlbao.txt`,
  `493 - Pamplona.txt`, `494 - Logrono.txt`, `479 - Burgos.txt`, `481 - Soria.txt`,
  `496 - Huesca.txt`, `497 - Teruel.txt`, `499 - Gerona.txt`, `500 - Lerida.txt`,
  `501 - Tarragona.txt` and `504 - Castellon.txt` all carry a
  `1836.1.1 = { revolt = { type = carlist_rebels controller = yes } }` block. Vic2
  loads history only up to the bookmark, so at the **1821.9.1** start those blocks
  never execute and the war has no scripted beginning at all.
- `history/countries/SPA - Spain.txt:90` sets `carlism_questioned` in its
  `1836.1.1` block - again dead at the 1821 start.
- Nothing anywhere mentions the Pragmatic Sanction, Maria Cristina, the Quadruple
  Alliance, the British Legion or Vergara: grepping the tree for `Carlist`/`carlist`
  returns only `SPAFlavor.txt`, `PORFlavor.txt`, `PORMiguelistGVG.txt`,
  `BELFlavor.txt` and `BRZFlavor.txt` (the last three only reuse the `carlists`
  picture). `PORMiguelistGVG.txt:10` even names 37711/37712 as the pattern the
  Portuguese Liberal Wars copy.

So the job is **dating, not rewriting**. This chain pre-empts 37760 with a dated
1829 event that sets the same flag and the same modifier, holds the modifier until
1833.9.29, and then releases the legacy outbreak on the day Ferdinand VII dies.
37710-37717, the rebel types and the `carlist_provinces` variable are left
untouched and still resolve the war.

`SPC` is a real registered tag (`common/countries.txt:99`, "Carlist Spain") and
37711's option B already does the `change_tag = SPC` branch. `BSQ` (Basqueland,
`common/countries.txt:86`) has cores on 492/493 - it is deliberately **not**
released anywhere in this chain; the Basque rising was fought for a Spanish
pretender, not for secession, and a `release_vassal` here would hand a Great Power's
northern iron away over a provincial revolt.

Provinces (all verified in `map/definition.csv`, cultures verified in
`history/pops/1821.9.1/Iberia (inc Gibraltar).txt`): 492 Bilbao (basque, spanish),
493 Pamplona (basque, spanish), 494 Logrono (spanish), 496 Huesca (catalan,
spanish), 504 Castellon (catalan, spanish), 487 Madrid (spanish). 37711 already
stamps `carlist_sympathies` on 492/493/497/499/500/501, so this chain only ever
touches 494, 496 and 504 - three of the remaining provinces that carry the 1836
`carlist_rebels` block - and never a province 37711 has already stamped, to avoid any
risk of a duplicate `carlist_sympathies` stacking its `local_RGO_throughput -0.50`.
487 Madrid is reached only through `capital_scope`, never by id.

## Chain — `events/SPACarlistGVG.txt`, ids 1002700-1002705

| id | who | when | options |
|---|---|---|---|
| 1002700 | SPA | `year = 1829 month = 11` (December, 0-indexed), `NOT = { year = 1831 }`, monarchy government, `NOT = { has_country_flag = carlism_questioned }`, MTTH 20 days, `major = yes` | A promulgate the Pragmatic Sanction (AI 70) / B bow to the Salic law, Carlos is heir (AI 20) / C silence the court, decide nothing (AI 10) |
| 1002701 | SPA | `year = 1833 month = 8` (September), `NOT = { year = 1836 }`, `has_country_flag = carlism_questioned`, `NOT = { has_country_flag = ferdinand_vii_dead }`, MTTH 20 days, `major = yes`, news | A proclaim Isabella II, Maria Cristina regent (AI 70) / B rule as my brother did - Cea Bermudez (AI 20) / C send the army north before Carlos is proclaimed (AI 10) |
| 1002702 | SPA | `year = 1834 month = 3` (April), `NOT = { year = 1838 }`, `has_country_flag = gvg_carlist_war`, `NOT = { has_country_flag = quadruple_alliance_signed }`, `NOT = { has_country_flag = spain_stands_alone }`, MTTH 2mo, news | A sign the Quadruple Alliance (AI 75) / B Spain will settle her own quarrels (AI 25) |
| 1002703 | ENG | `is_triggered_only`, fired from 1002702 A after 15 days | A suspend the Foreign Enlistment Act and raise the Legion (AI 55) / B arms and a subsidy, no men (AI 30) / C Britain will not meddle (AI 15) |
| 1002704 | SPA | `year = 1837`, `NOT = { year = 1845 }`, `has_country_flag = gvg_carlist_war`, `num_of_revolts = 1`, `NOT = { has_country_flag = vergara_settled }`, MTTH 18mo, `major = yes`, news | A the Embrace of Vergara - confirm the fueros (AI 70) / B no terms with rebels (AI 30) |
| 1002705 | SPA | `year = 1840 month = 2` (March), `NOT = { year = 1846 }`, `has_country_flag = gvg_carlist_war`, `has_country_flag = carlist_no_quarter`, `NOT = { has_country_flag = carlist_crushed }`, MTTH 8mo, news | single option: the pretender is beaten and Spain concedes nothing |

Every event is `tag = SPA` (or ENG) locked and additionally guarded by its own
country flag in the trigger, so engine-wide `fire_only_once` is never load-bearing
(`scripts/audit_fire_once.py`). Conditionality lives in `ai_chance` weights, never
in option triggers.

### War state: `gvg_carlist_war`, not the legacy `carlist_war`

The back half of the chain used to gate on the legacy flag `carlist_war`. That is
unusable as a war-state variable: it is set in exactly one place in the tree
(`SPAFlavor.txt:671`, option A of 37711, which is `fire_only_once = yes`) and it is
cleared by 37712, whose trigger is only `has_country_flag = carlist_war` +
`NOT = { num_of_revolts = 1 }` at MTTH 1 month. Any revolt-free lull between 1834
and 1839 - and there are several - therefore clears it permanently, because nothing
can set it a second time. 1002702, 1002703 and 1002704 were silently dead in most
playthroughs, with no error.log entry.

All three options of 1002701 now `set_country_flag = gvg_carlist_war`, and 1002702,
1002704 and 1002705 read that flag. It is cleared by 1002704 option A and by
1002705. Both options of 1002704 also `clr_country_flag = carlist_war`, so once the
player has been offered Vergara the legacy 37712 ending - and its
`remove_accepted_culture = basque`, the opposite of what Vergara did - can never
fire on top of this chain's ending. `carlist_war` is read elsewhere only as a soft
weight: a `factor = 0.5` in the `carlist_rebels` `will_rise` block
(`rebel_types.txt:2386`) and three MTTH gates on the legacy sympathy-spread province
events (`SPAFlavor.txt:1154`, `:1374`, `:1495`). Rebel *spawning* is gated on
`carlism_questioned` plus `carlist_sympathies`, not on `carlist_war`, so clearing it
at Vergara does not switch the rebels off underneath a war that is still being
fought.

### 1002700 — The Pragmatic Sanction, 1829-1830

The trigger is a deliberate copy of 37760's, including its exact government `OR`
block (`hms_government`/`prussian_constitutionalism`/`absolute_monarchy` and their
`2`/`3` variants), so this event is a drop-in replacement: **all three options set
`set_country_flag = carlism_questioned`**, which permanently blocks 37760 (whose
trigger is `NOT = { has_country_flag = carlism_questioned }`).

The date gate is 1829.12 rather than 1830.3 **to close the race with 37760**, which
is eligible from 1830.1.1 at MTTH 12 months. A March gate would leave two months in
which only 37760 can fire, and in that branch its own 1095-day instability lapses in
early 1833 and the war opens seven months early. Opening in December 1829 - Ferdinand
VII's marriage to Maria Cristina, 11 December 1829, is the historical prerequisite
for the whole quarrel - with MTTH `days = 20` means 1002700 has set the guard flag
before 37760 is ever eligible. 1002701 additionally keys off `carlism_questioned`
rather than a flag of its own, so even if something did fire 37760 first, the 1833
event still lands.

All three options also `add_country_modifier = { name = national_instability
duration = 1825 }` (reused, `common/event_modifiers.txt:2017`). 1002701 removes it
explicitly in October 1833 (about 3.8 years in practice), so the modifier is a *lock*
on 37711 rather than a timer; the nominal five years is only a ceiling, chosen so the
lock cannot lapse before Ferdinand dies. If 1002701 is never seen (Spain has stopped
being a monarchy by 1833) the lock expires in 1834 and the legacy chain resumes
exactly as it does today.

The options differ below that:

- **A promulgate** - `set_country_flag = pragmatic_sanction_1830`, `prestige = 2`,
  `any_pop = { limit = { OR = { type = clergymen type = aristocrats } } militancy = 2
  consciousness = 1 ideology = { value = reactionary factor = 0.05 } }`, and a small
  militancy/consciousness bump on 492/493 only (the apostolic north). The historical
  choice and the one that leads to the war as fought.
- **B bow to the Salic law** - `set_country_flag = carlos_recognised_1830`,
  `prestige = -2`, `add_country_modifier = { name = conservative_reaction duration =
  1095 }` (reused, `:81`), a national reactionary ideology shift
  (`ideology = { value = reactionary factor = 0.05 }`) and `scaled_militancy = {
  ideology = liberal factor = 4 }`. Carlos has the law on his side; the liberals are
  the ones who will have to rise. Read again by 1002701's and 1002702's `ai_chance`.
- **C silence the court** - `set_country_flag = succession_deferred`,
  `treasury = -3000` (pensions and exile for the apostolic ministers; well inside the
  fixed-point range), `any_pop = { consciousness = -1 }`. Cheapest now, but it gives
  neither side a head start in 1833 and weights the AI away from the 1834 alliance.

### 1002701 — The Death of Ferdinand VII, 29 September 1833

The hinge. Every option ends with `remove_country_modifier = national_instability`
and `set_country_flag = ferdinand_vii_dead`, which releases legacy 37711 (MTTH
1 day) on 1833.9.30 - the outbreak, the SPA/SPC fork and Espartero all stay in
`SPAFlavor.txt` where they are. This event is the regency's posture, not the war
declaration:

- **A Isabella II, Maria Cristina regent** - `set_country_flag = isabella_ii_regency`,
  `add_country_modifier = { name = liberal_reaction duration = 1825 }` (reused,
  `:87`), `relation = { who = ENG value = 25 }`, `relation = { who = FRA value = 25 }`
  (both recognised Isabella at once), a liberal ideology shift on `capital_scope`,
  and provinces 494 and 496 get `add_province_modifier = { name = carlist_sympathies
  duration = -1 }`. The Rioja and Aragon rise for Carlos before Madrid can move.
- **B rule as my brother did (Cea Bermudez)** - `set_country_flag =
  cea_bermudez_ministry`, `add_country_modifier = { name = conservative_reaction
  duration = 1825 }`, no foreign relation gain, `scaled_militancy = { ideology =
  liberal factor = 6 }` (the liberals will not fight for an absolutist regency), and
  `carlist_sympathies` on 494, 496 **and** 504. Cheap in the short run, the worst
  war.
- **C send Sarsfield north at once** - `treasury = -8000`, `war_exhaustion = 2`,
  `prestige = -2`, militancy +3 and `ideology = { value = reactionary factor = 0.05 }`
  on 492/493 (occupation radicalises), and only **one** new `carlist_sympathies`
  (province 494) - pre-emption keeps the rising close to 37711's own six provinces. Buy a smaller war with money and legitimacy. Every
  option seeds at least one province so that the 37712 race described below is closed
  on all three paths.

1002701 deliberately does **not** touch `carlist_provinces`. It fires one day before
37711, which unconditionally does `set_variable = { which = carlist_provinces value =
6 }`, so any `change_variable` here is wiped before a single `check_variable` site can
read it - the three branches would be indistinguishable to the eight legacy checks in
`SPAFlavor.txt` (`:1096`, `:1240`, `:1277`, `:1286`, `:1296`, `:1413`, `:1422`,
`:1515`). The branches are differentiated by the `carlist_sympathies` province
modifiers instead, which 37711 never overwrites and which are what the
`carlist_rebels` `spawn_chance` (`rebel_types.txt:2713`, `factor = 100` on
`has_province_modifier = carlist_sympathies`) and the legacy spread events
(`any_neighbor_province = { has_province_modifier = carlist_sympathies }`,
`SPAFlavor.txt:1246`) actually read. 1002702 option B still carries a
`change_variable` of its own: it fires in 1834-1837, well after 37711, so it survives. Placing them *before*
the outbreak also closes a latent legacy hole: 37712 ("The Carlists Defeated!")
fires on `has_country_flag = carlist_war` + `NOT = { num_of_revolts = 1 }` with MTTH
1 month, so without pre-seeded sympathies the war can end in a month before a single
rebel has spawned.

### 1002702 — The Quadruple Alliance, 22 April 1834

Gated on `has_country_flag = gvg_carlist_war` (see above) - if the player put Carlos
on the throne they are SPC and `tag = SPA` stops the chain dead.

- **A sign at London** - `set_country_flag = quadruple_alliance_signed`,
  `relation` +50 with ENG, FRA and POR, `prestige = 3`,
  `ENG = { diplomatic_influence = { who = THIS value = 50 } }`,
  `ENG = { country_event = { id = 1002703 days = 15 } }`, and the price:
  `any_pop = { scaled_militancy = { ideology = reactionary factor = 4 } }` - the
  Court resents foreign tutelage, and Britain gains influence in Madrid.
  `ai_chance` modifiers: x2 if `POR = { has_country_flag = por_charter_upheld }`
  (Maria II has already won her own war, `PORMiguelistGVG.txt:297`), x1.5 if
  `POR = { has_country_flag = por_liberal_war }`, x1.5 on `relation = { who = ENG
  value = 100 }`, x0.5 on `has_country_flag = cea_bermudez_ministry`.
- **B Spain will settle her own quarrels** - `set_country_flag = spain_stands_alone`,
  `prestige = 5`, `war_exhaustion = 2`, and the war widens: `carlist_sympathies` on
  494 and 496 behind `limit = { NOT = { has_province_modifier = carlist_sympathies } }`
  (so a 1002701-C game gets them here instead, and no province is ever stamped
  twice), with a matching `change_variable`.

### 1002703 — The British Auxiliary Legion (ENG)

`is_triggered_only`, fired from 1002702 A. `FROM` is SPA - the same sender-scope
pattern as `ZollvereinGVG.txt:36-76` (`relation = { who = FROM ... }`,
`FROM = { country_event = ... }`).

- **A suspend the Foreign Enlistment Act** - ENG `treasury = -5000`, `prestige = 2`,
  `relation = { who = FROM value = 25 }`,
  `FROM = { add_country_modifier = { name = british_legion duration = 1825 }
  war_exhaustion = -2 define_general = { name = "George de Lacy Evans"
  personality = bold background = war_college } }`. Traits verified in
  `common/traits.txt:284` and `:630`.
- **B arms and a subsidy, no men** - ENG `treasury = -3000`,
  `relation = { who = FROM value = 15 }`, `FROM = { treasury = 3000 }`. No modifier,
  no general, no domestic cost.
- **C Britain will not meddle** - `relation = { who = FROM value = -25 }`,
  `FROM = { war_exhaustion = 1 }`. `ai_chance` x3 if ENG `war = yes`.

### 1002704 — The Convention of Vergara, 1837-1840

The closing event, and the one place the chain overrides legacy behaviour on
purpose. 37712 ends the war with `remove_accepted_culture = basque` - the opposite
of what Vergara (31 August 1839) actually did.

The gate is deliberately **not** a fixed 1839 date. 37712 fires at MTTH 1 month
whenever `num_of_revolts` drops to zero, so any lull between rebel waves in 1834-1839
would close the war before a date-locked Vergara could ever appear. 1002704 therefore
opens at `year = 1837` and requires `OR = { num_of_revolts = 1 NOT = {
has_country_flag = carlist_war } }` - either the war is still alive, or the legacy
37712 has already declared it over. 37712 needs zero revolts *and* `carlist_war` set,
and the second half of that OR is only true once `carlist_war` is gone, so at any
given instant exactly one of them is eligible and the two can never both resolve the
chain. The OR also stops the chain stranding `gvg_carlist_war`: if 37712 fires first
it strips every `carlist_sympathies`, the `carlist_rebels` `factor = 100` spawn term
goes with it and a fresh revolt may never appear, so a bare `num_of_revolts = 1`
gate would leave 1002704 permanently ineligible.
MTTH 18 months with the modifiers below puts the expected fire date in 1838-1839.

- **A the Embrace of Vergara** - `set_country_flag = vergara_settled`,
  `clr_country_flag = carlist_war` (so 37712 can never fire),
  `any_owned = { remove_province_modifier = carlist_sympathies }`,
  `set_variable = { which = carlist_provinces value = 0 }`,
  `add_country_modifier = { name = basque_fueros duration = -1 }`, `prestige = 3`,
  `war_exhaustion = -2`, `any_pop = { limit = { OR = { has_pop_culture = basque
  has_pop_culture = catalan } } militancy = -6 consciousness = -1 }`,
  `any_pop = { scaled_militancy = { ideology = reactionary factor = -4 } }`, and
  `define_general = { name = "Rafael Maroto" personality = cautious background =
  turncoat }` - Maroto's officers taken into the royal army
  (`common/traits.txt:80`, `:713`). Basque stays an accepted culture. The rewards are
  deliberately modest (3 prestige, -2 war exhaustion) so that `basque_fueros` - a
  permanent `tax_efficiency = -0.03` bought with `core_pop_militancy_modifier =
  -0.03` - reads as the price of the peace rather than a free gift.
- **B no terms with rebels** - `set_country_flag = vergara_settled` (refire guard),
  `set_country_flag = carlist_no_quarter`, `clr_country_flag = carlist_war`, and the
  chain flag `gvg_carlist_war` is **left set**: the war goes on and 1002705 resolves
  it by force in 1840. Costs: `war_exhaustion = 3`, `treasury = -3000`, `prestige =
  2`, militancy +3 on 492/493 and a liberal ideology shift. No `basque_fueros`
  obligation. `ai_chance` x2 if `has_country_flag = spain_stands_alone`. Clearing
  `carlist_war` here is what stops the legacy 37712 from ending the war behind the
  player's back and taking `basque` off the accepted-culture list while doing it.

MTTH modifiers on 1002704: x0.5 on `has_country_flag = quadruple_alliance_signed`,
x0.5 on `NOT = { num_of_revolts = 2 }` (a single surviving rebel army is a stalemate
worth ending), x0.5 on `year = 1839`, x2 on `has_country_flag =
cea_bermudez_ministry`.

### 1002705 — The Fall of Morella, 1840

The payoff that makes 1002704 option B a real choice instead of a strictly dominated
one. Cabrera held Morella through the winter of 1839-40 with the last Carlist army in
the field; it fell on 30 May 1840 and he crossed into France. Trigger: `tag = SPA`,
`OR = { year = 1841 AND = { year = 1840 month = 2 } }` (March, 0-indexed),
`NOT = { year = 1846 }`, `has_country_flag = gvg_carlist_war`,
`has_country_flag = carlist_no_quarter`, `NOT = { has_country_flag = carlist_crushed }`.
MTTH 8 months, x0.5 on `NOT = { num_of_revolts = 1 }` (the rebels are already beaten),
x0.75 on `quadruple_alliance_signed`, x1.5 on `war_exhaustion = 10`. It deliberately
does **not** require zero revolts in the trigger, so a war that never quite ends
cannot strand the flag.

One option: `set_country_flag = carlist_crushed`, `clr_country_flag =
gvg_carlist_war`, `clr_country_flag = carlist_war`, `prestige = 8`, `war_exhaustion =
-3`, every `carlist_sympathies` removed, `set_variable = { which = carlist_provinces
value = 0 }`, basque/catalan pops `militancy = 2 consciousness = 1` (conquest, not
reconciliation - the northern resentment is the long-term price), `scaled_militancy =
{ ideology = reactionary factor = -6 }` with a small conservative shift, and
`define_general = { name = "Leopoldo O'Donnell" personality = bold background =
war_college }` (the same verified trait pair 1002703 uses). Picture `carlists`.

Net: A ends the war three to five years earlier at the cost of a permanent fiscal
exemption and a quiet north; B pays several more years of war exhaustion, keeps every
`carlist_sympathies` and its `local_RGO_throughput -0.50` until 1840, and buys
8 prestige, no fueros and a resentful Basque country.

## New modifiers — `docs/design/_pending/SPACarlistGVG_modifiers.txt`

Reused from `common/event_modifiers.txt` rather than redefined:
`national_instability` (`:2017`), `conservative_reaction` (`:81`),
`liberal_reaction` (`:87`), `carlist_sympathies` (`:2024`). Two are genuinely new
(every key verified against `docs/wiki/modifier-effects.md` and against existing
uses in `event_modifiers.txt`):

- `british_legion` (country): `land_organisation = 0.05`, `org_regain = 0.05`,
  `war_exhaustion = -0.01`, `icon = 26`.
- `basque_fueros` (country): `core_pop_militancy_modifier = -0.03`,
  `tax_efficiency = -0.03`, `icon = 3`. The fueros bought loyalty with a fiscal
  exemption; both halves are modelled.

## Localisation — `localisation/GVG_carlist.csv` (this chain's own file)

Added with `python scripts/modcheck.py loc-add GVG_carlist.csv KEY "text"` only -
Edit/Write on `localisation/*.csv` is blocked by the PreToolUse hook. Keys:
`EVTNAME`/`EVTDESC` for 1002700-1002705; `EVTOPTA`/`EVTOPTB`/`EVTOPTC` for 1002700,
1002701 and 1002703, `EVTOPTA`/`EVTOPTB` for 1002702 and 1002704, `EVTOPTA` for
1002705; the news set (`EVTNAME<id>_NEWS_TITLE`,
`EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`) for 1002701, 1002702, 1002704 and 1002705; and the two modifier names `british_legion` and `basque_fueros`.
ASCII only, so "Maria Cristina", "Cea Bermudez", "Logrono" and "Bilbao" all appear
unaccented.

## Pictures

No new art. All five already exist and are already referenced by shipped events:

- `Monarchy` (1002700) - vanilla `gfx/pictures/events/Monarchy.tga`, already used at
  `PORMiguelistGVG.txt:260` and `CleanUp.txt:1205`.
- `emperor_funeral` (1002701) - mod `CoE_RoI_R/gfx/pictures/events/emperor_funeral.tga`,
  used for Alexander I's death at `RUSDecembristGVG.txt:14`.
- `treaty` (1002702) - vanilla `treaty.tga`, used at `SPAAyacuchoGVG.txt:133`.
- `Recruits` (1002703) - vanilla `Recruits.tga`, used at `ACW.txt:259`.
- `war_ended` (1002704) - mod `war_ended.tga`, used at `SPAAyacuchoGVG.txt:22` and
  `AFGWarGVG.txt:223`.

`carlists.tga` (mod, already used by 37711/37713) is reused for 1002705, the one
event in this chain that is a direct continuation of the legacy war rather than a
distinct diplomatic beat.

## Risks

- **The lock is a shared modifier.** `national_instability` is generic PDM content,
  so anything that removes it from SPA between 1829 and 1833 would release 37711
  early. Grepping the whole tree for `remove_country_modifier = national_instability`
  returns exactly four sites: `BRZRegencyGVG.txt:249` (BRZ), `PORMiguelistGVG.txt:309`
  and `:406` (POR/UPB), and `SPAFlavor.txt:3122` - which is 37735 "A Return to Bourbon
  Rule", gated on `has_global_flag = spain_glorious_revolution` and a democracy
  government, i.e. the 1868 restoration, unreachable from an 1821 start before the
  1860s. Nothing can break the lock. Events that *add* the modifier
  (`PBC.txt`, `ChileanEvents.txt`, `newEvents.txt`, `PBCFlavor.txt`,
  `DIM/PERFlavour_five_x.txt`, `PORMiguelistGVG.txt`) only ever extend it, which is
  harmless here.
- **The 37760 race.** Closed by the 1829.12 gate plus MTTH 20 days, as described
  above; 37760 is not eligible until 1830.1.1, by which point `carlism_questioned` is
  already set. If some future change moves that gate later, the failure mode is
  graceful - 37760 fires, the war opens up to seven months early, and 1002701 still
  runs with a no-op `remove_country_modifier`.
- **The 37712 race.** Handled in both directions. If 1002704 comes first, both of its
  options `clr_country_flag = carlist_war`, which disarms 37712 permanently. If 37712
  comes first (a long revolt-free lull in 1834-1838) it runs its own ending and its
  `remove_accepted_culture = basque` - legacy behaviour, unavoidable without editing
  `SPAFlavor.txt` - but this chain tracks the war with `gvg_carlist_war`, so
  1002702/1002704/1002705 all survive it, and 1002704's `OR = { num_of_revolts = 1
  NOT = { has_country_flag = carlist_war } }` gate makes sure Vergara is still
  reachable afterwards even though 37712 stripped the sympathies that spawn rebels.
  The two are never simultaneously eligible. Every option of 1002701 also seeds at
  least one `carlist_sympathies` province before 37711 fires, so rebels exist within
  weeks of the outbreak.
- **The 1829-1833 window.** `carlism_questioned` is now set roughly a year earlier
  than 37760 would have set it, and `national_instability` runs about 3.8 years
  instead of three. `carlist_rebels` `spawn_chance` requires that flag, so Spain carries
  slightly more reactionary rebel pressure through the early 1830s. Mitigated by
  keeping 1002700's pop effects small (militancy 1-2, on clergy/aristocrats and on
  492/493 only) and by the fact that the x100 `carlist_sympathies` factor - the thing
  that actually makes Carlist rebels spawn in numbers - is not applied until 1833.
- **Ordering.** 37711 fires the day after 1002701 removes the lock, and SETs
  `carlist_provinces = 6`. 1002701 therefore never writes that variable; the province
  modifiers themselves
  are never overwritten, and the chain never stamps `carlist_sympathies` on a
  province 37711 also touches, so there is no risk of a double-stacked
  `local_RGO_throughput -0.50`.
- **Republican Spain.** If SPA is not a monarchy in 1829 or 1833 the chain simply
  does not fire and 37760/37711 behave exactly as they do today.
- **SPC.** 37711 option B changes the tag; 1002702-1002705 are `tag = SPA` and stop
  cleanly, leaving 37716/37717 and `christino_rebels` to run the mirror war.
- **Province ids** are the historical crash source in this repo. 492, 493, 494, 496
  and 504 are all confirmed in `map/definition.csv` and are re-checked by
  `modcheck provinces`; 494, 496 and 504 each already carry a 1836 `carlist_rebels`
  block in their own history file, which is the historical warrant for using them.
- **`decisions/SPA.txt`** gates `establish_la_guardia_civil` on `carlism_questioned`;
  setting that flag in 1830 makes the decision reachable three to six years earlier
  than before. Its `allow` block still requires `ideological_thought` and no ongoing
  revolt, so in practice it stays out of reach until the war is over.
