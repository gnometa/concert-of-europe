# Logic review: `events/USAFlavor.txt` + `events/USAFlavorGVG.txt`

*2026-09-06. Line-by-line read of both files (44100-44155, 1000100-1000101). Mechanical audits
(`modcheck`, `refcheck`, `audit_events`, `audit_owner_scope`, cwtools) were already at baseline,
so everything here is logic, not syntax. Cross-checked against `events/USASectionalGVG.txt`
(1001200-1001202) and the `events/ACW.txt` 16000 MTTH hooks.*

Fixed in place this pass: 44127 wargoal, 44115 option key, 44127 militancy, 44101 MTTH, 1000101
magnitudes. Everything else is documented only.

## [high]

- **1339 / 44127** - the Mexican-American War declaration built its wargoal as
  `attacker_goal = { casus_belli = acquire_all_cores country = USA }`. `acquire_all_cores` takes
  no `country` (see `common/cb_types.txt:458` and the wiki's note that `country` is only for CBs
  that name a third party, e.g. `release_puppet`); every other `acquire_all_cores` war in the mod
  (`CBsAndCores.txt:2450`, `PERFlavour.txt:2068`, four in `DIM/PERFlavour_five_x.txt`) omits it.
  Here it named the *attacker itself*, i.e. a war goal pointed at USA in USA's own war.
  **Fixed**: dropped `country = USA`, and added the `defender_goal = { casus_belli = status_quo }`
  that every comparable war effect in the mod pairs with the attacker goal (without it MEX has no
  way to sue for peace short of full capitulation).

## [medium]

- **767 / 44115** - "Time to Play Ball!" set `option name = "EVTOPTA44114"`, so the baseball event
  showed Wyatt Earp's option text. `EVTOPTA44115` exists (`text.csv:6156`) and was simply unused.
  **Fixed.**
- **1329 / 44127** - `any_pop = { limit = { has_pop_culture = mexican } militancy = 6 }` on war
  declaration. +6 militancy is a guaranteed rebellion trigger, and it runs in **USA** scope, where
  in 1846 the Mexican pops are still MEX's - so it is simultaneously too violent and mostly a
  no-op. **Fixed** to `militancy = 3`; the scope is arguably deliberate (Tejano pops in Texas) and
  was left alone.
- **1000101 / USAFlavorGVG** - `relation = { who = TEX value = 200 }` (relations cap at 200, so
  this pins them at maximum from a single event) plus `diplomatic_influence = { value = 400 }`,
  which sphere-grabs Texas outright for one click. **Fixed** to 50 / 100, in line with the other
  "we back you" options in the mod.
- **1000101 / USAFlavorGVG** - option A is called "We must help the Texans" but its only effects
  are relations and influence: no alliance, no CB, no subsidy, no war entry. Mechanically it is
  option B with the sign flipped. **Not fixed** - the right remedy (`create_alliance = TEX`, or a
  `casus_belli` against MEX) is a design call, not a defect fix. Note it also makes
  `texas_asked_for_help` / `texas_is_brave` pure bookkeeping: both are set and never read
  (refcheck already reports the class).
- **1449-1470 / 44130** - "The Maine Census" ends with
  `random_country = { limit = { tag = ENG NOT = { tag = THIS } } country_event = 44130 }`, i.e. it
  re-fires **its own id** at Britain. ENG then sees an American-voiced event, sets the USA-only
  `aroostook_war` flag on itself, stacks a second `nationalist_agitation` on 250/69, and applies
  `relation = { who = ENG }` to itself. It terminates (the `NOT = { tag = THIS }` blocks the
  bounce) and nothing reads ENG's flag, so it is cosmetic - but the intended shape is a separate
  notification event, exactly like 44149 does for the Oregon Trail. Fixing it needs a new id +
  loc, so it is left for a content pass.
- **1762-1770 / 44137** - the ultimatum concession uses `any_owned = { limit = { is_core = USA } ...
  secede_province = USA }` in ENG scope, with no region filter. 44136 only claims 250/69 (+53/54/55),
  but this hands over *every* USA-cored province Britain owns anywhere - including the Oregon cores
  that the 44150 chain may have added minutes earlier. Its sibling 44133 lists provinces explicitly.
  Left as-is: "We acknowledge their claims" can be read as accepting all claims.

## [low]

- **73-80 / 44101** - the MTTH modifiers keyed on 1886/1887 while the trigger window is 1893-1896,
  so both were permanently true and merely scaled the MTTH by a constant. **Fixed** to 1894/1895.
- **44100-44121** - twelve of these events use the identical `months = 5` + two `factor` modifiers
  block; 44104/44116/44117/44118/44120/44121 all open windows in 1836-1842, so the 1837-40 stretch
  fires roughly one USA flavour event per quarter. Pacing only; see `docs/audit/pacing-1821-1836.md`.
- **173 / 44103** - HMS Resolute grants `relation = { who = ENG value = 100 }`, four times what a
  comparable goodwill event in this mod gives.
- **44119 / 44120** - both carry a commented-out `limit` (`has_pop_religion = catholic` /
  `protestant`), so the consciousness hit lands on the whole population instead of the intended
  religious group. Deliberate-looking (the limits are commented, not deleted) but the effect no
  longer matches the text.
- **44120** - "Moral Crusaders" pushes `moralism` by 0.02 *and* `secularized` by 0.04, i.e. the
  temperance crusade secularises the country twice as fast as it moralises it. Possibly an intended
  backlash; too ambiguous to flip.
- **44126** - Mexico's defiant option ("That land is rightfully ours") *lowers* militancy by 1.
  Rallying-round-the-flag is a defensible reading.
- **44140 / 44145** - "Sell the territory" awards the seller `prestige = 5`. Selling Alaska/Hawaii
  for prestige is backwards; the buyer's +5 in 44123 is the correct sign.
- **44122** - Mexico's `ai_chance` for selling the strip has `factor = 2` when `money = 250000`, so
  a *richer* Mexico is likelier to sell, while the refuse option (correctly) also scales up with
  wealth. The two pull against each other.
- **44129** - the Mormon Exodus fires `reduce_pop = 0.25` on province 97's `native_american_minor`
  pops, i.e. it deletes 75% of them in one tick. Magnitude, not a bug.
- **44113** - the Great Chicago Fire costs a flat `treasury = -2500` regardless of the size of the
  economy in 1871.
- **1241 / 1310 / 1344** - `mexico_refused_usa_once`, `mexican_american_war` and
  `no_mexican_american_war` are set and never read anywhere in the tree (already in the refcheck
  flags baseline; listed here because all three belong to this chain).

## Interaction with tonight's `USASectionalGVG` (1001200-1001202)

No collision. USAFlavor never touches `tariff_of_abominations`, `us_sectional_tension`,
`nullification_resolved` or `monroe_doctrine2`, and its earliest window (44130, 1830) does not
overlap the 1828-1835 tariff/nullification arc except by calendar proximity. The hand-off works:
1001202's A/B/C branches set `nullification_resolved` / `us_sectional_tension`, and `ACW.txt:38-46`
reads both as MTTH modifiers on 16000 (0.8x sooner with tension, 1.1x later if resolved).
One asymmetry worth knowing rather than fixing: 1001201 option B ("strike out the higher schedule")
sets no flag and no modifier, so 1001202 - which requires `has_country_flag = tariff_of_abominations`
- can never fire on that branch, and the whole nullification episode is skipped. That is the
intended "the crisis was averted" path, but it means one in five AI runs (`ai_chance` 20) never
sees the Nullification Crisis at all.
