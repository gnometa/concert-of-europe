# Event audit: `CoE_RoI_R/events/` A-G (plus digit-, `+`- and `DIM/`-prefixed files)

Scope: the 70 event files whose name starts with a digit, `+` or A-G, plus everything in
`events/DIM/`. 1474 `country_event`/`province_event` blocks.
Tooling: `python scripts/audit_events.py` (`vocab` sub-command for the keyword pass only).
It reuses `refcheck.py`'s parser and deliberately does **not** repeat refcheck's checks
(dead event ids, missing localisation, undefined modifiers/flags, orphan events, unknown
culture/religion/goods/cb/reform names).

## Counts

| | |
|---|---|
| files in range | 70 |
| events | 1474 |
| `fire_only_once = yes` | 283 |
| `is_triggered_only = yes` | 425 (9 of them also `fire_only_once`) |
| events with an MTTH (self-firing) | 1068 |
| unknown keywords (distinct) | 4 |
| repeatable events granting permanent effects | 4 |
| always-false / always-true triggers | 0 |
| scope errors (`country_event` at province scope etc.) | 0 |
| events where every option is `ai_chance factor = 0` | 0 |
| MTTH modifiers with `factor = 0` and no trigger | 0 |
| `year`/date gates below 1821 (dead gates) | 0 |
| date gates at or after 1836 | 313 (in 45 files) |
| triggers made live by the 1821 start (`NOT = { year <= 1836 }`) | 6 |

The vocabulary used for the keyword pass is the union of `docs/wiki/list-of-conditions.md`,
`list-of-effects.md`, `list-of-scopes.md` and friends, every key vanilla's own
`events/*.txt` and `decisions/*.txt` use (~1900 keys), and every technology, invention,
reform option, ideology, government, pop type, building, good, rebel type and crime the mod
defines (those are legal bare trigger keys). Tags, `TAG_<state>` scopes and numeric province
scopes are recognised as scopes, so only genuinely unrecognised words are reported. All four
survivors below were checked against vanilla by hand and are real.

## Defects

### Unknown keywords

