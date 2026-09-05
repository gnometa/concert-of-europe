# AI behaviour and balance audit

*2026-09-06. Read-only. Line numbers against `master` (cab739e0). Scope: event `ai_chance`,
CB economy, rebels/revolutions, great-power start state, event spam, base economy. The
economy dispatcher, decision `ai_will_do` and cross-reference errors are covered in
`docs/audit/core-systems.md`, `docs/audit/decisions.md` and `scripts/refcheck.py` and are not
repeated. Conservative posture: PDM/vanilla behaviour is the default; only clear breakage is
tagged [high].*

## Defects

### [high]

~~`CoE_RoI_R/history/countries/*.txt:8` (all 521 files) - every country starts at
`literacy = 0.01`.~~ **Investigated 2026-09-06: intentional, left as is.** See
"Literacy: why the flat 0.01 start stays" below.

`CoE_RoI_R/common/production_types.txt:258-305` — the five factory chains are mis-priced
against `common/goods.txt`. `military_factory` returns **12.0x** its input cost and
`luxury_factory` **12.5x**, while `light_factory` returns **1.67x**. The AI factory builder
ranks by profitability, so it will build military and luxury factories to the exclusion of
everything else, and the light-industry tier that feeds luxury is the least attractive thing
to build. See Table 3. *Fix:* balance pass, not a patch — the two halves (`value` /
`input_goods` here, `cost` in `goods.txt`) have to move together. Target a 1.5-2.5x band for
every tier. Held for the same pass as the `core-systems.md` "Deferred" items.

~~`CoE_RoI_R/events/GreatPowers.txt:2` (id 800004) and `:78` (id 800006) - flag guard
commented out in both triggers.~~ **Fixed 2026-09-06.** Both guards uncommented. The chain
was already complete: 800004's option does `set_country_flag = military_access_granted`
and 800006's option does `clr_country_flag = military_access_granted`, so with the guards
live 800004 fires at most once per sphering and 800006 at most once per release.

### [medium]

`CoE_RoI_R/common/cb_types.txt` — the mod raised infamy on the *usable* CBs by roughly 7-14x
versus vanilla (`conquest` 2.2 -> 30, `acquire_state` 2.2 -> 15, `make_puppet` 2.0 -> 15,
`cut_down_to_size` 1.3 -> 12.5, `humiliate` 1.5 -> 7.5) while adding 52 new event-granted CBs,
**24 of which have `badboy_factor = 0`** — including `conquest_any` (`po_annex = yes`,
`prestige_factor = 5`), `acquire_any_state`, `annex_africa_full` (3.0), `colonial_reconquest_cb`,
`restore_america`, `restore_austrian_empire`, `restore_byzantine_empire`, `restore_british_raj`
and all four `great_war_install_*`. With `BADBOY_LIMIT` doubled to 50 (`common/defines.lua`,
noted in `common.md`), the practical effect is that ordinary expansion is priced out and
scripted expansion is free. *Fix:* balance pass. The cheap change is to give the
free-annexation ones (`conquest_any`, `annex_africa_full`, `colonial_reconquest_cb`) a nonzero
`badboy_factor` in the 2-5 band so the coalition system still sees them; leave the `restore_*`
and unification CBs at 0, since they are gated by decision/event prerequisites.

`CoE_RoI_R/common/rebel_types.txt` — `defection` was changed to `none` on the rebel types that
previously defected: `nationalist_rebels` (`culture` -> `none`, :1486), `communist_rebels`
(`ideology` -> `none`, :756), `pan_nationalist_rebels` (:1794), `red_shirts` (:2902), and
`indian_sepoys` (`independence` `culture` -> `none`, :3162). Winning rebels of these types
therefore no longer secede or flip the government; they only occupy. This is a mechanic
removal, not a tuning change, and the mod's revolution chains (`Revolution_*.txt`,
`2nd_grand_revolution.txt`) do the secession by script instead. *Fix:* confirm this was
deliberate and record it, or restore `defection` on `communist_rebels` and
`nationalist_rebels`, which have no scripted replacement.

