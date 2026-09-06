# The Unitarian-Federal Wars and the rise of Rosas (1828-1835) - design

## Problem

`docs/design/1821-1836-coverage.md:60` lists "Argentine unitarian-federal wars
1828-31" as **missing** with no pointer. That is right, and it understates it:
grepping the whole tree for `rosas` / `quiroga` / `dorrego` / `lavalle` /
`unitari` / `federal pact` / `caudillo` / `mazorca` returns **nothing** in
`events/`, `decisions/` or `common/`. The only near-hits are
`events/SouthAmericaFlavor.txt:740` (`EVTNAME97084` "Claiming the Pampas", a
colonisation event with no politics in it) and the picture name `Facundo` used
by `events/ARGFlavor.txt:151`.

What ARG already has, verified by reading the files:

- **The Cisplatine War is covered.** `events/URUFlavor.txt:46410-46421`
  (46410 "Thirty-Three Easterners", `tag = ARG`, `year = 1824`, sets the
  `cisplatine_war` country flag; 46414 lets ARG `inherit = URU`; 46415-46421 are
  the British mediation and the Treaty of Montevideo). Nothing in that chain
  touches domestic politics, and 46420 leaves ARG holding `cisplatine_war`.
  This design does not touch any of it.
- **`events/ARGFlavor.txt` is entirely post-1844.** 46600 (`year = 1851`,
  Alberdi), 46601 (`year = 1844`, the book *Facundo*, requires a
  `presidential_dictatorship` or an absolute monarchy), 46605/46610/46611/46612
  (`year = 1850`, the Entre Rios / Urquiza / Caseros chain), 46615-46630
  (Falklands, 1833+ but purely Anglo-Argentine). There is a nine-year hole
  between the end of the Cisplatine War and the first flavour event.
- **The 1836 country-history block is dead.**
  `history/countries/ARG - Argentina.txt` has an `1836.1.1 = { ... }` block that
  sets `government = presidential_dictatorship`, clears `liberal_constitution`,
  sets `conservative_constitution` and `cisplatine_war`, and hardens every
  political reform - i.e. it hand-waves this entire chain. Per
  `docs/audit/bridge-1836.md:9`, Victoria 2 applies country-history dated blocks
  only up to the bookmark date, so in an 1821 game **none of it happens**. ARG
  runs the whole century as `government = democracy`,
  `ruling_party = ARG_conservative`, `vote_franschise = landed_voting`,
  `upper_house_composition = appointed`, `public_meetings = yes_meeting`,
  `press_rights = state_press`, `political_parties = harassment`, carrying the
  `liberal_constitution` flag, unless an event changes it. Nothing does.

Tags. **ARG** is the Buenos Aires tag: `common/countries.txt:501`
(`ARG = "countries/Argentina.txt"`), capital 2348 Buenos Aires,
`primary_culture = platinean`. The coverage doc's "RPL" is wrong -
`common/countries.txt:53` is `RPL = "countries/Rupert's Land.txt"`.
`LPL` (`common/countries.txt:35`) is a real La Plata tag but owns **no province**
at 1821 and is only reachable through `decisions/ARG_irredentism.txt`
`unite_la_plata`, which requires `nationalism_n_imperialism` - unreachable
before the 1850s. The chain is therefore `tag = ARG` only; no
`OR = { tag = ARG tag = LPL }` wrapper. `ENT` (Entre Rios,
`common/countries.txt:31`) exists as a tag but is only released by
`events/ARGFlavor.txt:412` in the 1850s Urquiza chain. This design releases
nothing and creates no tag.

Parties available in the window (`common/countries/Argentina.txt`):
`ARG_liberal_2` (liberal, 1820-1856), `ARG_conservative` (conservative,
1820-1870), `ARG_reactionary` (reactionary, 1820-2000), `ARG_anarcho_liberal`.
So both `ruling_party_ideology = liberal` and `= reactionary` resolve to a real
party at every date the chain touches.

Provinces, all checked against `map/definition.csv` and
`history/provinces/south america/`:

