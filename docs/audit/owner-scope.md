# `any_owned` blocks that cannot match in the scope they run in

*2026-09-06. Tool: `scripts/audit_owner_scope.py` (uses `scripts/refcheck.py` for the parser and
the event/decision iterators; ownership from `history/provinces` at the 1821.9.1 bookmark).*

## The defect class

`any_owned` / `random_owned` iterate the **current country scope's** provinces. When the effect
names provinces or cores that this country does not hold, the whole block is a silent no-op - the
engine logs nothing. The Anglo-Afghan chain shipped exactly this: ENG applying `colonial_chaos`
and militancy to Kabul (1209), which stays AFG-owned even while ENG occupies it, and to HND-core
land held by the vassal HND. Fixed in `3b1770e0` by wrapping the blocks in the owner's scope
(`AFG = { capital_scope = { ... } }`, `HND = { any_owned = { ... } }`).

## What the tool checks

For every event and decision whose country scope is statically known - the trigger/potential pins
it with a single top-level `tag = X`, or the block sits inside an explicit `TAG = { ... }` scope -
it collects `any_owned`/`random_owned` blocks whose `limit` *requires* a `province_id` or
`is_core` (conditions inside `OR`, `NOT` or a nested scope such as `owner = { ... }` do not count,
since they are alternatives or exclusions), and asks whether the scoped tag owns any of those
provinces at the start.

Ownership moves during a game, so a hit is only a defect when the scope can never plausibly hold
the land. Each hit is classified:

- **high** - the scoped tag exists in 1821, owns none of the land and has no core on it, the
  event/decision does not gate on owning it, the effects in the block are not one branch of a
  conditional release (no `secede_province`/`release`/`change_tag`/`inherit`/`add_core`/...),
  nothing earlier in the same effect hands the scope new land, and the window is early
  (no year gate, or a year gate before 1850).
- **low** - everything else, with the reason printed per row.

## Results

148 blocks reported over `events/` and `decisions/` (the run below includes the pre-fix
`AFGWarGVG.txt` as a regression check; on the current tree it is 147).

| Verdict / reason | Count |
|---|---|
| **high - unconditional, early window** | **1** (only the already-fixed `AFGWarGVG` 1002301) |
| low - conditional release/secede branch | 120 |
| low - the effect moves land around before this runs | 16 |
| low - the scoped tag does not exist at the 1821 start | 7 |
| low - gated on owning it (trigger has `owns`/`owned_by`/`any_owned`) | 2 |
| low - unowned at start too | 1 |
| low - the scoped tag cores the land | 1 |

**No new high case exists on the current tree, so nothing was changed.** The AFG chain was the
only unconditional instance; everything else is a deliberate "if we happen to hold X, also do Y".

### Regression check

Restoring the pre-fix `events/AFGWarGVG.txt` makes the tool print

```
[high] CoE_RoI_R/events/AFGWarGVG.txt:191  event 1002301 scoped to ENG -> 1209 (owned by AFG)  [unconditional, early window]
```

and the fixed file prints nothing, so the audit does catch the class it was written for.

## Cases inspected by hand (all deliberate)

- `decisions/CLM_irredentism.txt:41-68`, `events/CLMFlavor.txt:699-1062` - GCO releases ECU / DOM /
  PRI / CUB only *if* it holds Quito (2279), Santo Domingo (2214), San Juan (2222), Havana (2209).
  Spain still owns those in 1821, which is exactly why the release is conditional.
- `decisions/China.txt:86,110` - `form_china` releases TIB / MGL only if QNG holds Lhasa (1587) or
  Urga (1465); by then it usually does, and `NOT = { exists = TIB }` guards it anyway.
- `decisions/Italy.txt:1055` - LUC sets its capital to Florence (744) *after* the preceding
  `any_owned = { secede_province = LUC }` has moved Tuscany's provinces to it. Order matters, and
  the tool's "moves land around" rule catches it.
- `events/Oriental Crisis.txt:1382` - TUR agitates EGY-core provinces after `inherit = EGY` in the
  same option, so it owns them by then.
- `events/GreatWar_Events.txt` (96038-96057) - peace-conference options acting on land the victor
  occupied during the war; the province ids sit inside `OR` blocks next to `region = ...`, so they
  are alternatives, not requirements.
- `events/USCAFlavor.txt:1106-1208` - UCA releases PNM / YUC only if it holds 2204 / 2183.
- `events/ACW2_Events.txt:2523` - the Alaskan Convention; the trigger already requires
  `3 = { owned_by = THIS }`, so USA holds the LSK cores when the option runs.
- `events/CANFlavor.txt:1733` - the CNR railway option; trigger requires `owns = 52` and
  `owns = 36`, and the province list is an `OR`.

## Known blind spots

- Only statically pinned scopes are examined. An `any_owned` inside `any_country = { ... }` or
  after a `THIS`/`FROM` switch is skipped.
- Ownership is the 1821 start state only; the tool cannot see conquests, formable-tag events or
  the order of two events firing days apart. That is why the branch/resequencing filters are
  deliberately generous - they trade recall for a list a human can actually read.
- `is_core` hits use "does the scope own **any** province with that core"; a block that needs a
  *particular* core province still slips through.
- Province-scope effect files (`history/`, `common/`) are not scanned.

## Running it

```powershell
python scripts/audit_owner_scope.py
```

Exit code 1 when a high case is found, 0 otherwise. Baseline for the current tree: **147 rows,
0 high**.