`CoE_RoI_R/common/rebel_types.txt` — `spawn_chance` factors were rebased onto a much wider
scale than vanilla's 1-3, and the ordering now strongly favours nationalism:
`nationalist_rebels` 3 -> **100**, `unciv_reactionary_rebels` 3 -> **100**,
`separatist_rebels` **50** (new), `colonial_rebels` / `native_rebels` / `independence_rebels` /
`turkish_nationalist_rebels` **20** (new), against `liberal_rebels` 2, `socialist_rebels` 2,
`reactionary_rebels` 2, `communist_rebels` 2. `spawn_chance` is a relative weight, so
liberal/socialist rebels are now ~50x less likely to be the type that rises than nationalists
in any province where both are eligible — and those are the rebels the 1848 chain needs.
*Fix:* balance pass; the minimum sane change is to bring the ideological types onto the same
scale (10-20).

`CoE_RoI_R/common/rebel_types.txt:4436` — `separatist_rebels` combine `occupation_mult = 5.0`
with `defect_delay = 3` and `spawn_chance = 50`. Five-times-speed occupation plus a
three-month defection timer is the fastest-collapsing rebel in the file by a wide margin.
*Fix:* raise `defect_delay` to 12 (matching `colonial_rebels`) or drop `occupation_mult` to
3.0, in the same pass.

~~CSA 49 techs; thirteen unformed release tags at 24; `SPC` prestige 50.~~ **Fixed
2026-09-06.** All thirteen release tags (BRE, CZH, HOL, LUX, OLD, ORA, PHL, RHI, SAA, SPC,
TRN, WES, YUG) carried the *identical* 24-tech list, which is the vanilla/PDM **1836**
European standard - the same list Prussia's `1836.1.1` block has. It is an un-backdated
leftover from the move to an 1821 start, not a design choice. All thirteen were trimmed to
the mod's own 1821 minor tier (the 14-tech list shared by BAV, BAD and WUR), which sits
below every plausible parent (Prussia 21, Netherlands 17, Spain 17, Austria 19). `SPC`
prestige 50 -> 0.

CSA was trimmed from 49 to the USA's 22-tech list verbatim, so the Confederacy can no
longer be released ahead of the Union.

Austria was raised from 14 to 19 by adding the 1821-tier techs Prussia has and it lacked:
`military_staff_system`, `army_command_principle` (army), `naval_design_bureaus` (navy),
`early_classical_theory_and_critique`, `freedom_of_trade` (commerce). All five are already
in Austria's own `1836.1.1` block, so nothing was invented. `guild_based_production` and
`mechanized_mining` were deliberately left out - Austria stays two industry techs behind
Prussia (19 vs 21), which is the "first-rank power, weaker industry" shape asked for.

`CoE_RoI_R/history/countries/PER - Persia.txt` — Persia starts with 5 army techs, equal to
France, Prussia and Russia, and 0 navy/industry techs. Probably an artefact of the
`000_persia_*` submod merge. *Fix:* drop to 3.

## Literacy: why the flat 0.01 start stays

Every country - and every dated block inside every country file, not just the 1821 head -
carries `literacy = 0.01  non_state_culture_literacy = 0.01` with the old value commented
out. This was checked on 2026-09-06 and is **intentional**; the commented values are kept
as historical reference and were not restored.

Evidence:

- `git log -S"literacy = 0.01" -- CoE_RoI_R/history/countries` bottoms out at **8f5e1248
  "economic rework base"** (Mitusonator, 2020-12-09) - the same commit that rewrote
  `common/buildings.txt` and `common/goods.txt`. It flattened `literacy` *and*
  `non_state_culture_literacy` in the head block **and in the `1836.1.1` and `1861.1.1`
  blocks of every file**. An accident of the start-date change would have touched only the
  head block; wiping the whole literacy timeline is a design decision.
- `f5231d50 "literacy fix"` (2021-10-26) is only a reformat of the comment placement
  (`literacy = 0.01 #literacy = 0.69` became
  `literacy = 0.01  non_state_culture_literacy = 0.01   #literacy = 0.69`), not a revert.