- Owned by ARG at 1821: 2348 Buenos Aires, 2349 Junin, 2351 La Plata,
  2356 Corrientes, 2357 Curuzu Cuatia, 2358 Santo Tomas, 2359 Colon,
  2360 Parana, 2361 Santa Espiritu, 2362 Reconquista, 2363 Rosario,
  2364 Resistencia, 2368 Salta, 2369 Jujuy, 2373 Tucuman, 2374 Catamarca,
  2376 Santiago del Estero, 2379 Cordoba de Argentina, 2383 San Luis,
  2385 La Rioja, 2387 San Juan, 2389 Mendoza, 2554 Posadas.
- **Empty at 1821**: 2350 Azul, 2352 Mar del Plata, 2353 Trenque Lanquen,
  2354 Bahia Blanca, 2355 Carmen, 2393 Telen, 2395 Curaco. All seven carry
  `add_core = ARG` and an `1836.1.1 = { owner = ARG }` block that, by the same
  bridge rule, never fires. They are handed over one at a time instead by
  `SouthAmericaFlavor.txt:97084`, which has no `fire_only_once` and no flag
  guard and runs at `months = 10`; on an average roll the frontier is complete
  around 1828-1830. That is why the Desert Campaign event below is **not** a
  land grab.

No file under `history/provinces/` is created, moved or renamed.

## Chain - `events/ARGFederalGVG.txt`, ids 1002800-1002804

| id | who | when | options |
|---|---|---|---|
| 1002800 | ARG | `year = 1828`, `NOT = { year = 1833 }`, neither outcome flag set, MTTH 4mo, major, news | A shoot Dorrego, Unitarian coup (AI 45) / B restore Dorrego, terms with the Federals (AI 55) |
| 1002801 | ARG | `year = 1829`, `NOT = { year = 1835 }`, either flag from 1002800, MTTH 5mo, news | A the Restorer of the Laws (AI 60) / B a government of the educated (AI 40) |
| 1002802 | ARG | `year = 1831`, `NOT = { year = 1838 }`, either flag from 1002801, MTTH 4mo, major, news | A the Federal Pact (AI 65) / B the League of the Interior (AI 35) |
| 1002803 | ARG | `year = 1833`, `NOT = { year = 1840 }`, either flag from 1002802, MTTH 6mo, news | A march to the Rio Negro (AI 70) / B a line of forts and treaties (AI 30) |
| 1002804 | ARG | `year = 1835`, `NOT = { year = 1842 }`, `has_country_flag = arg_desert_campaign`, MTTH 3mo, major, news | A grant the governor the whole public power (AI 70) / B try the murderers, call a constituent congress (AI 30) |

Every event is a self-firing MTTH event, so every option sets the flag the next
event reads, and every trigger negates its own event's outcome flags. One
scope note that applies throughout: `militancy` and `consciousness` are
pop-scope effects, so every "militancy down on provinces X, Y, Z" below is
written as `any_owned = { limit = { OR = { province_id = ... } } any_pop = {
militancy = -2 } }`, the shape used in `PORMiguelistGVG.txt:1001000`. There is no
`fire_only_once` anywhere in the chain - it is engine-wide, not per country
(`scripts/audit_fire_once.py`, `docs/audit/fire-only-once.md`). Flags allocated,
none of which appears anywhere in the tree today: `arg_unitarian_coup`,
`arg_dorrego_spared`, `arg_rosas_first_term`, `arg_unitarian_govt`,
`arg_federal_pact`, `arg_unitarian_league`, `arg_desert_campaign`,
`arg_rosas_triumph`, `arg_suma_del_poder`, `arg_constituent_congress`.

### 1002800 - Lavalle and the Fall of Dorrego (December 1828)

The Army of the South comes home from Brazil and Lavalle takes the Fort. The
trigger does **not** carry `war = no`: a Cisplatine War that runs long would
otherwise lock the chain out of its 1828-1832 window. The MTTH carries
`modifier = { factor = 3 war = yes }` and
`modifier = { factor = 0.5 has_country_flag = cisplatine_war }` instead - the
returning army is literally the historical trigger, and `cisplatine_war` is set
on ARG by `URUFlavor.txt:46410`.

