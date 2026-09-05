# USA 1823-1833: Monroe Doctrine, Tariff of Abominations, Nullification Crisis

Gap from `docs/design/1821-1836-coverage.md` (USA row): the Monroe Doctrine only exists
Chilean-side (`events/ChileanEvents.txt:198260513`, gated on a `monroe_doctrine2` country
flag that nothing sets), and the tariff/nullification episode is absent entirely.
New file `events/USASectionalGVG.txt`, ids 1001200-1001299 (1001200-1001202 used).

## Constraints found in the tree

- `trade_policy` is a **party issue** (`common/issues.txt:5`), not a reform, so no effect can
  change it. USA starts with `ruling_party = USA_conservative`, which is already
  `trade_policy = protectionism`. The tariff is therefore modelled as a country modifier.
- The Chilean event has no tag gate: it fires for any country holding `monroe_doctrine2`.
  The USA event sets that flag on American-capital countries only, so European colonial
  powers are excluded automatically (`continent` on a country scope means its capital).
- The ACW chain must not be disturbed. `events/ACW.txt:16000` requires the
  `the_slavery_debate` modifier plus the `john_browns_raid` / `dred_scott_decision` flags;
  nothing here touches those. The only ACW edit is one extra `mean_time_to_happen`
  modifier reading a flag this chain may set - a pure accelerator, no trigger change.
- Southern regions come from `map/region.txt`: `USA_205` (South Carolina), `USA_201`
  (Georgia), `USA_211` (Virginia), `USA_194` (Mississippi), `USA_196` (Alabama).

## Events

**1001200 - The Monroe Doctrine** (USA, `year = 1823`, before 1828, fire_only_once,
MTTH 3 months, `major = yes`).
- *Proclaim* (ai 85): prestige +10, `set_global_flag = monroe_doctrine`,
  `set_country_flag = monroe_doctrine_proclaimed`, and for every existing country whose
  capital is in north/south America (tested with `capital_scope = { OR = { continent = ... } }`,
  since `continent` is a province-scope condition) (not USA, flag not already set): `relation = 15` and
  `set_country_flag = monroe_doctrine2`, which makes the existing Chilean event reachable.
- *Say nothing* (ai 15): prestige -5, `set_country_flag = monroe_doctrine_declined`.

**1001201 - The Tariff of Abominations** (USA, `year = 1828`, before 1832, fire_only_once,
MTTH 3 months).
- *Sign it* (ai 80): `tariff_of_abominations` country modifier for 10 years,
  `set_country_flag = tariff_of_abominations`, +1 militancy / +1 consciousness on pops in
  the five southern regions.
- *Strike out the higher schedule* (ai 20): prestige -5, southern militancy -1,
  rich pops +1 militancy (New England manufacturers), no modifier and no flag - the
  nullification event then never fires. That is deliberate: refusing the 1828 schedule
  is the historical off-ramp, so the crisis is a consequence of the player's own choice.

**1001202 - The Nullification Crisis** (USA, `has_country_flag = tariff_of_abominations`,
`owns = 205`, `year = 1832`, before 1836, fire_only_once, MTTH 2 months, `major`, news).
- *Force Bill and Clay's compromise* (ai 80, historical): prestige +10, remove the tariff
  modifier, southern militancy -2, `set_country_flag = nullification_resolved`.
- *Back down* (ai 15): prestige -10, remove the tariff modifier, `sectional_tension`
  modifier for 10 years and `set_country_flag = us_sectional_tension`.
- *Coerce South Carolina* (ai 5): prestige -5, +3 militancy / +2 consciousness in
  `USA_205`, `sectional_tension` for 10 years and `us_sectional_tension`.

## Supporting changes

- `common/event_modifiers.txt`: two new modifiers, `tariff_of_abominations`
  (tariff efficiency up, southern-flavoured militancy) and `sectional_tension`
  (small consciousness/militancy). Names localised in `localisation/GVG_events.csv`.
- `events/ACW.txt:16000`: one added MTTH clause, `factor = 0.8` when
  `has_country_flag = us_sectional_tension`. Trigger logic untouched.
- Pictures are existing ones only: `greatpowers`, `anticorn` (vanilla), `senate_debate`.
