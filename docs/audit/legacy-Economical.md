# Legacy audit - events/EconomicalEvents.txt and events/Goods.txt

Scope: the generic economic-cycle chain every civilised country sees (22510-22616) and the RGO
conversion province events (1100-1141) restored to per-province MTTH tonight. Mechanical audits
(braces, encoding, province ids, loc keys, event ids) were clean at baseline; this is a logic pass.

## Clean by construction (checked, no findings)

- **Treasury**: neither file contains a `treasury =` effect or a `money =` *trigger*. The only money
  effect in either file is `money = -50` in a pop scope (22550), far below the +/-2,147,483
  fixed-point cap and unaffected by the mod's inflated goods prices. Nothing to cap.
- **Goods**: every `trade_goods = X` in Goods.txt, effect *and* trigger, resolves to
  `precious_metal`, `oil`, `rubber` or `lead`, all present in `common/goods.txt`.
- **Buildings**: only one building reference exists (`building = railroad`, 22530), which survived
  the tier collapse. No `*_factory` names appear in either file, so the
  `military_/heavy_/food_/light_/luxury_factory_building` rework touches nothing here.
- **Province ids**: all distinct `province_id` values in Goods.txt exist in `map/definition.csv`.
- **Trigger vocabulary**: the bare `stock_exchange = 1`, `keynesian_economics = 1`,
  `combustion_engine = 1`, `mechanized_mining = 1` ... forms all resolve to real *technologies*; the
  four that are inventions (`stock_exchanges`, `private_bank_monitoring`, `hyperinflation`,
  `capital_for_investors`) are correctly written as `invention = X`. No mixed-up pair.
- **Localisation**: every `EVT*` key referenced by either file exists in `localisation/`, including
  the cross-referenced `EVTNAME22560`/`EVTDESC22560` (22600) and `EVTNAME22500`/`EVTOPTA22500` (22605).
- **Modifiers**: all `add_/remove_country_modifier` and `add_province_modifier` names resolve;
  `in_bankrupcy` and `generalised_debt_default` live in `common/static_modifiers.txt`, the rest in
  `common/event_modifiers.txt`.
- **Pictures**: all eight event pictures used resolve in the mod or the game folder.
- **ai_chance**: neither file scripts a single `ai_chance` block, so there are no extremes to
  balance; the AI takes option A everywhere. Design debt, not a defect.

## Findings

`file line id - problem - fix`

### [high]

- `events/EconomicalEvents.txt` 1812 22616 - **repeatable free Bull Market.** 22615 sets `pig_dogs`
  when a country turns communist but *leaves `consumer_confidence` set*; 22616 then clears
  `pig_dogs` on the way back out and grants `Bull_market` for 1825 days while wiping
  `recession`/`stock_market_crash`/`economic_boom`. Because 22615's own trigger only needs
  `consumer_confidence` plus a communist government, the pair re-arms forever: every government
  flip-flop farms another five-year Bull Market, and it was the only event in the chain with no
  `economic_trend` guard, so there was not even the usual one-year cooldown between grants.
  **FIXED** - folded `has_country_modifier = economic_trend` into 22616's existing
  `NOT = { has_country_modifier = great_depression }` block (multi-statement NOT is NOR, so this
  reads "neither depression nor cooldown", the idiom used by 22516/22590/22595/22596/22600/22606).
  The liberation event still fires, but at most once a year, like every sibling.

### [medium]

- `events/EconomicalEvents.txt` 1745 22610 - **`mean_time_to_happen = { months = 1 }` with an
  almost-empty trigger.** Every country gets this within a month or two of researching the
  `stock_exchange` *technology*, and the option hands out `Bull_market` for 1825 days after removing
  `recession`, `stock_market_crash`, `great_depression` and `economic_boom`, i.e. it launders any
  ongoing crisis into a five-year boom. It was also the only event in the chain missing
  `civilized = yes`, and had no `economic_trend` cooldown guard, so it could land on top of an event
  that fired days earlier and silently overwrite it.
  **FIXED** - added `civilized = yes` and folded `has_country_modifier = economic_trend` into the
  existing `NOT = { has_country_flag = consumer_confidence  OR = { government = ... } }` NOR block.
  The `months = 1` and the once-per-game `consumer_confidence` flag are left alone: the event is
  meant to be a one-off "markets open" bonus and its pacing is a balance call, not a bug.
