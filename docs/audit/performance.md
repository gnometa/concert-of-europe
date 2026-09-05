# Event trigger performance

*2026-09-06. Follow-up to the "Performance: worst 10 always-evaluated events" section of
`core-systems.md`. Scores come from `scripts/audit_perf.py`; run it to reproduce.*

## What the score means

An event without `is_triggered_only = yes` has its `trigger` block evaluated once per scope
per day — once per province for a `province_event` (~2700 owned land provinces), once per
country for a `country_event` (~200 living tags). `mean_time_to_happen` does **not** reduce
that; it only scales the roll *after* the trigger passes (`docs/wiki/event-modding.md`).

The engine evaluates a trigger's clauses top to bottom and short-circuits on the first
failure, so **clause order is the whole game**. `audit_perf.py` models a leaf clause as ~1
unit, an iteration scope (`any_country`, `any_pop`, `any_owned_province`, `any_core`,
`state_scope`, `any_greater_power`, ...) as its expected member count times the cost of its
body, and charges each clause only for the fraction of scopes that got past the clauses
before it. The unit is arbitrary; only the ratios matter.

## This pass: reordering only

**121 events across 26 files** had their top-level trigger clauses re-ordered
cheap-gates-first, iteration-scopes-last. Nothing else changed:

- no condition was added or removed, and no clause was moved into or out of an `OR`/`AND`/
  `NOT` — only the top-level sequence inside `trigger = { }` was permuted;
- no `is_triggered_only` was added and no `mean_time_to_happen` was touched.

Trigger blocks are pure predicates, so a permutation is **rate-neutral by construction**:
the same set of scopes passes on the same days, only the work done to reject the failures
changes. That is the difference from the `Goods.txt` dispatcher attempt recorded under
*Deferred* in `core-systems.md`, which changed conversion rates and was reverted.

Ordering rule applied (stable within each bucket, so unrelated lines do not move):

1. cheap gates — `year`, `always`, `tag`, `exists`, `civilized`, `ai`, `is_greater_power`,
   `has_country_flag` / `has_global_flag` / `has_province_flag`, `province_id`,
   `trade_goods`, `has_province_modifier`, `is_core`, `owned_by`, `controlled_by`, plus
   `NOT`/`OR`/`AND` and single-target scope switches (`owner = { tag = ENG }`) whose whole
   body is cheap gates;
2. everything else, in its original order;
3. anything containing an iteration scope, in its original order.

### Result

| | before | after |
|---|---|---|
| whole mod, all self-firing events | ~1,404,600 | ~1,092,700 |
| the 121 events that were re-ordered | 670,903 | 358,975 |

About a **22% cut** in modelled daily trigger work overall, **-46%** across the events that
were touched. The biggest single wins:

| Event | File | before -> after |
|---|---|---|
| 880010/880020/880030 + 12 more | `events/Ideology_Strongholds.txt` | 13,346 -> 1,241 each |
| 2625, 2610, 2615, 2620 | `events/CBsAndCores.txt` | 36,233 -> 4,725 total |
| 15000-15320 (28 events) | `events/NationalistMovements.txt` | ~4,400 -> ~950 each |
| 46306 (quilombo) | `events/BRZFlavor.txt` | 27,790 -> 5,201 |
| 999886 (colony types) | `events/0_colony_types.txt` | 15,059 -> 6,203 |
| 97181 | `events/Revolution_Nationalism_Event.txt` | 12,069 -> 4,517 |
| 98900/98905 | `events/New Colonies.txt` | 5,501 -> ~915 each |
| 46605 | `events/ARGFlavor.txt` | 2,400 -> 123 |
| 32509 | `events/RUSFlavor.txt` | 1,157 -> 51 |

