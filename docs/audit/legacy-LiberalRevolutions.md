# Legacy review: `events/LiberalRevolutions.txt` (the 1848 machinery)

*2026-09-06. Line-by-line logic review of all 33 events (10000-10330). Line numbers are
post-fix. Mechanical baselines (refcheck 14/0/60/0/128/0/8, audit_events unknown 0 / high 0,
cwtools 0 errors / 14 known warnings) are unchanged by the edits below.*

## Chain reachability from the 1821 start

Traced and sound: 10001 (`year = 1840`, literacy 0.20 or AUS/KUK/SIC/MOL/WAL) sets
`liberal_revolution_in_progress` -> every flavour event (10105-10170, 10250, 10270) hangs off that
flag -> 10000 Springtime (`year = 1847`, mtth collapses to ~0.4 months once
`liberal_revolutions_should_now_fire` is global) -> `springtime_of_nations` (365 d) ->
10050/10051 close it out. No year window is impossible from 1821 and nothing in the chain assumes
the 1836 vanilla start. The non-flag entry points (10100 blight, 10230 cholera, 10180,
10280-10330) are ungated by year but gate on province modifiers or literacy, so they cannot
pre-empt 1848.

## Findings

| line | id | problem | fix |
|---|---|---|---|
| 3717, 3764 | 10221 | **[high]** the event fires for `tag = ENG` **or** `tag = ENL`, but both options ended `random_owned = { limit = { province_id = 300 ... } change_controller = ENG }`. Playing England (ENL), retaking London hands it to a different tag instead of the recipient. 10229 already uses the right idiom. | **fixed**: `change_controller = THIS` (matches 10229 at 4441/4483). |
| 3864, 4007 | 10225 | **[high]** dead branch. Options 1 and 3 ("restore order" / "throw off Hapsburg rule") did `any_owned = { limit = { culture = north_italian } add_province_modifier = liberal_agitation }`. Sub-cultures live in the pop **religion** field, so no province is ever `culture = north_italian`: Lombardy-Venetia never caught the 1848 unrest in two of the three branches, while option 2 (line 3952) tests it correctly with `has_pop_religion`. | **fixed**: `limit = { has_pop_religion = north_italian }` (valid in province scope, matches option 2). |
| 1601-1615 and 6 more | 10150 | **[medium]** the rebuilt "state is industrialised" OR blocks name the right five buildings (`military/heavy/food/light/luxury_factory_building` all exist in `common/buildings.txt`), but that file also defines independent `...2` and `...3` variants with the same `production_type` and `default_enabled = yes`. `has_building` matches the building key, so a state built out of tier-2/3 factories failed the check and the Luddite Mob could never fire there. | **fixed**: all 7 blocks (trigger, 4 mtth modifiers, both option limits) now list all 15 names. |
| 866 | 10110 | **[medium]** option B applied `scaled_militancy` directly in `random_state` scope - the only site in the file that does not wrap it in `any_pop` (cf. 2953, 3121, 2745). A no-op if the engine rejects the shorthand, identical if it does not. | **fixed**: wrapped in `any_pop = { ... }`. |
| 5200 | 10330 | **[medium]** the `great_reform_act` reader (flag set by `ENGReformGVG.txt:147,222`) uses `factor = 1.25`, i.e. passing the Great Reform Act makes Chartist rallies *rarer*. Historically Chartism was the answer to the 1832 Act's failure to enfranchise workers, and the mtth already rewards actual franchise width elsewhere. | direction is a design call, so **not changed**; use `factor = 0.8` if the intent is "the Act stoked Chartism". |
| 5330-5356 | 10330 | **[medium]** option B ("Let the boys in blue have their way") runs three *independent* `random_state` blocks with no exclusion, so one state can be drawn three times and take `reduce_pop = 0.99` plus `militancy = 4` three times (+12 militancy). Neither option has `ai_chance`, so the AI massacres its own pops half the time, on a 240-month pulse that needs no revolution flag. | balance only, **not changed**: add `ai_chance` (A ~80 / B ~20) and an exclusion between the draws. |
| 585-660 | 10105 | **[low]** same duplicated-episode shape - three identical `random_state` limits can pick one state three times and stack `liberal_agitation` (730 d) on it while the rest of the country is untouched. Also in 10130, 10140, 10160 (two blocks each). |
| 375 vs 446 | 10051 / 10050 | **[low]** ending the revolution by *conceding the franchise* pays `prestige = 5`; letting `springtime_of_nations` simply expire pays `prestige = 15`. The do-nothing exit is three times more rewarding. |
| 31, 220 | 10001 / 10000 | **[low]** 10001 is blocked by `NOT = { has_global_flag = liberal_revolutions_should_now_fire }`, which the first country's Springtime sets. Any nation not already `liberal_revolution_in_progress` at that instant (late civilisers, low-literacy states) is locked out of the whole chain forever. Reads as deliberate ("1848 happens once"), but it makes ~25 flavour events unreachable for most of the map after 1848. |
| 4554, 4567 | 10230 | **[low]** `random_province` at country scope is undocumented in `docs/wiki/list-of-scopes.md`, but vanilla `LiberalRevolutions.txt`, `EconomicalEvents.txt` and `IssueSuggestion.txt` all use it, so it is engine-supported and was **not** rewritten to `random_owned`. It does let the cholera seed land in a colony. |
| 4511-4620 | 10230 / 10240 | **[low]** magnitudes invert as the epidemic spreads: the seed province gets 180 d (small) or 365 d (big), while a *neighbour* infected by 10240 gets 365 d or **730 d** at 50/50. Each mtth is 240 months, so it creeps rather than runs away. |
| 4517, 4530 | 10230 | **[low]** "Quarantine the province" costs consciousness (+2) while "How bad could it get?" *calms* pops (-2). Read as a deliberate act-now-pay-politically trade-off: 10100 (potato blight - "Spare no effort" costs prestige and +3 consciousness, "Let them eat cake!" costs nothing) has the same shape, so both were left alone rather than "corrected" twice over. |
| 4353-4506 | 10229 | **[low]** `ai_chance = { factor = 100 }` vs `factor = 0`: the AI always takes the March-revolution reforms and never "make promises, but work to undermine them". Intentional-looking (10225 option 3 uses `factor = 0` the same way for a tag switch) but it removes all variance from the Prussian 1848. |
| 3789-3985 | 10225 | **[low]** 95/5 AI split on crush-vs-release; option 2's modifiers reach ~20/95 when Austria is occupied or at war with a great power, so it is not a hard lock. Noted as the file's other hard-coded split. |
| 3007-3033 | 10205 | **[low]** three options, no `ai_chance` on any of them, so "Fighting in the Streets" resolves punish-liberals / punish-reactionaries / neither uniformly, whatever the ruling ideology. |
| 3121, 2745 | 10210 / 10200 | **[low]** compounding militancy with no decay: 10210's single option is `any_pop = { militancy = 3 }` plus `scaled_militancy 6` for liberals state-wide, and it re-arms as soon as `liberal_agitation` returns. The only sinks are 10050, 10051, 10220, 10221 and 10229. |
| 5117 | 10310 | **[low]** event id 10310 uses `EVTNAME10320` / `EVTDESC10320` / `EVTOPTA10320` / `EVTOPTB10320`. The keys exist and no event 10320 exists, so it renders correctly; it is a naming trap for the next editor, not a bug. |
| 4012 | 10226 | **[low]** `set_country_flag = reclaimed_croatia` duplicates `decisions/HUN.txt:87`, whose own `potential` (`HUN.txt:70`) then blocks the decision. Harmless, but the flag now has three writers (also `GreatWar_Events.txt:5939`). |
| file-wide | - | **[low]** ~20 `controlled_by = THIS` uses sit in this file's **province** events (10170, 10200, 10210, 10216, 10220), where `THIS` is the province rather than a country. The idiom is inherited from vanilla PDM and appears 207 times mod-wide, so it wants one mod-wide decision, not a per-file rewrite. |

