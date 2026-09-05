# Factory and artisan profitability balance pass

*2026-09-06. Scope: `CoE_RoI_R/common/production_types.txt` only. `common/goods.txt` was
**not** touched. Addresses the [high] `production_types.txt:258-305` finding in
`docs/audit/ai-balance.md` (Tables 3 and 4). **Untested in game — needs a play test.***

## Correction, second pass

The first cut of this pass (and the audit's Table 3) costed factories on `input_goods`
alone and dismissed the template's `efficiency` block as an optional bonus. **That is
wrong.** In Vic2 the `efficiency` block is the factory's *maintenance* goods: the engine
buys them every day and a shortfall cuts efficiency (vanilla's own comment,
`common/production_types.txt:5`, "if no cement, work at 75% efficiency"). Vanilla annotates
factories with `total input+maint`, e.g. `aeroplane_factory` sums its four inputs (80.99)
plus `cement 0.5 x 16.0` plus `machine_parts 0.05 x 36.5` to "= 90". `scripts/balance_factories.py`
now includes maintenance and reports `margin` (revenue - input - maint) as well as the ratio.

This changes the picture completely, because this mod's maintenance blocks are 40-90x
vanilla's:

| | vanilla | this mod |
|---|---|---|
| maintenance cost / level / day | 4.00 - 9.88 | **339 - 872** |
| `input_goods` cost / level / day | 20 - 411 | 30 - 175 |
| factory ratio band (input+maint) | 0.80 - 1.28 | 0.15 - 1.12 |
| factory margin band | -7 to +17 | -745 to +58 |

Vanilla parks every factory just above break-even at base prices. Here maintenance is 70-90%
of total cost, and **`heavy_factory` (0.26), `light_factory` (0.15) and `food_factory` (0.21)
cannot be profitable at base prices under any employment level** — throughput scales inputs
and output together, so it does not close a 4-6x gap. They only run because scarcity pushes
the *output* good's market price far above `cost` in `goods.txt`. That is the mod's real
economic defect and it is **not fixed here**: closing it means rescaling the `efficiency`
blocks (or the output `value`s) by roughly 4x, which moves world supply of every good and
belongs in its own pass with a play test. Logged as a new [high] item in the audit.

What *is* fixed here is that the first cut, optimising the wrong objective, pushed the only
two factories that were above break-even below it.

## Design rules used

1. **Move `input_goods` amounts and `value`, never `goods.txt` prices.** A price change
   ripples into every pop need, RGO income and unit cost; an amount change is local.
2. **Judge a factory by margin including maintenance, not by the `input_goods` ratio.**
3. Keep `military_factory` and `luxury_factory` in vanilla's 1.0-1.3 ratio band while still
   making them the demand sink for `heavy_industry` and `light_industry` — the tier the audit
   found nobody had a reason to build. `military_factory` absorbs 2x the old
   `heavy_industry`; `luxury_factory` absorbs 1.7x the old `light_industry` and its `value`
   rises to pay for it.
4. Employees, owner blocks, workforce, templates, efficiency blocks and the factory list are
   untouched, per the audit's "don't restructure" note.
5. Artisans have **no template and therefore no maintenance**, so the plain input-vs-output
   ratio is correct for them and only the three outliers moved.

## Changes

Ratio = revenue / (input + maintenance). "1st cut" is commit `1005f94e`.

| factory | change | before | 1st cut | now |
|---|---|---:|---:|---:|
| military_factory | `heavy_industry` 10 -> **20** | 1.22 (+108) | 0.97 (-17) | **1.11 (+58)** |
| luxury_factory | `light_industry` 6 -> **10**, `value` 25 -> **29** | 1.02 (+6) | 0.83 (-74) | **1.12 (+46)** |
| heavy_factory | `value` 20 -> 24 | 0.22 (-354) | 0.26 (-334) | 0.26 (-334) |
| light_factory | `value` 10 -> 13 | 0.12 (-384) | 0.15 (-369) | 0.15 (-369) |
| food_factory | `grain` unchanged at 30 | 0.21 (-744) | 0.20 (-780) | 0.21 (-744) |

The `grain 30 -> 45` raise on `food_factory` from the first cut is reverted: it deepened the
worst loss in the file to no purpose.

| artisan | change | before | 1st cut | now |
|---|---|---:|---:|---:|
| artisan_food_maker | grain 60 -> 30, cattle/fish/fruit 30 -> 10 | **0.58** | 1.49 | 1.49 |
| artisan_horsebreeder | grain 3.8 -> **7**, fruit 2 -> **4**, iron 0.5 -> **1.0** | **4.66** | 1.58 | **2.42** |
| artisan_military_maker | sulphur 20 -> 12, `heavy_industry` 45 -> 40 | 1.19 | 1.50 | 1.50 |
| (other eight, unchanged) | — | 1.49-1.60 | | 1.49-1.60 |

`artisan_horsebreeder` is deliberately left as the most profitable artisan rather than
flattened to 1.5x. **No province anywhere on the map has `trade_goods = horses`** (0 of 2,827)
and no event grants one, so artisan horsebreeders are the world's only source of horses —
while every unit in `units/*.txt` burns `horses = 0.10`/day in supply and four of the five
factory templates buy horses as maintenance (`food` 12.5, `military` 7.5, `heavy` 5.4,
`luxury` 1.25 per level per day). Demoting the sole producer to mid-pack risks a world-wide
army-supply squeeze. 2.42x removes the 4.66x outlier without doing that. Note it also carries
`workforce = 5000` (half the other artisans) and `effect_multiplier = 2` on its owner block,
so its per-pop income is about twice what the ratio column suggests.

## Start-state supply, checked

At the 1821 bookmark the world has **376 levels of `heavy_factory` and nothing else** (290
`state_building` blocks across 135 province files, all `heavy_factory_building`). So world
supply is ~9,000 `heavy_industry`/day at full employment, and `light_industry`,
`luxury_industry`, `military_industry` and `food_industry` come **only from artisans** until
someone builds. Pop demand dwarfs that (`heavy_industry` alone is an everyday need of 5-24
per pop type). A single `military_factory` at 20/day is 0.2% of world heavy output, so the
constraint is not "can the world supply one factory" — it is that `heavy_industry` and
`light_industry` sit at their price ceiling for decades, which makes the two end tiers
cost more than the base-price table shows. Hence the conservative 1.1x targets.

## What to watch in a play test

- Whether `military_factory` and `luxury_factory` are still built once `heavy_industry` /
  `light_industry` trade above base price. If not, cut their inputs back toward 15 / 8.
- Whether horse supply holds up: watch army supply/attrition on large AI armies after 1840.
- The maintenance-scale defect above: `light_factory` and `food_factory` will look
  permanently unprofitable in the factory UI. Expected, not caused by this pass.

## Third pass: rescale the `efficiency` (maintenance) blocks

*2026-09-06, same scope. Fixes the [high] the second pass logged and deferred.*

### Semantics, established from vanilla
`efficiency` goods are **maintenance**: bought daily at the **full listed amount per factory
level**, at market price, summed 1:1 with `input_goods` into the factory's cost. Vanilla says
both halves in its own comments. `factory_template` annotates `cement = 0.5 #cost = 16.0` and
`machine_parts = 0.05 #cost = 36.5` "**9.825/day/level for both**"
(`common/production_types.txt:5-7`) — 0.5x16 + 0.05x36.5 = 9.825 exactly: amount x price, per
level, per day, undiscounted. `cheap_factory_template` (`:36`) is `cement = 0.25` = 4.00/day,
and its users are annotated `total input+maint` — `dye_factory` (`:566`) is
`coal 9 #20.7  total input+maint = 24.7`. Shortfall does **not** scale output linearly; it
clamps efficiency to a floor ("if no cement, work at 75% efficiency", `:5`). Consumption is
per *level*, not per employee, so a half-staffed factory pays full maintenance on half the
revenue. The wiki mirror has no production-types page, so vanilla is the source.

### Why this mod's numbers are 40-90x vanilla's

`git log -S"efficiency" -- CoE_RoI_R/common/production_types.txt` returns one commit
(`939ed127`, the rename import); `goods.txt` has the same squashed history, so neither can show
the price change. The evidence is in the file: every maintenance line carries a hand-computed
`#N$` cost that only works against a far cheaper price table — `coal = 15.0 #3.45$` implies
**0.23** vs goods.txt's **5.14** (22x), `horses = 7.5 #0.4$` implies 0.053 vs 6.40 (**120x**),
`cattle = 2.5 #0.04$` implies 0.016 vs 3.20 (**200x**) — and the totals they sum to (military
`#4.387$`, heavy `#6.215$`, food `#4.436$`) sit inside vanilla's 4.00-9.88 band. The blocks
*were* tuned correctly, against prices later raised without retuning. This pass re-tunes them,
rewrites the `#N$` comments to current prices, and adds a
`# total maintenance N$ / level / day` line per block so the next price move is visible.

### Method and result
Target **1.35x** for all five (vanilla parks at 0.8-1.3, but this mod's artisans sit at
1.49-1.60 and factories must not be strictly worse). Budget = revenue/1.35 - input; every good
is scaled by budget/current, so the mix is untouched. Solver: `balance_factories.py --target 1.35`.

| factory | input | revenue | maint before | maint after | scale | ratio before -> after | margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| military_factory | 100.00 | 600.00 | 442.10 | **344.47** | 0.779 | 1.11 -> **1.35** | +155.53 |
| luxury_factory | 50.00 | 435.00 | 339.32 | **272.41** | 0.802 | 1.12 -> **1.35** | +112.59 |
| food_factory | 72.00 | 200.00 | 872.45 | **76.17** | 0.087 | 0.21 -> **1.35** | +51.83 |
| heavy_factory | 44.15 | 120.00 | 409.35 | **44.68** | 0.109 | 0.26 -> **1.35** | +31.17 |
| light_factory | 30.00 | 65.00 | 403.76 | **18.15** | 0.045 | 0.15 -> **1.35** | +16.85 |

The remaining spread (military 344 vs light 18) tracks revenue, which tracks output prices
(`military_industry` 20.0, `luxury_industry` 15.0, `heavy`/`light` 5.0, `food_industry` 0.5).
No `value`, `input_goods`, employee, owner or workforce entry moved. The **376 `heavy_factory`
levels at the 1821 start** are the point of the pass: they lost 333.50/level/day at base
prices and now clear +31.17, so the AI's only industry is solvent from day one.

### What to watch in a play test

- **Raw-goods demand drops hard.** Those 376 heavy levels bought ~154,000/day of coal, iron,
  copper, lead, sulphur, timber, oil, rubber and horses; now ~16,800, and `horses`
  (artisan-only) loses its largest buyer. If RGOs stagnate, raise `value` on the raw tiers
  rather than re-inflating maintenance.
- 1.35 is a *base-price* figure. `heavy_industry`/`light_industry` trade above base for
  decades (see "Start-state supply"), pushing `light_factory` and `military_factory` down and
  `heavy_factory` up; re-check after 1840. `food_factory` still emits 400 units of a good
  priced 0.5, so its ratio follows `food_industry`'s price to the floor.