Option A (the coup succeeds, Dorrego shot at Navarro):
`set_country_flag = arg_unitarian_coup`, `prestige = -4`,
`ruling_party_ideology = liberal` (government stays `democracy` - see below),
`political_reform = no_meeting`, `political_reform = underground_parties`,
`clr_country_flag = reactionary_election_win`,
`set_country_flag = liberal_election_win` (the pairing convention from
`PORMiguelistGVG.txt:1001000`; the Unitarians are the liberals here),
`add_country_modifier = { name = national_instability duration = 1095 }`,
`add_country_modifier = { name = coup_risk duration = 730 }`, and an `any_owned`
limited to the cattle provinces of the campana and the littoral (2349 Junin,
2351 La Plata, 2356 Corrientes, 2360 Parana, 2363 Rosario,
2379 Cordoba de Argentina) whose `any_pop` raises reactionary ideology and
`scaled_militancy` on reactionary pops. ARG owns all six at 1821, so the
`any_owned` is not the silent no-op `scripts/audit_owner_scope.py` hunts for.

Option B (Dorrego lives, the governor comes to terms with the Federal militias):
`set_country_flag = arg_dorrego_spared`, `prestige = 2`,
`add_country_modifier = { name = military_strife duration = 730 }` - the officer
corps is the thing that suffers - plus an `any_pop` limited to `type = officers`
/ `type = soldiers` raising liberal ideology and militancy. No reform change, no
government change, no money.

### 1002801 - The Restorer of the Laws (December 1829)

Fires off either 1828 flag. There is **no** `immediate` block clearing them:
`immediate` runs before the option is picked, so clearing the 1828 flags there
would make the `ai_chance` modifiers below dead weight, and the flags are wanted
later anyway. The trigger instead negates this event's own outcomes -
`NOT = { has_country_flag = arg_rosas_first_term }`,
`NOT = { has_country_flag = arg_unitarian_govt }` - which is what keeps it from
re-arming.

Option A: `government = presidential_dictatorship` **before**
`ruling_party_ideology = reactionary` - effect order copied from
`PORMiguelistGVG.txt:1001000` option A, because `presidential_dictatorship` in
`common/governments.txt` permits only `socialist`, `conservative` and
`reactionary`, so the ideology must be set once the government already allows
it. Then `set_country_flag = arg_rosas_first_term`, `prestige = 3`,
`remove_country_modifier = national_instability`,
`add_country_modifier = { name = conservative_reaction duration = 1825 }`,
`clr_country_flag = liberal_election_win`,
`set_country_flag = reactionary_election_win`. Rural pops calm
(`militancy = -2` over the same six campana and littoral provinces); an
`any_owned` limited to 2348 Buenos Aires, with an `any_pop` limited to
`type = capitalists` / `type = bureaucrats` / `type = clergymen`, gains liberal
ideology and consciousness - the Unitarian emigration to Montevideo.

Option B: `set_country_flag = arg_unitarian_govt`, government left at
`democracy`, `ruling_party_ideology = liberal`,
`add_country_modifier = { name = liberal_reaction duration = 1825 }`,
`add_country_modifier = { name = national_instability duration = 1095 }`,
`plurality = 2`, and militancy up in the interior. This branch is **deliberately
unstable in engine terms**: `democracy` has `election = yes duration = 48`, so
the ideology set here survives at most four years before an election can replace
it, whereas the Rosas branch runs under `presidential_dictatorship`, which has
`election = no` and is sticky. That asymmetry is the point - Unitarian
governments in Buenos Aires did not last.

`ai_chance` on A is weighted up by `has_country_flag = arg_dorrego_spared`; on B
by `has_country_flag = arg_unitarian_coup`.

### 1002802 - The Unitarian League and the Federal Pact (January 1831)

Option A, the Federal Pact of 4 January 1831: `set_country_flag =
arg_federal_pact`, a twenty-year (`duration = 7300`) `federal_pact` country
modifier (new, below), `prestige = 3`, `militancy = -2` through an `any_owned`
on the littoral signatories (2348 Buenos Aires, 2356 Corrientes, 2360 Parana,
2363 Rosario), `relation = { who = URU value = 25 }` and
`relation = { who = PRG value = 25 }` - both tags are registered
(`common/countries.txt:509`, `:508`) and both exist at 1821.