## Checked and clean

- Every multi-statement `NOT` in the file (10001:23, 10130:1131, 10140, 10225:3818, 10240:4595,
  10300:5046, plus the `any_core` filters in 10215/10216) reads correctly as NOR: each is an
  exclusion list where "none of these" is the intent.
- `THIS` in nested scopes: 10150's `any_state = { any_owned_province = { controlled_by = THIS } }`
  and 10226's `AUS = { truce_with = THIS }` both resolve to the event root, as intended.
- Owner scope (the `docs/audit/owner-scope.md` class): no `any_owned` / `random_owned` block here
  acts on land the scoped country cannot hold. 10221 and 10228 hard-code provinces 300 (London)
  and 375 (Amsterdam), both correct in `map/definition.csv` and owned by the scoped tag; 10225
  gates on `owns = 641` (Budapest) and region `AUS_771` (Croatia, `map/region.txt:363`).
- Flag lifecycle: `liberal_revolution_in_progress` -> `liberal_revolution_fired` ->
  `had_liberal_revolution` is closed on all five exits (10050, 10051, 10221 opt A, 10229 opt A,
  with 10050 as the catch-all after 10221 opt B / 10229 opt B). `global_liberal_agitation` and
  `springtime_of_nations` are removed on every path that sets `had_liberal_revolution`.