`CoE_RoI_R/events/BYZFlavorGVG.txt:14` (also `:138`, `:169`) — `has_truce = RUS` is not a
Victoria 2 condition; the engine's condition is `truce_with`. The three uses sit inside
`NOT = { ... }` blocks, so the truce guard silently does nothing and the Russian-protector
events can fire while a truce with Russia is running. — **fix**: rename to
`truce_with = RUS`. The same typo exists at `CoE_RoI_R/events/USAFlavorGVG.txt:12`
(outside this audit's range) and should be fixed in the same pass. **[high]**

`CoE_RoI_R/events/CHIFlavor.txt:2645` and `CoE_RoI_R/events/CleanUp.txt:2381,2399,2414` —
`unciv_military_industry` is not an issue group in `CoE_RoI_R/common/issues.txt` (the mod's
unciv reforms are `unciv_light_armament`, `unciv_artillery`, `unciv_military_training`,
`unciv_officer_corps`, `unciv_military_doctrines`, `unciv_naval_construction`,
`unciv_naval_organisation`). At `CleanUp.txt:2414` it is used as an *effect*, so a
Westernisation step silently does nothing; at `CHIFlavor.txt:2645` it is one term of an AND
in the "New Army" trigger. — **fix**: map the four uses onto an existing unciv reform (most
likely `unciv_light_armament` / `unciv_military_doctrines`) or add the missing issue group.
**[high]**

`CoE_RoI_R/events/DIM/PERFlavour_five_x.txt:1184` — `random_neighbor = { relation = { ... } }`
is not a scope; the engine's names are `random_neighbor_country` and
`random_neighbor_province`. The whole option effect is dropped. — **fix**:
`random_neighbor_country`. **[medium]**

`CoE_RoI_R/events/CivilizationAndGunBoats.txt:3959` — `activate_unit = regular` is not an
effect (the neighbouring line `activate_building` is already commented out). Units are
unlocked by technology; the line does nothing and logs an error. — **fix**: delete it, or
replace with `activate_technology`/`activate_invention` for the tech that unlocks the unit.
**[medium]**

### Events that repeat and stack permanent effects

Only self-firing events (trigger + MTTH) with no `fire_only_once` and no flag/modifier/
ownership guard are listed; time-limited `add_*_modifier` (finite `duration`) is not counted.

`CoE_RoI_R/events/01_SocFlavour.txt:2` — event 99990 "Road to Communism Paved!" has
`mean_time_to_happen = { months = 1 }`, a trigger of only "socialist government +
literacy >= 0.75", and grants `prestige = 10` plus `add_country_modifier = { name =
road_to_communism_paved duration = -1 }`. It re-fires roughly every month for the rest of
the game: unbounded prestige and a modifier stack. — **fix**: add
`NOT = { has_country_modifier = road_to_communism_paved }` to the trigger (the paired
event 99989 already removes the modifier, so `fire_only_once` would be wrong here).
**[high]**

`CoE_RoI_R/events/GREFlavor.txt:1065` — event 31240 "Imperial Pretensions Challenged" fires
for BYZ every ~12 months while `is_greater_power = no`, each time applying
`prestige = -50`, `badboy = -15` and ~10 `remove_core = BYZ` calls that are no-ops after the
first run. A non-great-power Byzantium bleeds 50 prestige a year forever. — **fix**:
`fire_only_once = yes`, or guard with a country flag set in the option. **[high]**

`CoE_RoI_R/events/EconomicalEvents.txt:399` — event 22540 (stock exchange) repeats every
~600 months and adds a permanent province modifier each time. — **fix**: `fire_only_once`
or a `has_province_modifier` guard on the target province. **[medium]**

`CoE_RoI_R/events/ColonialUprisings.txt:300` — event 14540 (colonial museum) repeats every
~300 months, adding a permanent modifier to a `random_owned` province each time. Slow, but
a long game accumulates several. — **fix**: `fire_only_once = yes`. **[medium]**

### Date gates relative to the 1821.9.1 start

No gate is dead (`year = N` with `N < 1821`: none), and no always-false or always-true
trigger was found. Note for future work: in Victoria 2 a `NOT` containing several statements
is a NOR (all must be false), per `docs/wiki/list-of-conditions.md:86` — the very common
`NOT = { year = 1840  war_with = USA }` idiom in these files is therefore correct and was
*not* reported.

313 triggers gate on 1836 or later. Most are genuine historical lower bounds (the commonest
are 1850, 1870, 1846, 1840) and are fine. The ones that read as "not before game start"
rather than as history are the bare `year = 1836` gates — 8 of them, all inherited from
vanilla/PDM flavour chains, and each locks the first 15 years of the mod's timeline out of
its country's flavour:

- `CoE_RoI_R/events/AUSFlavor.txt:11` (31501, AUS/KUK opener) **[medium]**
- `CoE_RoI_R/events/ENGFlavor.txt:56` (36900, public meetings; window `1836..1839`) **[medium]**
- `CoE_RoI_R/events/ENGFlavor.txt:1641`, `:3530` **[low]**
- `CoE_RoI_R/events/FRAFlavor.txt:64` (37201, window `1836..1840`), `:544` (37213) **[medium]**
- `CoE_RoI_R/events/COBFlavor.txt:12`, `CoE_RoI_R/events/DIM/PERFlavour_five_x.txt:3527` **[low]**

**fix** for each: lower the bound to `year = 1821` (or drop it) where the flavour is not tied
to a dated event, and keep it only where the text names something that really happened in
1836+. Where the event is one end of a narrow window (`year = 1836` + `NOT = { year = 1839 }`)
the whole window should be moved, not just the lower bound, or the event never gets its extra
15 years.

Six triggers are the mirror image: they were unreachable on a 1836 start and are now live.
They should be play-checked, three of them fire within days of the start:

- `CoE_RoI_R/events/CLMFlavor.txt:10` — 37800 "El Libertador" (GCO), `NOT = { year = 1836 }`,
  MTTH `days = 1`: fires on the first day of the 1821 game. Intended, but verify the option
  effects suit 1821 rather than the tail of Bolivar's career. **[medium]**
- `CoE_RoI_R/events/CLMFlavor.txt:90` — PNM joins Colombia, `NOT = { year = 1830 }`. **[low]**
- `CoE_RoI_R/events/FRAFlavor.txt:1551` — 37244, `NOT = { year = 1836 }`, MTTH `days = 3`:
  a Three-Glorious-Days follow-up that can now resolve almost immediately. **[medium]**
- `CoE_RoI_R/events/FRAFlavor.txt:1239` — 37234 (Charles X / July Revolution vs ALD). **[low]**
- `CoE_RoI_R/events/ChileanEvents.txt:903` — `NOT = { year = 1825 }`, MTTH in days. **[low]**
- `CoE_RoI_R/events/00_CoE_RoI.txt:1015` — `NOT = { year = 1825 }`. **[low]**

### Checks that came back clean

`is_triggered_only` + `fire_only_once` combinations (9) are all harmless loop targets.
No `country_event` is fired from a province scope and no `province_event` from a country
scope without a scope change (the numeric `300 = { province_event = ... }` form in
`Exploration.txt` and `DIM_flores.txt` is correct). No option set has all its `ai_chance`
weights at 0, and no MTTH `modifier = { factor = 0 }` lacks a trigger.

## Narrative / historical review of the six largest files in range

Files read: `China.txt`, `CBsAndCores.txt`, `crises.txt`, `ACW.txt`, `ColonialUprisings.txt`,
`BritishDominions.txt`.

`CBsAndCores.txt` and `crises.txt` turned out to hold no dated historical content at all —
they are the generic CB-generation flavour, core-integration province events and the
Great-Wars flashpoint/crisis system. Nothing in them interacts with the 1821 start (the lone
`year = 1900` at `crises.txt:365` is late-game crisis suppression). Likewise most of
`ColonialUprisings.txt` is undated `colonial_nation` flavour; it contains no Latin-American
independence or Indian Mutiny content to mis-date.

### China.txt — the awakening chain assumes the awakener is CHI

`CoE_RoI_R/events/China.txt:33` — event 90900 fires for `tag = CHI`, `TPG` or `QNG` (the
`civilize_your_nation_china` decision in `decisions/UncivFlavor.txt` passes all three), but
its option looks for vassals with `substate_of = CHI` instead of `substate_of = THIS`. A
Taiping or Qing-successor westernisation notifies China's tributaries, not its own. —
**fix**: `substate_of = THIS`. **[high]**

`CoE_RoI_R/events/China.txt:279`, `:300` — the follow-ups 90901/90902 hardcode
`leave_alliance = CHI` for the same reason; the vassal leaves an alliance with China even
when the overlord that civilised was TPG/QNG. — **fix**: `leave_alliance = FROM`. **[high]**

`CoE_RoI_R/events/China.txt:305-368` — event 90903 (commented `#Unused? -Koro`, and indeed
nothing fires it) triggers on GXI/MCK/XIN/YNN/XBI/MGL, i.e. post-1911 warlord and successor
states that cannot exist for ninety years after the start. It also sets the shared
`the_dragon_wakes` global flag and civilises CHI (via 90904) rather than itself, so if it
were ever re-enabled it would permanently block the real CHI/TPG/QNG chain. — **fix**:
delete it. **[low]**

