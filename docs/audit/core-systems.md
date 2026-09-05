# Core scripted systems audit

*2026-09-06. Read-only audit of the Roar of Industry economy rework and the systems around
it. Line numbers are 1-based against the files as they stand in `master` (cab739e0).
Event-id references, modifier names, loc keys and orphans are covered by
`scripts/refcheck.py` and are not repeated here.*

## What is actually live

The mod ships **one live economy stack and four dead shadow copies of it**. Live: the
quarterly maintenance hub `00_CoE_RoI.txt:523` (id 99997, `is_triggered_only` + fired from
`common/on_actions.txt` `on_quarterly_pulse`) which is the only dispatcher in the whole
rework; the canal/infrastructure pulse `Canals.txt` 97200/97250/97350 off `on_yearly_pulse`;
the trade-goods switcher `Goods.txt` (42 province events, ids 1100-1141, MTTH-driven); the
RGO technology spread `RGOSpreadEvents.txt` (11 events, 29900-29907, adds
`local_tractors`-style province modifiers); the education/RGO chain `+education_RGO.txt`
(999958 setup + 11 province events 9999959-9999969); `0_colony_types.txt`,
`Slave Popsize.txt`, `WorkPlaceEvents*.txt`, `CleanUp.txt` and `OnAction.txt`. Dead:
`+demand.txt` **and** `industrial_demand.txt` are two commented-out copies of the same 29
events on the same ids 999971-999999 (one country-scoped, one province-scoped);
`+education_RGO1.txt` and `+education_RGO2.txt` are two commented-out earlier drafts of
`+education_RGO.txt`; `0_demographic_transition.txt` and `0_demographic_transition2.txt` are
**byte-identical** and 100% commented out, as is `population trends.txt`; `+education_RGO_b.txt`
holds Education Setup I (9999856), reachable only from `decisions/00_setup_decisions.txt`
which is `always = no`. `RGOChangeEvents.txt` is half-dead: 199000/199001 are killed by
`always = no` but the other 22 mine-depletion events are live and overlap `Goods.txt`.

## Defects

### [high]

`CoE_RoI_R/events/money.txt:3` — `id = 99999999999` exceeds the engine's signed 32-bit event
id range (max 2147483647); it will wrap or be rejected at parse. The trigger also uses
`TAG = HAW` (uppercase `TAG` is not a trigger; the condition is `tag = HAW`), so the event is
either an error-log entry or silently never fires. *Fix:* give it an id from a registered
range (`modcheck next-id`), lowercase `tag`, and register it in `events/GVG Event IDs.txt` —
or delete the file, since a one-off 50k-100k handout to every country is not obviously wanted.

`CoE_RoI_R/events/00_CoE_RoI.txt:531` — the entire economy-maintenance system hangs off
`trigger = { tag = BHU }`. The same is true of `+education_RGO.txt:12`,
`WorkPlaceEvents_triggers.txt:11` and the 99992-99999 block. If Bhutan is annexed (very likely
by 1860 in any game where China or Britain expands), the quarterly pulse stops doing anything:
pop-type conversion, the money sink, the state-population display modifiers and the ghost-unit
cleanup all silently die. *Fix:* move the dispatcher to a tag-independent host — fire 99997
from `on_quarterly_pulse` without a tag gate (it is already `is_triggered_only`, so gate it on
a per-quarter global flag instead), or guarantee BHU survives as a shell tag.

`CoE_RoI_R/events/00_CoE_RoI.txt:594-624` — the pop-type rewrite (`aristocrats -> farmers`,
`00_urban_poor -> craftsmen`, `clergymen -> clerks`, colonial non-accepted
`bureaucrats -> capitalists`) runs over `any_country = { any_pop = { ... } }` **every quarter,
forever**, with no flag and no cap. It is also duplicated: the identical four blocks appear
once in the BHU scope at lines 556-591 and again inside `any_country` at 592-626. This
permanently deletes the aristocrat and clergy pop types from the game world four times a
year. *Fix:* if this is a one-time start-of-game migration, move it into the 2000000-range
setup events in `decisions/SetupGVG.txt` and gate it on `has_country_flag = setup_done`; if it
is meant to be continuous, at minimum delete the duplicated top-level copy.

`CoE_RoI_R/events/00_CoE_RoI.txt:538-540` — the treasury sink:

```
any_country = { limit = { money = 100000000 } treasury = -50000000 }
any_country = { limit = { money = 200000000 } treasury = -100000000 }
any_country = { limit = { money = 300000000 } treasury = -100000000 }
```