Full list of files touched: `+education_RGO.txt`, `0_colony_types.txt`, `ACW.txt`,
`ARAFlavor.txt`, `ARGFlavor.txt`, `BRZFlavor.txt`, `BoerWar.txt`, `CBsAndCores.txt`,
`CHIFlavor.txt`, `CivilizationAndGunBoats.txt`, `ColonialSpain_Event.txt`,
`ColonialUprisings.txt`, `ENGFlavor.txt`, `Ideology_Strongholds.txt`, `India.txt`,
`Irish woes.txt`, `NORFlavor.txt`, `NationalistMovements.txt`, `New Colonies.txt`,
`Ottoman_Event.txt`, `RUSFlavor.txt`, `Revolution_Event.txt`,
`Revolution_Nationalism_Event.txt`, `Socialism_Fascism.txt`, `WorkPlaceEvents.txt`,
`crises.txt`.

## Remaining hotspots — these need a design change, not a reorder

Everything below is already ordered as cheaply as its own clauses allow. Cutting them means
changing *what* they test or *how often* they are tested, which changes firing rates, so it
belongs in a separate pass with its own rate check.

| Rank | Event | Where | after | Why it is still expensive |
|---|---|---|---|---|
| 1 | 97175 | `Revolution_Nationalism_Event.txt:364` | 101,020 | 3 clauses, all real work: an `OR` on `is_colonial`/`is_overseas`, then a `state_scope` aggregating every pop in the state. There is no selective gate to hoist. |
| 2 | 31268 | `Ottoman_Event.txt:2938` | 69,151 | 2 clauses only: `owner = { crisis_exist = no ... }` then `state_scope = { any_owned_province = { ... } ... }` — a nested province iteration inside a state aggregate, per province per day. |
| 3 | 130 | `TemperanceLeague.txt:204` | 37,530 | `has_province_modifier = beer_halls` already gates it, but the surviving `state_scope = { any_owned_province = { ... } }` is a nested iteration. |
| 4-5, 8 | 20110/20111/20112 | `crises.txt:356,471,525` | 65,003 | `crisis_exist`/`has_flashpoint`/`flashpoint_tension` are all state- or globe-level. Nothing here is a leaf gate. |
| 6-7 | 98225/98226 | `BoerWar.txt:641,676` | 43,290 | The Great Trek pair. `state_scope = { has_pop_culture = boer }` is the selective test but it is also the expensive one. |
| 9-19 | 9999959-9999969 | `+education_RGO.txt` | ~10,800 each, ~119k total | 11 daily province events each doing `state_scope = { literacy = ... }`. Row 3 of the `core-systems.md` table, still open. |

Suggested shape for a later pass, in priority order:

1. **`+education_RGO.txt` 9999959-9999969** — the cleanest candidate. Collapse the 11 literacy
   buckets into one `is_triggered_only` province event dispatched from `on_yearly_pulse`, with
   the buckets as internal `if`-style branches. The chain is already effectively a ladder, so
   one `state_scope` read per province per year replaces 11 per day. Rate change is real
   (daily -> yearly) and must be signed off, but the mechanic is a state-modifier refresh, not
   a random event, so it is the least rate-sensitive of the group.
2. **`crises.txt` 20110-20112 and `Ottoman_Event.txt` 31268** — flashpoint crises are already
   a slow, once-per-crisis mechanic. A country-scoped `on_yearly_pulse` event that finds the
   flashpoint state once and dispatches `province_event` would remove ~130k/day; the per-
   province MTTH would have to be folded into the pulse period.
3. **`Revolution_Nationalism_Event.txt` 97175 and `TemperanceLeague.txt` 130** — both would
   benefit from a cheap province-level marker stamped once (a province modifier or flag set
   when the colonial/beer-hall condition first holds) so the daily test is
   `has_province_modifier`, and the `state_scope` only runs behind it.
4. **`BoerWar.txt` 98225/98226** — narrowly scoped to South Africa in practice; a
   `province_id` or `region` gate in front of the `state_scope` would be nearly free and is
   arguably still rate-neutral, but it *adds* a condition, so it was left out of this pass.

Rows 1, 2, 4, 7 and 9 of the `core-systems.md` performance table (`Goods.txt` 1107-1138,
`RGOChangeEvents.txt` terrain scans, `0_colony_types.txt`, `CleanUp.txt`'s 48 country events,
`Slave Popsize.txt`) are unchanged in kind by this pass; only their clause order improved.
