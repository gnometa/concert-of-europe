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
| ~~9-19~~ | ~~9999959-9999969~~ | `+education_RGO.txt` | **0** | **Done** — converted to `is_triggered_only` and dispatched quarterly; see "Education ladder" below. |

Suggested shape for a later pass, in priority order:

1. ~~**`+education_RGO.txt` 9999959-9999969**~~ — **done**, see the next section. Kept as 11
   separate events rather than one branching event, and dispatched quarterly rather than
   yearly.
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

## Education ladder 9999959-9999969 — done (2026-09-06)

### What the eleven steps do

They are **province** events, not country events, and they are a *classifier*, not a random
event. Each one owns one decile of state literacy:

| id | modifier | state literacy | id | modifier | state literacy |
|---|---|---|---|---|---|
| 9999959 | `RGO_education_0` | 0.00-0.10 | 9999964 | `RGO_education_6` | 0.60-0.70 |
| 9999969 | `RGO_education_1` | 0.10-0.20 | 9999963 | `RGO_education_7` | 0.70-0.80 |
| 9999968 | `RGO_education_2` | 0.20-0.30 | 9999962 | `RGO_education_8` | 0.80-0.90 |
| 9999967 | `RGO_education_3` | 0.30-0.40 | 9999961 | `RGO_education_9` | 0.90-0.99 |
| 9999966 | `RGO_education_4` | 0.40-0.50 | 9999960 | `RGO_education_10` | 0.99+ |
| 9999965 | `RGO_education_5` | 0.50-0.60 | | | |

Trigger, identical in shape in all eleven (three clauses):

```
has_global_flag = education_setup
NOT = { has_province_modifier = RGO_education_<N> }
state_scope = { literacy = <lo>  NOT = { literacy = <hi> } }
```

Effect: `state_scope = { any_owned = { remove the other ten modifiers, add
RGO_education_<N> duration = -1 } }` — so although the event fires *on a province*, it
re-stamps **every province of that province's state**, and the remaining provinces of the
state then fail their own `NOT = { has_province_modifier }` clause. MTTH was
`months = 1` on all eleven. (Each also carries ~30 lines of commented-out `life_rating`
inversion code; left untouched.)

### Dispatch chosen

`is_triggered_only = yes` on all eleven, `mean_time_to_happen` removed, **every trigger
clause kept verbatim** (a triggered event's `trigger` is still checked when it is fired).
The dispatch is a new block in the **quarterly** hub `00_CoE_RoI.txt` 99997 (already
`is_triggered_only`, already fired from `common/on_actions.txt` `on_quarterly_pulse`):

```
any_country = {
    limit = { has_global_flag = education_setup }
    any_state = {
        random_owned = {
            limit = { NOT = { has_province_modifier = RGO_education_0 }
                      state_scope = { literacy = 0 NOT = { literacy = 0.1 } } }
            province_event = { id = 9999959 }
        }
        ... x11
    }
}
```

The `has_global_flag` clause is hoisted to the country `limit` (one test per country
instead of eleven); the other two clauses are the province `limit`, in the same
cheap-gate-first order the events already used. No new event id, no `on_actions.txt`
change.

Two details worth recording:

- The dispatch is **per state**, via `any_state = { random_owned = { ... } }`. The event's
  effect re-stamps every province of its state anyway, so firing it once per matching
  province would queue one popup *per province* for a human player — the AI resolves events
  immediately and was therefore self-limiting, the player is not. `state_scope = {
  random_owned = { ... } }` is the vanilla idiom for picking one province of a state
  (`events/TemperanceLeague.txt` 130).
- `province_event` takes the block form `province_event = { id = N }`. The bare-int
  shorthand is documented only for `country_event` (`docs/wiki/list-of-effects.md`), and
  `.cwtools/effects.cwt` defines `province_event` as block-only.

### Rate mapping

| | old | new |
|---|---|---|
| evaluation | 11 triggers per owned province **per day** | 11 `limit`s per owned province **per quarterly pulse** |
| firing | `mean_time_to_happen = { months = 1 }` per province | deterministic, at the pulse |
| state resync latency | ~30/k days for a k-province state (~8-15 days typical) | 0-91 days, ~45 days mean |

**No `random = { chance = X }` was introduced.** The instruction to convert an MTTH into a
per-pulse probability does not apply here: the trigger is a state's own literacy decile,
which does not stop being true if the event does not fire today, so the old MTTH was not a
firing *rate* at all — it was purely a delay before a certain event. Converting it to a
chance would make the classifier stochastic where it was not. (The precedent does exist —
`events/GreatWar_Events.txt` has 11 instances of `random = { chance = N country_event = X }`
inside `any_country` — so this was a choice, not a limitation.) The original MTTH was
≤ 12 months, so per the brief the deterministic conversion is the sanctioned option;
quarterly rather than the yearly suggested above keeps the added latency to a quarter.

The behavioural change is therefore exactly this: **a state that crosses a literacy decile
keeps its previous `RGO_education_*` modifier for up to one quarter instead of up to about
a month.** The set of states, the modifier each ends up with, and the effect body are
unchanged. This is a real, if small, rate change and is documented in a comment header
above 9999969 in `+education_RGO.txt` and above the dispatch block in `00_CoE_RoI.txt`.

### Cost

`audit_perf.py`, whole mod, all self-firing events: **1,092,776 -> 975,655**
clause-evals/day (-117,121, -10.7%). The eleven events are no longer counted at all
(2330 -> 2319 self-firing events). The dispatcher's own work is not in that model: it is
11 `any_owned` passes with a `state_scope` per country per quarter, i.e. the same
~36k clause-evals the ladder used to spend *every day*, now spent four times a year.

`refcheck.py` unchanged at 14/0/60/0/132/0/8 — the eleven are `is_triggered_only` but 99997
fires them, so no new orphans. `audit_events.py` unknown keywords 0; cwtools at baseline.