`CoE_RoI_R/events/China.txt:247` — event 90901 reuses `title = "EVTNAME90900"` and its
second option uses `EVTOPTB90100`; the player sees the "China Awakens" headline on the
vassal follow-up. — **fix**: `EVTNAME90901` / `EVTOPTB90901`. **[low]**

### ACW.txt — the war can start twice, and 1861 history overrides the dynamic chain

`CoE_RoI_R/events/ACW.txt:2` — event 16000 "A House Divided" releases the CSA
(`release_vassal = CSA`) but has neither `fire_only_once` nor `NOT = { exists = CSA }`; its
only guard is `NOT = { has_global_flag = american_civil_war_has_happened }`, and that flag is
set two months later by the separate Fort Sumter event 16005 (`ACW.txt:311`). With
`mean_time_to_happen = { months = 12 }` the secession event can roll a second time inside the
gap. — **fix**: `fire_only_once = yes`, or add `NOT = { exists = CSA }` to the trigger.
**[high]**

`CoE_RoI_R/events/ACW.txt:15` — 16000's trigger keys off `has_country_flag =
the_slavery_debate`, but that flag is set unconditionally in the undated block of
`history/countries/USA - USA.txt:42`, so it is true from 1821 onward, while the player-facing
"Slavery Debate" event 16001 only ever adds a *modifier* of the same name. The narrative
chain and the mechanical gate are disconnected. — **fix**: check
`has_country_modifier = the_slavery_debate`, or set the flag from 16001 rather than in
history. **[medium]**

`CoE_RoI_R/events/ACW.txt:461` — Dred Scott's MTTH has
`modifier = { factor = 0.9  has_country_flag = john_browns_raid }`, making the 1857 decision
*less* likely once the 1859 raid has happened, i.e. the historical order is discouraged. —
**fix**: invert the factor or drop the modifier. **[low]**

Cross-file (outside this audit's scope but caused by the events above):
`history/countries/USA - USA.txt:139` force-loads the 1861 wartime OOB and sets
`american_civil_war_has_happened` on a fixed `1861.1.1`, and `history/countries/CSA -
CSA.txt:159,165` re-apply CSA's setup on the same date. With a 1821 start the dynamic chain
can resolve the war years earlier, after which those blocks overwrite the result. Worth a
follow-up in the history audit. **[medium]**

### BritishDominions.txt

`CoE_RoI_R/events/BritishDominions.txt:1429` — Southern Rhodesia's MTTH still carries
`modifier = { factor = 0.5  year = 1910 ... }` copied from the Australia/South Africa
template, although the event's own trigger already requires `year = 1924`, so the modifier is
unconditional. The event also calls Rhodesia a Dominion, which it never was (it was a
self-governing colony). — **fix**: drop the dead year check and reword. **[low]**

`CoE_RoI_R/events/BritishDominions.txt:1261` — "The Alaskan Dominion" fires whenever ENG/ENL
owns any of the `USA_1` region and hands the whole region's cores to CAN/LSK without checking
what the USA holds there. — **fix**: add an `owns`/`NOT = { USA = { owns = ... } }` check on
the region's provinces. **[low]**

## Status (2026-09-06 fix pass)

### Fixed
- `has_truce` -> `truce_with`: `BYZFlavorGVG.txt:14,138,169` (RUS), `USAFlavorGVG.txt:12` (USA).
- `unciv_military_industry` -> `unciv_artillery` (the mod's real group; option `no_artillery_for_you`)
  at `CHIFlavor.txt:2645` and `CleanUp.txt:2381,2414`; `CleanUp.txt:2399`
  `unciv_military_industry = unciv_light_armament` -> `unciv_artillery = early_light_artillery`.
  The paired effect at `CleanUp.txt:2419` was `military_reform = unciv_light_armament` (a group
  name, not an option) and is now `military_reform = early_light_artillery`, which matches the
  `activate_technology = bronze_muzzle_loaded_artillery` on the next line.
- `01_SocFlavour.txt` 99990: trigger gains `NOT = { has_country_modifier = road_to_communism_paved }`
  (not `fire_only_once`, because 99989 removes the modifier and the chain is meant to be re-enterable).
- `GREFlavor.txt` 31240: `fire_only_once = yes`. Option A ends BYZ via `change_tag = GRE`, so only the
  refusal option could repeat, and it handed out free prestige every year.
- `China.txt:33` `substate_of = CHI` -> `substate_of = THIS`; `:279`, `:300` `leave_alliance = CHI` ->
  `leave_alliance = FROM` (90901/90902 are fired from the awakener's `any_country` scope, and both
  events already use FROM for `inherit`/`relation`, so FROM is the civilising overlord). The two
  further `CHI` hardcodings at `:332`/`:338` are inside the dead event 90903 and were left alone.
- `ACW.txt:2` 16000: `fire_only_once = yes` plus `NOT = { exists = CSA }` in the trigger.
- `ACW.txt:15`: `has_country_flag = the_slavery_debate` -> `has_country_modifier = the_slavery_debate`.
  Every other event in the chain (16002, 16010, ...) already gates on the *modifier* that 16001 adds;
  the flag is set unconditionally by USA history from 1821, so it gated nothing. History left untouched.
- `USAFlavorGVG.txt:26`: `realtion` -> `relation`.
- `PERFlavour_five_x.txt:1184`: `random_neighbor` is not a scope and `random_neighbor_country` does not
  exist either (vanilla and `list-of-scopes.md` only have `random_neighbor_province`). Rewritten as the
  vanilla idiom `random_country = { limit = { neighbour = THIS } ... }`
  (cf. vanilla `events/CBsAndCores.txt:550,675`).
- `CivilizationAndGunBoats.txt:3959`: `activate_unit = regular` commented out, matching the already
  commented `#activate_building` above it and the identical commented pair in `China.txt:64-65`.
  `activate_unit` is a technology key, not an event effect.