- The surrounding commit stream tunes literacy *growth* rather than the start value:
  `92081418 "lower base literacy"`, `149285a2 "lower literacy speed"`,
  `31970187 "balanced literacy and state services"`, `a4c2e485 "lowered education effects"`,
  `6836458b "more exp for literacy"`, `7ea32ef1 "fixed education modifiers not aplying correctly"`.

How literacy is meant to move in this mod:

- There is **no script effect in Victoria 2 that sets pop literacy**; `literacy` in
  `events/`, `decisions/` and `+education_RGO*.txt` is only ever a *trigger*. Nothing
  outside the history files can seed it, so the education rework grows it purely through
  the engine's clergy / education-spending loop.
- `common/defines.lua:619-621` - `LITERACY_CHANGE_SPEED = 0.0050` (vanilla 0.1),
  `BASE_CLERGY_FOR_LITERACY = 0.003` (vanilla 0.005), `MAX_CLERGY_FOR_LITERACY = 0.05`
  (vanilla 0.04). Slower per tick, but rewarding a larger clergy.
- `common/static_modifiers.txt:157-161` - `base_values` grants a flat
  `education_efficiency_modifier = 2.00` to every country (vanilla grants none), tripling
  that base rate. On top of it sit well over a hundred further
  `education_efficiency_modifier` entries in `event_modifiers.txt`, `static_modifiers.txt`,
  `triggered_modifiers.txt`, `issues.txt`, `national_focus.txt` and all five
  `technologies/*.txt` files - education output is the mod's intended differentiator,
  replacing the historical head start.
- `events/+education_RGO.txt:505-750` reads state literacy in 0.1-wide brackets
  (`RGO_education_0` ... `RGO_education_9`) and stamps a matching RGO province modifier.
  That ladder starting at 0-0.1 only pays off if everyone starts at the bottom.

Consequence to keep in mind for the economy pass: because literacy is flat, the great-power
field really is separated only by tech count, prestige and education modifiers - which is
why the tech-count outliers above were worth fixing.

## Checks that came back clean

- **No event has `ai_chance = { factor = 0 }` on every option** (3171 events scanned). The
  "AI can never pick anything" failure mode does not occur anywhere in the mod.
- **No `add_casus_belli` in `events/` or `decisions/` omits `months`** — 146 grants, all with
  an expiry. There is no permanent scripted CB in the mod.
- **The 1848 chain is reachable from an 1821 start and terminates.**
  `LiberalRevolutions.txt:114` (10000) gates on `year = 1847` plus
  `has_country_flag = liberal_revolution_in_progress`; its option grants
  `springtime_of_nations` for `duration = 365` (`:229`), which is the modifier
  `1german_revolution_1848.txt:11` (99944) and sixteen `rebel_types.txt` spawn modifiers key
  off. 10050 (`:386`) closes the loop by setting `had_liberal_revolution` and clearing both
  in-progress flags; 99944 is `fire_only_once`. No re-fire path was found. (Note 99944's
  trigger also requires a specific human/AI arrangement across FRM/PRU/BAV/AUS; in an all-AI
  game the FRM branch is the one that qualifies, and FRM exists at start.)
- **No compounding militancy loop** in `LiberalRevolutions.txt`, `Socialism_Fascism.txt`,
  `1german_revolution_1848.txt` or `2nd_grand_revolution.txt`. Every repeating militancy event
  carries an MTTH of 20 months or longer plus a flag or modifier that its own option clears;
  the `days = 1` entries in the 1848 and 2nd-revolution chains are all `is_triggered_only`.
- **`CBsAndCores.txt` / `CBGeneration.txt` / `crises.txt` hand out no unbounded cores.** The
  repeating grants (2510, 2520, 2530, 2540, 2550, 2560, 2570, 2605, 2616, 2625) are PDM stock
  with MTTHs of 24-1200 months and self-clearing triggers.

## Table 1 — great power and secondary start state

Population is the sum of `history/pops/1821.9.1` sizes over provinces owned by the tag; a dash
means no owned province carries a pop entry under that tag at start (the tag is formed later,
or its provinces are owned by someone else in 1821). Literacy is `0.01` for every tag in the
mod and is omitted.