Option B, the League of the Interior under Paz: `set_country_flag =
arg_unitarian_league`, a twenty-year `unitarian_league` country modifier (new),
`prestige = 2`, `add_country_modifier = { name = national_instability
duration = 1825 }`, and an `any_owned` over the ten interior provinces
(2368 Salta, 2369 Jujuy, 2373 Tucuman, 2374 Catamarca, 2376 Santiago del Estero,
2379 Cordoba de Argentina, 2383 San Luis, 2385 La Rioja, 2387 San Juan,
2389 Mendoza) adding the existing `liberal_agitation` province modifier for
1825 days plus pop militancy. ARG owns all ten at 1821.

`ai_chance` on A carries `modifier = { factor = 2 has_country_flag =
arg_rosas_first_term }`; on B, `modifier = { factor = 3 has_country_flag =
arg_unitarian_govt }`. The two `relation` lines are wrapped as
`random_country = { limit = { tag = URU exists = yes } relation = { who = THIS
value = 25 } }` (and the same for PRG), the pattern `PORMiguelistGVG.txt`
1001000-A uses for BRZ, because ARG may have annexed URU through
`URUFlavor.txt:46414` by 1831. Neither option releases a tag, cedes a province or
declares a war: the unitarian-federal conflict is expressed as pop militancy and
country modifiers, the way `PORMiguelistGVG.txt` and `SPAFlavor.txt:37711`
handle the Miguelist and Carlist wars, so the engine rebels do the fighting.

### 1002803 - The Campaign of the Desert (1833-34)

Because `SouthAmericaFlavor.txt:97084` has usually finished the Pampas by 1833,
the payload here is **prestige, a province modifier and a political flag**, not
land. The `X = { secede_province = THIS }` lines are a fallback for a slow roll
of 97084 and a no-op where ARG already owns the province. The country-scope
form `<province id> = { secede_province = THIS }` is the working pattern from
`events/BoerWar.txt:143`.

Option A: `set_country_flag = arg_desert_campaign`,
`set_country_flag = arg_rosas_triumph`, `treasury = -6000` (ARG is poor; the
java-war figure of 20000 would be most of its cash, and the fixed-point ceiling
of 2147483 is nowhere near), `war_exhaustion = 2`, `prestige = 6`, the seven
secede lines for 2350, 2352, 2353, 2354, 2355, 2393 and 2395, and an `any_owned`
limited to 2354 Bahia Blanca, 2355 Carmen, 2393 Telen and 2395 Curaco adding
`settlement_colony` for `duration = 3650`. An `any_pop` limited to
`type = soldiers` / `type = aristocrats` gets `militancy = -2`.

Option B: `set_country_flag = arg_desert_campaign` only, `treasury = -1500`,
`prestige = 1`, the two nearest secede lines (2350 Azul, 2352 Mar del Plata) and
no modifier. Both options set the same continuation flag; only A sets
`arg_rosas_triumph`, which is what weights 1002804.

### 1002804 - Barranca Yaco (February 1835)

Quiroga is ambushed on the road from Cordoba. The option names are
branch-neutral - a Unitarian-league player reaches this event too, and the
choice is about the office, not the man.

Option A, the suma del poder publico: `set_country_flag = arg_suma_del_poder`,
`government = presidential_dictatorship` then `ruling_party_ideology =
reactionary`, `political_reform = none_voting`, `political_reform =
party_appointed`, `political_reform = no_meeting`, `political_reform =
underground_parties` (each exactly one step from the 1821 value;
`vote_franschise` in `common/issues.txt:283` is marked `next_step_only = yes`),
`clr_country_flag = liberal_constitution` **and** `set_country_flag =
conservative_constitution` in the same option (see Risks),
`clr_country_flag = liberal_election_win`, `set_country_flag =
reactionary_election_win`, `remove_country_modifier = national_instability`,
`add_country_modifier = { name = suma_del_poder_publico duration = 6200 }`
(new, about seventeen years, expiring around Caseros), `prestige = 5`, and
`any_pop = { militancy = -3 consciousness = -2 }` plus a reactionary ideology
shift. `ai_chance` `factor = 70` with
`modifier = { factor = 2 has_country_flag = arg_rosas_triumph }` and
`modifier = { factor = 1.5 has_country_flag = arg_rosas_first_term }`.