- `MostlyHarmless.txt:19`: dead `suez_canal_built` -> `suez_canal_global` (set by `decisions/Canals.txt:52`).
- `GREFlavor.txt:102` (raised in `docs/audit/events-H-Z.md`) - the London Conference chain reused
  `EVTNAME31200`/`31202`/`31205` as the title of several different outcome events, so they were
  indistinguishable in the message log. Events 31201, 31203, 31204, 31206 and 31207 now use their own
  keys, added to `localisation/PDM_CE.csv` via `modcheck.py loc-add`.

### Bare `year = 1836` gates - decisions

| Location | Event | Decision |
|---|---|---|
| `ENGFlavor.txt:1641` | 36937 "The Name of the Royal House" | **lowered to 1821** - undated dynastic flavour, really gated by `exists = COB` + war with GER/PRU |
| `COBFlavor.txt:12` | 35000 "British Monarchy Splits From the House of Saxe-Coburg-Gotha" | **lowered to 1821** - follow-up to 36937, gated by `has_global_flag = ENGRoyalHouseAnglified` |
| `AUSFlavor.txt:11` | 31501 "Smoking Ban!" | kept - desc dates the Vienna ban to 1837 |
| `ENGFlavor.txt:56` | 36900 "The Reform Club" | kept - the Reform Club was founded in 1836; the `1836..1839` window is correct |
| `ENGFlavor.txt:3530` | 36983 South Australia claim | kept - South Australia was founded in 1836 |
| `FRAFlavor.txt:64` | 37201 "Arc de Triomphe" | kept - unveiled 1836; `1836..1840` window correct |
| `FRAFlavor.txt:544` | 37213 "Democracy in America" | kept - Tocqueville published in 1835 |
| `PERFlavour_five_x.txt:3527` | 190345 "The Allahdad" | kept - the Mashhad Allahdad was 1839 |

### Deferred
- `EconomicalEvents.txt:399` (22540) and `ColonialUprisings.txt:300` (14540) - still repeat and stack a
  permanent province modifier; medium, outside this pass.
- `China.txt:305-368` event 90903 (dead warlord-state chain) and `China.txt:247` (wrong `EVTNAME90900` /
  `EVTOPTB90100` loc keys) - low.
- `ACW.txt:461` inverted Dred Scott MTTH modifier; `ACW.txt` vs `history/countries/USA - USA.txt:139` /
  `CSA - CSA.txt:159,165` 1861 hardcoding - for the history audit.
- `BritishDominions.txt:1261,1429` - low.
- `GREFlavor.txt` 31208/31209/31210 still share `EVTNAME31205` and 31212 shares `EVTNAME31211`;
  those are the "X agrees/refuses" pairs where one headline arguably fits both, so they were left.
- The six `NOT = { year = ... }` triggers that the 1821 start makes live still need play-testing.