| tag | pop | prestige | plur | techs | army | navy | comm | cult | ind |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ENG | 6,872,958 | 250 | 15 | 27 | 3 | 5 | 9 | 4 | 6 |
| FRA | 7,746,775 | 150 | 5 | 25 | 5 | 5 | 5 | 6 | 4 |
| RUS | 12,106,502 | 200 | 0 | 17 | 5 | 4 | 2 | 4 | 2 |
| AUS | 8,148,433 | 100 | 5 | 19 | 5 | 3 | 4 | 4 | 3 |
| PRU | 3,265,125 | 80 | 0 | 21 | 5 | 3 | 5 | 4 | 4 |
| USA | 2,475,839 | 50 | 20 | 22 | 4 | 4 | 7 | 4 | 3 |
| TUR | 4,645,989 | 60 | 0 | 8 | 3 | 1 | 1 | 2 | 1 |
| SPA | 4,435,354 | 40 | 0 | 17 | 3 | 5 | 3 | 4 | 2 |
| NET | 4,032,854 | 60 | 5 | 16 | 3 | 5 | 3 | 3 | 2 |
| POR | — | 10 | 0 | 18 | 3 | 5 | 4 | 4 | 2 |
| SAR | 846,490 | 30 | 0 | 16 | 4 | 3 | 3 | 3 | 3 |
| SIC | 1,619,709 | 5 | 0 | 16 | 4 | 4 | 2 | 4 | 2 |
| SWE | 682,477 | 10 | 0 | 14 | 4 | 3 | 2 | 3 | 2 |
| DEN | 329,101 | 0 | 0 | 14 | 4 | 3 | 2 | 3 | 2 |
| BAV | 993,364 | 2 | 0 | 14 | 3 | 2 | 3 | 3 | 3 |
| BEL | — | 1 | 0 | **0** | 0 | 0 | 0 | 0 | 0 |
| BRZ | — | 1 | 0 | 8 | 3 | 1 | 1 | 2 | 1 |
| EGY | 1,352,933 | 0 | 5 | 8 | 1 | 3 | 1 | 3 | 0 |
| PER | 1,502,110 | 0 | 0 | 8 | **5** | 0 | 1 | 2 | 0 |
| QNG | 91,878,513 | 0 | 0 | 3 | 0 | 0 | 1 | 2 | 0 |
| HND | 21,384,048 | 0 | 0 | 7 | 3 | 3 | 0 | 1 | 0 |
| JAP | 1,009,965 | 0 | 0 | 4 | 0 | 0 | 1 | 3 | 0 |
| KOR | 4,349,362 | 0 | 0 | 3 | 0 | 0 | 1 | 2 | 0 |
| CSA | — | 0 | 0 | 22 | — | — | — | — | — |

Unformed tags formerly at 24 techs, now at 14: BRE, CZH, HOL, LUX, OLD, ORA, PHL, RHI, SAA,
SPC, TRN, WES, YUG.
Tech-count histogram over all 521 tags: 226 at 0, 67 at 2, 41 at 4, 23 at 5, 13 at 19, then
the list above. Qing and Japan at 3-4 techs and Korea at 3 are consistent with an unciv start;
no unciv outlier was found.

## Table 2 — `common/goods.txt` base prices vs vanilla

All 30 mod goods differ from vanilla. The mod deleted all 28 vanilla secondary goods
(`steel`, `machine_parts`, `regular_clothes`, `canned_food`, `artillery`, ...) and replaced
them with five abstract tiers, and added five raw goods.

| good | vanilla | mod | ratio |
|---|---:|---:|---:|
| tobacco | 1.1 | 5.6 | 5.09 |
| wool | 0.7 | 3.2 | 4.57 |
| opium | 3.2 | 12.8 | 4.00 |
| timber | 0.9 | 2.88 | 3.20 |
| coffee | 2.1 | 6.4 | 3.05 |
| coal | 2.3 | 5.14 | 2.23 |
| fish | 1.5 | 3.2 | 2.13 |
| iron | 3.5 | 7.38 | 2.11 |
| fruit | 1.8 | 3.2 | 1.78 |
| cotton | 2.0 | 3.2 | 1.60 |
| cattle | 2.0 | 3.2 | 1.60 |
| tea | 2.6 | 4.0 | 1.54 |
| tropical_wood | 5.4 | 8.0 | 1.48 |
| precious_metal | 8.0 | 10.0 | 1.25 |
| grain | 2.2 | 2.4 | 1.09 |
| sulphur | 6.0 | 5.6 | 0.93 |
| dye | 12.0 | 6.4 | 0.53 |
| rubber | 7.0 | 3.2 | 0.46 |
| silk | 10.0 | 4.0 | 0.40 |
| oil | 12.0 | 3.2 | 0.27 |