These are cumulative, not exclusive: a country holding 300M loses 250M in a single quarter.
It is an anti-hyperinflation drain for the AI, but the brackets are unbounded above (10bn is
still only -250M/quarter, so it never converges) and it hits the human player with no
notification. *Fix:* make the brackets mutually exclusive with `NOT = { money = ... }`, add a
proportional top bracket, and exclude `ai = no` or surface it as a visible event.

`CoE_RoI_R/common/production_types.txt:4-255` — the `efficiency` blocks in the five factory
templates are calibrated against a price table that no longer exists. The inline annotations
(`coal = 15.0 #3.45$`, `timber = 12.5 #0.27$`) imply coal at ~0.23 and timber at ~0.02 per
unit; `common/goods.txt` now prices them at 5.14 and 2.88 — 20x to 130x higher, and
inconsistently so between goods. Priced at the current table, a fully supplied factory's
efficiency inputs cost 3x to 8x its gross revenue (see table below). *Fix:* rescale each
template's efficiency block against the current price of the good, or re-derive the numbers
from a target cost-of-efficiency budget and update the `$` comments in the same pass.

### [medium]

`CoE_RoI_R/events/+demand.txt` + `CoE_RoI_R/events/industrial_demand.txt` — two full copies of
the consumption-growth system on the same ids 999971-999999, both entirely commented out. They
are a latent duplicate-id crash: uncommenting either one is safe, uncommenting both gives 29
duplicate ids. *Fix:* delete one file outright (`industrial_demand.txt`, the province-scoped
variant, is the newer of the two judging by its `EVTNAME999999` loc keys) and keep the other
as the single dead-but-recoverable copy.

`CoE_RoI_R/events/0_demographic_transition2.txt` — byte-identical to
`0_demographic_transition.txt` (md5 `8af318cc...`), both 1286 lines and 100% commented out.
*Fix:* delete `0_demographic_transition2.txt`.

`CoE_RoI_R/events/+education_RGO1.txt`, `+education_RGO2.txt` — 24 commented-out events on
ids 99958 and 999959-999969, superseded by `+education_RGO.txt` (which uses 999958 and
9999959-9999969, one digit longer). The near-miss between `99958`/`999958` and
`999969`/`9999969` is exactly the kind of typo that produces an unreachable event. *Fix:*
delete both files.

`CoE_RoI_R/events/RGOChangeEvents.txt` vs `CoE_RoI_R/events/Goods.txt` — two mechanics both
change `trade_goods` on the same provinces with no shared lock. `Goods.txt` guards itself
with `NOT = { has_province_modifier = switched_production }` and applies that modifier for
365 days; the 22 live `RGOChangeEvents` (199005-199042) do not check or set it, so a mine can
be converted to `grain` by 199005 the day after `Goods.txt` 1103 turned it into coal. *Fix:*
add `NOT = { has_province_modifier = switched_production }` to the RGOChange triggers and have
their options apply the same modifier.

`CoE_RoI_R/events/RGOChangeEvents.txt:12` and `:76` — 199000/199001 are disabled with
`always = no` inside the trigger while their 22 siblings run. Nothing records why. *Fix:*
either delete the two events or add a comment; if `always = no` was a debug switch, the same
argument applies to the siblings.

`CoE_RoI_R/events/Slave Popsize.txt:16-27` — `add_country_modifier = { name = slavepopupdated
duration = 365 }` is applied in both `immediate` and `option`, so the cooldown is set twice
per firing (the second application resets the timer). Harmless today because the durations are
equal, but it makes the `immediate` block dead weight and the pattern is copied across all
five events 500000-500004. *Fix:* keep the `immediate` copy only.

`CoE_RoI_R/events/00_CoE_RoI.txt:628-720` — the state-population display runs six
`any_country = { any_owned = { ... } }` passes per quarter, each removing all six
`s_pop_*` province modifiers before adding one. That is up to 36 modifier removals per
province per quarter across every province in the world, purely to drive a UI label.
*Fix:* only reshuffle provinces whose bucket changed (test the current modifier in the
`limit`), or drop to `on_yearly_pulse`.

### [low]

`CoE_RoI_R/decisions/00_setup_decisions.txt:4` — `development_setup_decision` is `always = no`
in both `potential` and `allow`, and its only effect is `country_event = 9999856`. It is the
sole caller of Education Setup I. *Fix:* see "Is the education chain reachable" below.

`CoE_RoI_R/common/on_actions.txt` — 60+ commented-out entries (all of `on_election_tick`,
most of `on_quarterly_pulse`) with no comment saying whether they were disabled for
performance or because the events were removed. *Fix:* strip the dead lines; git has them.

