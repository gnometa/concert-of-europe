# Legacy audit — WorkPlaceEvents.txt / WorkPlaceEvents_triggers.txt

Universal workplace/industrial content: 27 country-scope dispatchers (`_triggers.txt`,
ids 12000-12280, all gated on `has_country_flag = economy_pulse_host`) that pick a random
country + a random owned province and fire the matching province event in
`WorkPlaceEvents.txt` (ids 12001-12281, plus the self-firing 12010/12011/12100).

Line numbers are post-fix unless the entry says "was". Fixed entries are marked **[fixed]**.

## [high]

- `WorkPlaceEvents_triggers.txt` all 27 events — **[fixed]** — 34 dispatch sites wrote
  `province_event = { id = 120x1 }` and only *then*
  `add_province_modifier = { name = futile duration = 1 }`. An event effect with no `days`
  fires inline, so the whole "re-find the province by its `futile` marker" idiom that every
  province event in `WorkPlaceEvents.txt` is built on saw the marker as not yet applied:
  every `random_owned = { limit = { has_province_modifier = futile ... } }` branch (the
  dominant-issue/safety-reform payload, ~60 blocks) was dead. Fix: emit the modifier before
  the event at all 34 sites. Safe under either ordering semantics — `duration = 1` still
  covers the next day.
- `WorkPlaceEvents_triggers.txt` 12060, 12070, 12240, 12250, 12260, 12270 — **[fixed]** —
  the `random_country` limit of every option contained an `OR = { }` whose only members were
  commented-out `#any_state = { #has_building = food_industry_factory }` lines (the factory
  types were collapsed to the five `*_factory_building` entries in `common/buildings.txt` by
  the Roar of Industry rework and never re-mapped). An empty `OR` is **false**, so
  `random_country` matched nobody and these six dispatchers — Feed the Hungry Soldiers,
  Old Canned Food, The Drunk Fool, Explosives Explode, Elegant Furniture, Fashion Fails —
  could never fire. 30 empty `OR`/`NOT`/`any_state`/`state_scope` blocks removed (the same
  scaffolding also left empty always-true blocks in 12030/12040/12160/12280).
- `WorkPlaceEvents.txt` 1074, 1152, 1275 (was 1074/1151/1273) — **[fixed]** — 12171 option B,
  12181 option A and 12201 option A ran four `random_owned` blocks directly at option scope.
  The option root of a `province_event` is a province; `random_owned` is a country-scope
  iterator, so all twelve blocks were no-ops. Wrapped each run in `owner = { ... }`, matching
  the sibling options in the same events.

## [medium]

- `WorkPlaceEvents.txt` 1044 (was 1043) — **[fixed]** — 12171 option A's fourth branch used
  `random_state` where its three siblings use `random_owned`, with a province-scope
  `has_province_modifier = futile` in the limit. Changed to `random_owned`.
- `WorkPlaceEvents_triggers.txt`, 41 remaining `#has_building` comments — the dispatchers no
  longer check that the target province has any factory at all: "Boiler Explodes",
  "Cistern Explodes", "Quality Problems" etc. now fire in a random province of a random
  civilized country. Not fixed here because restoring the gate changes event frequency
  materially and needs an in-game pass. Mapping if it is restored:
  `military_industry_factory` -> `military_factory_building`,
  `food_industry_factory`/`fish_cannery`/`bakery`/`fruit_cannery` -> `food_factory_building`,
  `light_industry_factory` -> `light_factory_building`,
  `luxury_industryry`/`*_distillery` -> `luxury_factory_building`,
  `heavy_factory_building` (already the live name, commented out for no reason).
- `WorkPlaceEvents.txt` 696 — 12111 "In Them Old Cotton Fields" option B:
  `owner = { random_country = { limit = { neighbour = THIS } ... relation = { who = THIS } } }`.
  `THIS` is the event root, which for a `province_event` is the province, so the neighbour
  test and the relation effect are being handed a province. Either branch is at best a
  no-op. Fix: make the giver explicit, e.g. hoist to a country event, or replace with
  `owner = { any_neighbor_country = { limit = { civilized = yes } ... } }` and accept the
  all-neighbours spread.
- `WorkPlaceEvents.txt` 100, 306, 967, 1352 (pattern, ~20 sites) — many options apply the
  pop effect at *country* scope (`owner = { labourers = { consciousness = 4 } }`,
  `owner = { any_pop = { consciousness = 2 } }`) for what the text describes as one mine or
  one factory burning down. `consciousness = 6` nationwide (12001B, 12021, 12151B) is a
  large share of the 0-10 range from a single local accident. Preferred form is the
  `state_scope = { ... }` used elsewhere in the same file. Left alone: it is uniform legacy
  behaviour across the whole file and rebalancing it is a design pass, not a bug fix.
- `WorkPlaceEvents.txt` 638-664 — 12100 "A Cure!": option A removes `silk_famine` from the
  event province only, option B removes it from *every* province in the country and charges
  50000. Fine as written, but option A's follow-up (`any_pop` at province scope) and option
  B's (none) make A strictly better for a one-province outbreak; check the loc text sells
  the national scope of B.
- `WorkPlaceEvents.txt` 1332 (was ~1330) — 12201 "Tragedy at the Mine" option A gives
  `owner = { iron = 200 }` (a *gain* of iron) on the option that also raises labourer
  militancy; option B loses 200 iron. Verify against `EVTOPTA12200`/`EVTOPTB12200`: if the
  text is "keep the pit working" / "close it", the signs are right; if reversed, swap them.

## [low]

- `WorkPlaceEvents_triggers.txt` 66-104 — 12000's "Target Acceptable Safety" and "Target Low
  Safety" options carry `ai_chance = { factor = N modifier = { factor = 0 NOT = { year = 1890 } } }`,
  so before 1890 only the trinket/no-safety options are reachable. Deliberate (high safety
  regs barely exist early) but it is the only dispatcher that does this; the other 26 leave
  all options live from 1821.
- Unlocalised option names: 21 options use raw English strings
  (`"Target No-Safety"`, `"That sounds terrible..."`, `"Money, my dear, does not stink!"`).
  They render literally, so they only look wrong next to the `EVTOPTA*` neighbours.
- Loc key drift: 12001 uses `EVTNAME12000`/`EVTDESC12000` (the dispatcher's keys), 12011
  reuses 12010's title, desc and both option names, and most province events pair
  `EVTNAME120x0` with `EVTDESC120x1`. Nothing is missing, but a key edit will hit two events.
- `WorkPlaceEvents.txt` 606 — 12100 has no `picture`, so it falls back to the engine default
  while every other event in the pair of files sets one.
- `WorkPlaceEvents.txt` 12161/12231 — event comments say "heavy_industry"/"light_industry"
  but the loc reads "Standard $PROVINCENAME$ Cement" / "Radio $PROVINCENAME$"; correct under
  the reworked goods list, just confusing when grepping.
- No repeat guards anywhere in either file, by design: the dispatchers are MTTH-driven on a
  single host country and the province events are `is_triggered_only`, so `fire_only_once`
  (which is engine-wide, not per country) is correctly absent.

## Verified after the fixes

`modcheck braces` 2 files ok; `refcheck` 14/0/60/0/125/0/8 (unchanged);
`audit_events` unknown 0, [high] 0; `cwtools_check` at baseline (12 production_types
CW242 + CBsAndCores:2467 + Indochina:188). Both files remain ASCII with CRLF.