Option B, try the Reinafe brothers and call a constituent congress:
`set_country_flag = arg_constituent_congress`, then `government = democracy`
followed by `ruling_party_ideology = liberal` (democracy permits liberal; the
same ordering rule as A). Setting the government explicitly matters: a player
who took 1002801-A is already in a `presidential_dictatorship`, and "leave it
untouched" would make this option a no-op for exactly the branch it is meant to
reverse. Also `clr_country_flag = reactionary_election_win`,
`set_country_flag = liberal_election_win`, mirroring A. Then
`prestige = -2`, `plurality = 2`, `add_country_modifier = { name =
national_instability duration = 1825 }`, `add_country_modifier = { name =
liberal_reaction duration = 1825 }`, liberal ideology up and reactionary
militancy up. `liberal_constitution` is left alone.

**Downstream interlock, stated deliberately:** `ARGFlavor.txt:46610` (the 1850
Constitutional Demand that opens the Urquiza and Caseros chain) and
`ARGFlavor.txt:46605` both require ARG to be in a `presidential_dictatorship`,
and 46601 (the book *Facundo*, 1844) requires a dictatorship or an absolute
monarchy. Option A therefore wires this chain into the existing 1850s content;
option B closes it off unless ARG drifts back to a dictatorship by 1850. That is
the historically correct shape - Caseros happened because Rosas ruled - and it
is the price of the liberal branch.

## New modifiers

Written ready-to-paste to `docs/design/_pending/ARGFederalGVG_modifiers.txt`;
`common/event_modifiers.txt` is shared and is not edited by this design.

Reused rather than reinvented (line numbers in `common/event_modifiers.txt`):
`national_instability` (:2017), `conservative_reaction` (:81),
`liberal_reaction` (:87), `liberal_agitation` (:19, province), `coup_risk`,
`military_strife` (:1686), `settlement_colony` (:3347, province).

New, three:

- `federal_pact` (country, applied for 7300 days):
  `administrative_efficiency_modifier -0.05`, `tax_efficiency -0.05`,
  `core_pop_militancy_modifier -0.05`,
  `global_pop_consciousness_modifier -0.02`, `RGO_throughput 0.05`, icon 7.
  A loose league: no central state worth the name, but the provinces stop
  burning each other estancias.
- `unitarian_league` (country, 7300 days):
  `administrative_efficiency_modifier 0.05`, `tax_efficiency 0.05`,
  `research_points_modifier 0.05`, `core_pop_militancy_modifier 0.05`,
  `global_pop_consciousness_modifier 0.02`, icon 4. The mirror image: a real
  state, permanently resented.
- `suma_del_poder_publico` (country, 6200 days):
  `suppression_points_modifier 0.50`, `issue_change_speed -0.50`,
  `global_pop_consciousness_modifier -0.05`,
  `global_pop_militancy_modifier -0.02`, `global_immigrant_attract -0.20`,
  `mobilisation_size 0.02`, `prestige 0.02`, icon 15.

Every key above appears in `docs/wiki/modifier-effects.md` and already in
`common/event_modifiers.txt`. Note `global_immigrant_attract`, not
`immigrant_attract` - the latter is province-scope and `scripts/audit_common.py`
checks the distinction. The dictatorship modifier is **not** `duration = -1`:
Rosas fell at Caseros in 1852, and a permanent country modifier would still be
running in 1936.

## Localisation

New file `localisation/GVG_platine.csv`, created and appended only through
`python scripts/modcheck.py loc-add GVG_platine.csv KEY "text"` (Edit and Write
on `localisation/*.csv` are blocked by the PreToolUse hook). No pre-existing csv
is touched.

- `EVTNAME1002800` to `EVTNAME1002804`, `EVTDESC1002800` to `EVTDESC1002804`,
  and `EVTOPTA<id>` / `EVTOPTB<id>` for all five ids - 20 keys.
- News keys for all five, since every event carries `news = yes`:
  `EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG`, `_NEWS_MEDIUM` and
  `_NEWS_SHORT` - 20 keys.
- Three modifier names: `federal_pact`, `unitarian_league`,
  `suma_del_poder_publico`.

ASCII only - Cordoba, campana, Parana, suma del poder publico, malon, all
without accents; no em dashes, no curly quotes, no semicolon in any field.

## Pictures

No new art, nothing downloaded. Four files from
`CoE_RoI_R/gfx/pictures/events/` and one vanilla fallback; each was decoded with
`python scripts/gfxtool.py preview` to confirm it actually fits the moment.