`CoE_RoI_R/events/+education_RGO.txt:768-1958` — every one of the 11 province events carries
~30 lines of commented-out `life_rating` inversion code, identical in each: ~330 dead lines.

## Is the `+education_RGO` chain reachable?

**Yes, and the disabled decision is irrelevant to it.** There are two independent setup events:

- **Setup I** — `+education_RGO_b.txt:8`, id 9999856, `is_triggered_only = yes`, its own
  trigger commented out. Its only caller is `decisions/00_setup_decisions.txt`, which is
  `always = no`. This one is genuinely dead: it sets per-culture starting literacy for ~200
  cultures and never runs. Removing it means deleting `+education_RGO_b.txt` and
  `decisions/00_setup_decisions.txt` together, then re-running `refcheck.py` to catch the loc
  keys and the `Education` picture it orphans. Nothing else references 9999856.
- **Setup II** — `+education_RGO.txt:1`, id 999958, **not** `is_triggered_only`, fires on
  `tag = BHU` + `NOT = { has_global_flag = education_setup }` with `days = 1`. It sets
  `set_global_flag = education_setup` at line 760, which is the gate on all 11
  `RGO_education_*` province events (9999959-9999969). So the RGO-education chain runs from
  day 1 of any game where Bhutan exists at start — which it does.

The trap is that the starting-literacy half of the design (Setup I) never runs while the
literacy-*rewards* half (Setup II plus the 11 province events) always does. If Setup I was
meant to feed the `state_scope = { literacy = 0.1 }` thresholds, the whole chain is currently
being driven by vanilla/PDM literacy instead of the intended distribution.

## Performance: worst 10 always-evaluated events

Baseline: 3304 provinces in `map/definition.csv`, 573 tags in `common/countries.txt`. Any
event without `is_triggered_only` has its trigger evaluated once per scope per day; a
`months = N` MTTH does **not** reduce that, it only scales the roll after the trigger passes.

| # | Where | Scope evals/day | Why it costs | Safer pattern |
|---|---|---|---|---|
| 1 | `events/Goods.txt:358-1870` (1107-1138, 32 events) | 32 x 3304 ~ 106k | Each trigger runs `any_greater_power = { ... }` (8 GPs) **and** `owner = { any_neighbor_country = { ... } }` after a 22-term `province_id` OR: a nested country iteration per province per day | Hoist to a country event on `on_yearly_pulse` that checks the tech once, sets a global flag, and dispatches `province_event` to the listed ids |
| 2 | `events/RGOChangeEvents.txt` (199005-199042, 22 live) | 22 x 3304 ~ 73k | 25-30 `terrain =` comparisons plus `owner = { war = no civilized = yes }` per province; terrain never changes yet is re-tested daily | Collapse the terrain list into one `NOT = { OR = { ... } }` placed first, or stamp a `mineable_terrain` province modifier once at setup and test that |
| 3 | `events/+education_RGO.txt:768-1958` (9999959-9999969) | 11 x 3304 ~ 36k, `months = 1` | `state_scope = { literacy = ... }` aggregates every pop in the state, 11 times per province per day; the winning event then does 11 `remove_province_modifier` over `any_owned` | One dispatcher province event with the 11 buckets as internal branches, fired from `on_yearly_pulse` |
| 4 | `events/0_colony_types.txt` (999886/999888/999889/999890) | 4 x 3304 ~ 13k, `months = 1` | 999886's trigger is 2.6 KB: `unemployment_by_type` twice plus nine `AND` blocks each aggregating `state_scope` *and* `owner` total_pops | Compute the owner's population bucket once per country per year into a variable and compare the variable |
| 5 | `events/RGOSpreadEvents.txt` (29900-29907, 11 events) | 11 x 3304 ~ 36k | Cheap trigger, but each MTTH block is 40-60 `modifier` entries, all evaluated on every trigger pass | Acceptable as-is; collapse the literacy ladder into 3 buckets if it shows up in profiling |
| 6 | `events/Goods.txt:4-356` (1100-1106, 1139-1141) | 10 x 3304 ~ 33k | `year = 1821` is always true, so the 22-term `province_id` OR is fully evaluated every day for every province | Put the cheap `trade_goods` / `has_province_modifier` test first, before the id list |
| 7 | `events/CleanUp.txt` (48 country events, 60000-60160) | 48 x 573 ~ 27k | Triggers are 130-690 chars of culture/religion/state tests; 30 of them are `months = 1` | Batch into one `is_triggered_only` dispatcher on `on_yearly_pulse` |
| 8 | `events/00_CoE_RoI.txt:523` effect body (99997) | 1 per quarter | Cheap trigger, but the *effect* is the most expensive thing in the mod: a global `any_pop` pop-type rewrite plus six `any_country`/`any_owned` modifier reshuffles (see [high] and [medium]) | Split: pop conversion once at setup, display modifiers yearly |
| 9 | `events/Slave Popsize.txt` (500000-500004) | 5 x 573 ~ 3k, `months = 1` | Cheap, but re-fires monthly for every slaveholding country only to re-add its own cooldown modifier | `on_yearly_pulse` |
| 10 | `events/WorkPlaceEvents.txt:605` (12100) | 1 x 3304 | `months = 300` province event that fires ~4 times per game; the daily scan is pure overhead | `is_triggered_only`, dispatched from the country-scoped 12000-series |