New, no vanilla equivalent: `military_industry` 20.0, `luxury_industry` 15.0,
`heavy_industry` 5.0, `light_industry` 5.0, `food_industry` **0.5**, `spices` 12.8,
`horses` 6.4, `copper` 4.16, `lead` 2.68, `sugar` 2.4.

## Table 3 — factory profitability at base prices

> **Corrected 2026-09-06 (see `docs/design/factory-balance.md`).** This table costs factories
> on `input_goods` only. The template `efficiency` block is **maintenance**, not a bonus: the
> engine buys those goods daily and vanilla sums them into the factory's cost
> ("total input+maint"). In this mod maintenance is 339-872 per level per day against 30-175
> of `input_goods`, so the ratios below are wrong by 3-12x and the ordering below is wrong
> too. Real ratios (input+maint): military 1.22, luxury 1.02, heavy 0.22, food 0.21,
> light 0.12. New **[high]**: `heavy_factory`, `light_factory` and `food_factory` cannot break
> even at base prices at any employment level; the maintenance blocks (or the output `value`s)
> need rescaling by ~4x in a dedicated pass. Table 4 (artisans) is unaffected — artisans have
> no template and so no maintenance.

`revenue = value x price(output)`, `cost = sum(qty x price(input))`, per unit of production.
Efficiency and `workforce` are identical across the five templates and do not change the
ordering.

| factory | inputs | cost | output | revenue | margin | ratio |
|---|---|---:|---|---:|---:|---:|
| luxury_factory | light_industry 6 | 30.00 | luxury_industry 25 | 375.00 | +345.00 | **12.50** |
| military_factory | heavy_industry 10 | 50.00 | military_industry 30 | 600.00 | +550.00 | **12.00** |
| food_factory | grain 30 | 72.00 | food_industry 400 | 200.00 | +128.00 | 2.78 |
| heavy_factory | coal 5, iron 2.5 | 44.15 | heavy_industry 20 | 100.00 | +55.85 | 2.26 |
| light_factory | heavy_industry 6 | 30.00 | light_industry 10 | 50.00 | +20.00 | **1.67** |

Five factories, none unprofitable, but a 7.5x spread between best and worst. `food_factory`
is a separate oddity: it emits 400 units of a good priced at 0.5, so world supply of
`food_industry` is two orders of magnitude larger than any other tier and its market price
should collapse to the floor almost immediately, taking the 2.78 ratio with it.

## Table 4 — artisan viability at base prices

11 artisan types; one has a negative margin.

| artisan | revenue | cost | margin |
|---|---:|---:|---:|
| artisan_food_maker | 250.00 | 432.00 | **-182.00** |
| artisan_luxury_maker | 82.50 | 55.00 | +27.50 |
| artisan_furniture_maker | 100.00 | 66.08 | +33.92 |
| artisan_cloths_maker | 118.80 | 79.20 | +39.60 |
| artisan_imports_maker | 126.00 | 84.00 | +42.00 |
| artisan_stimulants_maker | 138.00 | 92.00 | +46.00 |
| artisan_electricity_maker | 144.00 | 96.00 | +48.00 |
| artisan_bronze_maker | 139.25 | 87.30 | +51.95 |
| artisan_steel_maker | 163.50 | 108.99 | +54.51 |
| artisan_military_maker | 400.00 | 337.00 | +63.00 |

`artisan_food_maker` can never break even at base prices; artisans in that type will demote
continuously from turn one. The other ten sit in a tight +27 to +63 band, so artisans are
viable but undifferentiated — the pop AI has little reason to prefer any particular good.