| id | picture | where it lives | what it shows |
|---|---|---|---|
| 1002800 | `Execution` | mod `gfx/pictures/events/Execution.tga` (also in vanilla) | a firing squad drawn up in a field - Dorrego at Navarro. Already used by `ARGFlavor.txt:546` |
| 1002801 | `military_reform` | mod `gfx/pictures/events/military_reform.tga` | officers and frock-coated civilians round a table signing a document - the Sala de Representantes voting the facultades extraordinarias |
| 1002802 | `confederation` | mod `gfx/pictures/events/confederation.tga` | a convention of some forty delegates in a long hall - the Pact, or the League |
| 1002803 | `Expansion` | mod `gfx/pictures/events/Expansion.tga` (also in vanilla) | a mounted officer pointing across an empty horizon |
| 1002804 | `Facundo` | vanilla only, `D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\Facundo.tga` | horsemen ambushing a stagecoach - literally Barranca Yaco. Already referenced by `ARGFlavor.txt:151`, so `gfxtool.py missing` stays silent |

`national_congress.tga` was considered for 1002802 and rejected on inspection:
it is a photograph of the Indian National Congress.

## Risks

- **The `liberal_constitution` trap.** `SouthAmericaFlavor.txt:97095`
  ("Constitutional Controversy", `major = yes`, `months = 1`) fires for any
  country whose `capital_scope` is in South America and which holds neither
  `liberal_constitution` nor `conservative_constitution`, and its two options
  overwrite `government` and three political reforms. ARG starts with
  `liberal_constitution` (undated head of its history file), so 97095 is blocked
  today. If 1002804-A cleared `liberal_constitution` without setting
  `conservative_constitution`, 97095 would fire within a month and stomp the
  whole outcome. The option therefore sets both flags in the same block, and no
  other option in the chain touches either flag.
- **Province ids** are the historical crash source in this repo (commit
  `31764737`, province 3309 against 1408). All thirty ids used are listed above
  and were read out of `map/definition.csv`; the PostToolUse hook and
  `modcheck.py provinces` re-check them.
- **97084 overlap.** If a slow roll leaves frontier provinces empty past 1833,
  1002803-A grants them and 97084 simply stops finding empties; if 97084 has
  already finished, the secede lines are no-ops. Nothing is taken from another
  owner: none of the seven is `colonial = 1` and only ARG has cores on them, so
  no other tag can hold them.
- **`settlement_colony` on empty provinces.** Its payload is
  `immigrant_attract 2.5` and `life_rating 0.10`; the four frontier provinces
  have no pops in `history/pops/1821.9.1`, so the immigration half may be inert
  until pops migrate in. The life-rating half applies regardless. If in-game
  testing shows it does nothing, swap it for a small `local_RGO_output` province
  modifier rather than adding a fourth new one.
- **Event load.** Five self-firing MTTH events on one tag over seven years sits
  inside the `scripts/audit_pacing.py` band for a major playable; ARG currently
  has no events at all between 1828 and 1844, so the chain fills a hole rather
  than crowding one.
- **Election drift.** On the 1002801-B and 1002804-B branch ARG stays a
  `democracy`, so the engine election system can put a conservative back in
  power four years later and the branch quietly reverts. Accepted, not a bug; it
  is exactly why the Rosas branch uses `presidential_dictatorship`.
- **`inherit = URU`.** If the player won the Cisplatine War through
  `URUFlavor.txt:46414`, ARG owns Montevideo (2344) when this chain runs.
  Nothing here enumerates 2344 and every `any_owned` is limited by explicit
  province id, so the annexed Banda Oriental is simply not addressed - which is
  correct, because the Uruguayan civil war is a separate episode.
- **Nothing shared is edited.** No change to `events/GVG Event IDs.txt`,
  `common/event_modifiers.txt`, `common/on_actions.txt`, any pre-existing
  localisation csv, or any other chain file. The registry line for the
  orchestrator to merge is: `#1002800-1002899: ARGFederalGVG (1828-1835
  Unitarian-Federal wars, Lavalle and Dorrego, the Federal Pact, the Desert
  Campaign, Barranca Yaco and the suma del poder publico; 1002800-1002804 used)`.