## Factory profitability (base prices from `common/goods.txt`)

`rev` = `value` x output good price. `direct in$` = `input_goods` at base price. `eff in$` =
the template's `efficiency` block at base price (an upper bound: efficiency goods are bought
when affordable). All five factories clear their *direct* inputs; none clears direct + eff.

| Factory | Output | value | rev | direct in$ | rev/direct | eff in$ | rev - (direct+eff) |
|---|---|---|---|---|---|---|---|
| `luxury_factory` | luxury_industry | 25 | 375.0 | 30.0 | **12.50** | 339.3 | +5.7 |
| `military_factory` | military_industry | 30 | 600.0 | 50.0 | **12.00** | 442.1 | +107.9 |
| `food_factory` | food_industry | 400 | 200.0 | 72.0 | 2.78 | 872.5 | **-744.5** |
| `heavy_factory` | heavy_industry | 20 | 100.0 | 44.1 | 2.27 | 409.4 | **-353.5** |
| `light_factory` | light_industry | 10 | 50.0 | 30.0 | **1.67** | 403.8 | **-383.8** |

Two problems fall out of this. First, the direct-margin spread is 7.5x between
`light_factory` (1.67) and `luxury_factory` (12.50): the AI will build luxury and military
factories to the exclusion of the light and heavy factories those two depend on
(`military_factory` eats `heavy_industry`, `luxury_factory` eats `light_industry`), so the
supply chain starves its own top end. Second, the efficiency blocks are priced for a different
goods table (see [high] above) and make `food_factory`, `heavy_factory` and `light_factory`
loss-making the moment efficiency inputs are available. Raising `value` for `light_factory`
and `heavy_factory` — or lowering `cost` for `luxury_industry` and `military_industry` in
`common/goods.txt` — is the smallest change that fixes the first problem; the efficiency
rescale is a separate pass.

RGO gross revenue at base price ranges from 6.0 (`silkworm_ranch`, silk) to 100.0
(`precious_metal_mine`), with most in the 12-32 band. `silkworm_ranch` (6.0) and
`tea_plantation` (8.0) are outliers at roughly half the next-lowest (`lead_mine`, 9.4) and are
worth a look, but nothing there is broken.

## Fixed / Deferred

*Worked through on 2026-09-06, after the audit above was written. The line numbers in the
sections above still refer to `cab739e0` and are now stale for the files listed here.*

### Fixed

- **`events/money.txt` (id 99999999999, `TAG = HAW`)** — deleted. It was a one-off debug
  handout (50k to every country, 100k to every great power, MTTH 1 day) with an out-of-range
  id and a non-existent trigger; nothing referenced it and nothing wanted it.
- **The Bhutan gate** — `tag = BHU` is replaced everywhere it was acting as a
  "run this global effect for exactly one country" host by the country flag
  `economy_pulse_host`. Two new events in `00_CoE_RoI.txt` maintain it: **2000100**
  (election, daily, O(1) trigger `NOT = { has_global_flag = economy_pulse_lock }`) and
  **2000101** (watchdog, `is_triggered_only`, added to `on_yearly_pulse`, clears the lock
  when no country carries the flag any more so 2000100 elects a replacement the next day).
  Consumers converted: `00_CoE_RoI.txt` 99997, `+education_RGO.txt` 999958 (Education Setup
  II), and all 27 dispatchers in `WorkPlaceEvents_triggers.txt` (12000-12780). The pattern is
  documented in a comment block above 2000100. Exactly one country is still evaluated per
  day, so every `mean_time_to_happen` rate is unchanged; the difference is that annexing
  Bhutan no longer silently switches the economy rework off. `bhu_paradise` in 999958 is now
  applied inside an explicit `BHU = { ... }` scope, since the host is no longer Bhutan.
  Ids 2000100-2000199 are registered in `events/GVG Event IDs.txt`.