## Table 5 — top event-spam candidates

MTTH <= 3 months, no `fire_only_once`, no `is_triggered_only`, broad trigger, player-facing
(has a `title`). 475 events matched the loose filter; these are the 15 where the trigger is
not obviously self-clearing, ranked by expected frequency. `CleanUp.txt`'s 48 one-month
events are PDM stock and are excluded — their triggers are nation-forming checks that go
false permanently.

| # | event | MTTH | note |
|---|---|---|---|
| 1 | `GreatPowers.txt:2` 800004 | 1 day | ~~flag guard commented out~~ fixed, guard restored |
| 2 | `GreatPowers.txt:78` 800006 | 1 day | ~~same, mirrored~~ fixed, guard restored |
| 3 | `00_CoE_RoI.txt:956` 99988 | 1 month | ~~option does not clear the trigger~~ fixed, once-per-war flag |
| 4 | `GreatWar_Events.txt:363` 96006 | 1 day | "Total Collapse"; guarded by a `great_war*` modifier plus 75% occupation, self-limiting in practice |
| 5 | `Revolution_Nationalism_Event.txt:414` 97180 | 1 day | annexes the province; self-clearing |
| 6 | `Revolution_Nationalism_Event.txt:859` 97185 | 1 day | removes `colonial_chaos`; self-clearing |
| 7 | `Canals.txt:807` 97305 | 3 days | Suez treaty; flag-guarded |
| 8 | `Canals.txt:1589` 97395 | 3 days | Panama treaty; flag-guarded |
| 9 | `CBsAndCores.txt:1191` 2601 | 3 days | removes `core_integration`; self-clearing |
| 10 | `SWHFlavor.txt:52` 900500 | 5 days | Schleswig-Holstein; narrow tag set |
| 11 | `Canals.txt:834` 97310 | 7 days | treaty cancellation |
| 12 | `Canals.txt:1616` 97400 | 7 days | treaty cancellation |
| 13 | `CHIFlavor.txt:5699` 131746 | 7 days | China flavour |
| 14 | `NationalValues.txt:965,1060,1158` 18540/18541/18542 | 10 days | fires for anyone on `nv_progress`; the option changes the NV so it is self-clearing, but it is three near-identical `major = yes` popups per newly-civilised nation |
| 15 | `0_colony_types.txt:381` 999886 | 1 month | 142-token trigger evaluated for every country every month; performance, not spam (already row 3 of the `core-systems.md` performance table) |

Only rows 1-3 were genuine defects; all three are fixed. 4-15 are recorded so a later pass
does not re-derive them.

## Fixed in this pass (2026-09-06)

- `events/GreatPowers.txt` 800004 / 800006 - flag guards restored.
- `events/00_CoE_RoI.txt` 99988 - once-per-war flag plus `months = 1` MTTH; the flag is
  released by 99997.
- `history/countries/AUS - Austria.txt` - 14 -> 19 techs.
- `history/countries/CSA - CSA.txt` - 49 -> 22 techs (the USA's list).
- 13 release tags (BRE, CZH, HOL, LUX, OLD, ORA, PHL, RHI, SAA, SPC, TRN, WES, YUG) -
  24 -> 14 techs; `SPC` prestige 50 -> 0.
- Literacy investigated and deliberately left flat (section above).

## Deferred

- `common/production_types.txt` / `common/goods.txt` factory pricing (Table 3) and
  `artisan_food_maker`'s negative margin (Table 4) - one economy balance pass, shared with
  the `core-systems.md` deferred items.
- `common/cb_types.txt` - 24 event CBs at `badboy_factor = 0` against 7-14x infamy on the
  ordinary CBs; `always = yes` plus `is_triggered_only = yes` on the two
  `east_indian_unification` entries.
- `common/rebel_types.txt` - `defection = none` on five types, the 1-100 `spawn_chance`
  rebase, and `separatist_rebels`' `occupation_mult = 5.0` / `defect_delay = 3`.
- `events/China.txt` 90901 - 100:10 AI weight toward `release_vassal`.
- `history/countries/PER - Persia.txt` - 5 army techs, drop to 3.
