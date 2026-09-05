# Factory and artisan profitability balance pass

*2026-09-06. Scope: `CoE_RoI_R/common/production_types.txt` only. `common/goods.txt` was
**not** touched. Closes the [high] `production_types.txt:258-305` finding in
`docs/audit/ai-balance.md` (Tables 3 and 4). **Untested in game — needs a play test.***

## Method

`scripts/balance_factories.py` prints, per production type, input cost and output value at
base prices (`ratio = value x price(output) / sum(qty x price(input))`). Throughput
multipliers, the owner output bonus and the `efficiency` bonus-goods blocks are ignored:
throughput scales inputs and output together and cancels; the efficiency block only pays out
when its goods are actually on the market. What is left is what the AI factory builder and
artisan promotion see. Run `--vanilla` for the same table over the vanilla game files.

Reference: **vanilla factories sit in a 1.02-1.74x band**, vanilla artisans 1.12-1.74x. This
mod runs richer margins by design, so the target band here is **1.5-3.5x**. Targets:

- military and luxury at the top of the band (3.3-3.5x) — high-margin end tiers, but they now
  have to buy the intermediate goods they consume;
- heavy in the middle (~2.7x), light and food at the bottom but clearly above 1.5x;
- every artisan >= 1.2x, and `artisan_food_maker` profitable at all.

## Design rules used

1. **Move `input_goods` amounts and `value`, never `goods.txt` prices.** A price change
   ripples into every pop need, RGO income and unit cost in the mod; an amount change is
   local to one production type. No price change turned out to be necessary, so goods.txt is
   unchanged.
2. **Fix military/luxury by raising inputs, not by cutting output.** Cutting `value` on
   `military_factory` would shrink world `military_industry` supply, which only units buy
   (`units/*.txt`), and on `luxury_factory` would shrink a good every pop type needs. Raising
   the input instead keeps end-tier supply intact and turns the two most attractive factories
   into the demand sink for `heavy_industry` and `light_industry` — which is exactly the tier
   the audit found nobody had a reason to build.
3. **Offset the new demand with modest output rises one tier down** (`heavy_factory` 20 -> 24,
   `light_factory` 10 -> 13), which also lifts `light_factory` out of its 1.67x last place.
4. **Fix `food_factory` on the input side** (grain 30 -> 45). Its 400-unit output is what pop
   food needs are scaled against and was left alone; the audit's separate concern that 400
   units of a 0.5-cost good floods the market is a `goods.txt` question, deferred.
5. Employees, owner blocks, workforce, templates, efficiency blocks and the factory list are
   untouched, per the audit's "don't restructure" note.
6. Artisans: only the three outliers moved. The other eight already sat at 1.50-1.60x. The
   audit's separate observation that artisans are undifferentiated (a tight margin band gives
   the pop AI no reason to prefer a good) is **not** addressed here — that is a design change,
   not a defect.

## Before / after

Ratio = revenue / input cost at base prices. Full table from
`python scripts/balance_factories.py`.

| factory | change | before | after |
|---|---|---:|---:|
| military_factory | `heavy_industry` 10 -> 35 | **12.00** | 3.43 |
| luxury_factory | `light_industry` 6 -> 22 | **12.50** | 3.41 |
| heavy_factory | `value` 20 -> 24 | 2.27 | 2.72 |
| light_factory | `value` 10 -> 13 | **1.67** | 2.17 |
| food_factory | `grain` 30 -> 45 | 2.78 | 1.85 |
| | | spread 7.5x | spread 1.9x |

| artisan | change | before | after |
|---|---|---:|---:|
| artisan_food_maker | grain 60 -> 30, cattle/fish/fruit 30 -> 10 | **0.58** | 1.49 |
| artisan_horsebreeder | grain 3.8 -> 11, fruit 2 -> 6, iron 0.5 -> 1.5 | **4.66** | 1.58 |
| artisan_military_maker | sulphur 20 -> 12, `heavy_industry` 45 -> 40 | **1.19** | 1.50 |
| (other eight, unchanged) | — | 1.50-1.60 | 1.50-1.60 |

`artisan_horsebreeder` is not in the audit's Table 4 (it was missed) but was the largest
artisan outlier at 4.66x; it also carries `effect_multiplier = 2` on its owner block, which
the ratio above does not include.

## What to watch in a play test

Whether `heavy_industry` and `light_industry` markets can actually supply 35/22 units per
military/luxury factory-day: if they cannot, prices spike, the top two tiers stall and the
2.72x/2.17x tiers below them absorb the investment. That is the intended feedback loop, but
the magnitude is untested. Check the AI's factory mix around 1840-1860 and whether artisans
still demote en masse.