- **Treasury sink (`00_CoE_RoI.txt` 99997)** — the three cumulative brackets became five
  mutually exclusive ones (150M/200M/300M/500M/1000M, each with a `NOT` on the next
  threshold). Each deduction is at most the bracket's lower bound minus a 100M floor, so a
  country loses one bracket per quarter at most and the drain can never push a treasury
  below 100M. Nothing is taken below 150M at all. The top bracket (-900M at 1bn+) makes the
  ladder converge instead of leaving 10bn hoards permanently.
- **Pop-type rewrite (`00_CoE_RoI.txt` 99997)** — the duplicated copy that ran in the host
  country's own scope is removed; the `any_country` copy is kept. It is **intentionally
  continuous**, not a one-off migration: `poptypes/*.txt` still lists `aristocrats`,
  `clergymen` and `00_urban_poor` as live promotion targets (from artisans, craftsmen,
  labourers, clerks and farmers), so pops keep being created in those types every month and
  a start-of-game migration would be undone within a year. That reasoning is now a comment
  in the file, with the condition under which it could be flag-gated.
- **`Goods.txt` 1107-1138** — all 32 province events are `is_triggered_only = yes` with
  their `mean_time_to_happen` blocks removed, and are dispatched from the quarterly hub
  99997. That takes them from ~106,000 nested-country trigger evaluations per day to the
  same number four times a year. Their triggers are untouched and are still checked when the
  event is fired, so eligibility is identical. The per-province MTTH is replaced by three
  `random_owned` rolls per country per quarter (limited to provinces without
  `switched_production`), which keeps conversions trickling in; Victoria 2 has no
  `random = N` trigger and a non-top-level `random_list` returns the same branch for every
  scope, so `random_owned` is the only per-province randomness available.
- **`RGOChangeEvents.txt` vs `Goods.txt`** — the audit above overstated this. 20 of the 22
  live events already carried `has_province_modifier = switched_production` inside a
  multi-statement `NOT`, which *is* a valid guard: Victoria 2's `NOT` with several children
  is a NOR (`docs/wiki/list-of-conditions.md`), not a negated AND. Only 199041 (Intensive
  Farming) was missing it and has had it added. 199042 (Exhausted Farmland) is deliberately
  left unguarded — it only swaps province modifiers and never touches `trade_goods`.
  199000/199001 are left in place with `always = no` and now carry a comment saying they are
  the superseded original of the mechanic.
- **Dead duplicate files** — `git rm`'d: `+demand.txt`, `industrial_demand.txt`,
  `+education_RGO1.txt`, `+education_RGO2.txt`, `0_demographic_transition.txt`,
  `0_demographic_transition2.txt`, `population trends.txt`. All were 100% commented out.
  Their id ranges (999971-999999, 99958/999959-999969, 99902-99904, 2260601-2260607) are
  recorded as reserved in `events/GVG Event IDs.txt` together with a pointer to git history.
  Note 99902 is in live use by `Sepoy rebellion.txt`, so the demographic-transition range
  cannot simply be reused as-is.

### Deferred

- `common/production_types.txt` efficiency blocks and `common/goods.txt` prices — the whole
  factory-profitability section above. Explicitly held back for a balance pass; changing
  either half alone makes the mismatch worse.
- `00_CoE_RoI.txt` state-population display (six `any_country = { any_owned = { ... } }`
  passes per quarter, up to 36 modifier removals per province). Still quarterly, still
  reshuffling every province. The redundant host-scope copy of the same six passes that sits
  after the `any_country` block is also still there.
- `+education_RGO.txt` 9999959-9999969 (11 daily province events with `state_scope`
  literacy aggregates), `RGOChangeEvents.txt` 199005-199042 (22 daily terrain scans),
  `0_colony_types.txt`, `CleanUp.txt`'s 48 always-evaluated country events, and
  `Slave Popsize.txt`'s doubled cooldown — all unchanged. Rows 2-4, 7 and 9 of the
  performance table are still open.
- `+education_RGO_b.txt` (9999856) and `decisions/00_setup_decisions.txt` — the dead
  Education Setup I chain. Left alone; removing it means also cleaning up its loc keys and
  the `Education` picture it orphans.
- `common/on_actions.txt`'s 60+ commented-out entries and the ~330 dead `life_rating` lines
  in `+education_RGO.txt`.