- `events/EconomicalEvents.txt` 132 22516 - **option contradicts its own text.** "Signs of Relief" /
  "It's about time!" removes `great_depression` and immediately adds `stock_market_crash` for 1825
  days. This *is* the intended step-down ladder (depression -> crash -> 22606 recovery), but nothing
  in the title, description or option name tells the player they are trading a ten-year depression
  for a five-year crash. Not fixed: the mechanic is deliberate, the loc text is the thing that is
  wrong, and rewriting `EVTDESC22516` is a localisation job for a separate pass.
- `events/EconomicalEvents.txt` 105 22515 - 22510's option fires 22515 at `any_country`, and 22515
  re-applies `great_depression` for 3650 days with no `economic_trend` check. Harmless today because
  `add_country_modifier` refreshes rather than stacks, but it means the depression's duration is
  reset for every neighbour that later triggers its own 22510. Left as-is: adding a guard would stop
  the depression spreading at all, which is the event's whole point.

### [low]

- `events/Goods.txt` 358 1107 - the rubber event is the only conversion event in the file with no
  `year` gate at all; vanilla had `year = 1880` plus a `year = 1900` fallback. In practice the
  `combustion_engine`/`electricity`/`assembly_line`/`any_greater_power` OR is a de-facto date gate,
  so nothing fires early. Deliberate rewrite (it also gained a `switched_production` guard and the
  `rubber_found` global flag), so no change, but it is the one event whose pacing is implicit.
- `events/Goods.txt` 4/285 1100, 1105 - `year = 1821` is not a bug: the mod shifts vanilla's
  `year = 1836` start-date anchors by -15 years to match the 1821.9.1 bookmark. All other gates
  (1848, 1850, 1861, 1867, 1874, 1886, 1890, 1896 ...) are unchanged from vanilla, which is correct
  since those are historical dates rather than start-date anchors. Verified against the vanilla file.
- `events/Goods.txt` 4 1100 - `gold_rush` and `switched_production` run 365 days here versus 1825 in
  every sibling, across the largest province list in the file (22 provinces). Vanilla used 730 for
  `gold_rush` and had no `switched_production`, so this is a deliberate rebalance, not drift.
- `events/Goods.txt` 4/285 1100, 1105 - lack the
  `NOT = { has_province_modifier = switched_production }` guard that 1107/1108 carry. Safe in
  practice: `NOT = { trade_goods = precious_metal }` already prevents a re-fire once converted.
- `events/EconomicalEvents.txt` 503 22570 - options are declared `EVTOPTB22570` then `EVTOPTA22570`.
  The engine keys on the explicit name so the text is right; only the A/B naming is inverted.
- `events/EconomicalEvents.txt` - 22510, 22515, 22516, 22590, 22591, 22595, 22596, 22600, 22606,
  22610, 22615, 22616 all use hard-coded English option/title strings instead of loc keys. Legacy
  PDM style, renders fine, but invisible to `modcheck loc-find` and untranslatable.
- `events/Goods.txt` - six events carry `picture = ""`. Vanilla does the same in five places, so the
  engine tolerates it; those events simply render with no illustration.

## Permanent modifiers

Only one event in either file stacks a permanent (`duration = -1`) modifier: 22540 applies
`local_stock_exchange` to a random owned non-colonial province. It is guarded by
`set_country_flag = local_stock_exchange_built`, checked in its own trigger, so it can never apply
twice to the same country. No unguarded permanent stacking anywhere else.
