# Legacy logic audit — `CoE_RoI_R/events/FRAFlavor.txt`

Line-by-line review of the 30 France flavour events (ids 37200-37300). The mechanical
audits (refcheck, audit_events*, fire_once, pacing, owner_scope) were at baseline before
this pass, so everything below is a logic/semantic defect a script cannot see.
Line numbers are pre-fix. **[FIXED]** entries were applied in this commit; the rest are
proposals (design changes) left for the maintainers.

## Fixed

- **404 (37208) — [high]** — Option of the 1848 "Louis-Napoleon returns" event pointed at
  `EVTOPTA37207`, i.e. it displayed the previous event's text *"Merde!"* on a button whose
  effects are `prestige = 5`, `set_country_flag = louies_back` and a liberal ideology
  push. Text contradicted the effects. **Fix:** point at `EVTOPTA37208` ("Vive la
  République!"), which already exists in `text.csv`.
- **557,561 (37213) — [medium]** — Tocqueville event fires in the window 1836-1840
  (`year = 1836`, `NOT = { year = 1840 }`) but both mean_time_to_happen modifiers test
  `year = 1853` / `1854`; they can never apply, so the intended "gets likelier over time"
  ramp is dead and the event always sits at a flat 5-month MTTH. Copy-paste from 37211.
  **Fix:** 1837 / 1838, matching the pattern used by every other event in the file.
- **944 (37223) — [medium]** — Jenatzy/automobile event's only option is named
  `EVTOPTA37222`, the aeroplane event's key. **Fix:** own key `EVTOPTA37223`, added to
  `localisation/newCE.csv`.
- **984 (37224) — [medium]** — Ballets Russes event's only option is named
  `EVTOPTA37221` (Sarah Bernhardt). **Fix:** own key `EVTOPTA37224`, added to
  `localisation/newCE.csv`.
- **1067 (37226) — [high]** — Corsican Rebellion option applies the militancy relief with
  `limit = { has_pop_religion = north_italian }`. `north_italian` is a *culture*
  (`common/cultures.txt`), not a religion; the limit matches nothing, so the -8 militancy
  the option promises is never applied to anybody and the province secedes with its
  rebellion intact. **Fix:** `has_pop_culture = north_italian` (the sister events 37227/
  37228 already use `has_pop_culture = greek` / no filter).
- **1614 (37244) — [high]** — Option B of the July Revolution ("Kings do not bow to
  shopkeepers", i.e. Charles X *wins* and the revolution is crushed) set
  `set_country_flag = july_revolution`, the same flag option A sets. That flag is read
  cross-file as "the liberal July Monarchy is in power": `BELRevolutionGVG.txt:42`,
  `ENGReformGVG.txt:106` and `ITARisingsGVG.txt:45,112,124` all gate the 1830 revolutionary
  wave on `FRA = { has_country_flag = july_revolution }`, and `decisions/France.txt:596`
  uses it to lock out `constitution_suspended`. Picking B therefore unlocked the Belgian
  and Italian risings on behalf of a France that had just shot the liberals, and the
  reactionary branch became indistinguishable from the liberal one. **Fix:** option B no
  longer sets the flag at all. `charles_x` is (correctly) left in place by B and is what
  marks that branch, so the Fan Affair (37234, `charles_x` OR `july_revolution`) still
  fires; `fire_only_once` keeps 37244 from repeating. Side effect worth a follow-up: with
  neither flag set, `constitution_suspended` becomes selectable again after a crushed
  revolution, which is defensible but should be a deliberate choice.
- **1683 (37300) — [medium]** — "Luxembourg wants to join us", decline option:
  `relation = { who = LUX value = 400 }`. Relations are clamped to -200..200, so half the
  stated reward is silently discarded and the number misrepresents the effect.
  **Fix:** 200.

## Proposals (not applied)

- **1265 (37234) — [medium]** — The Fan Affair's pay-up option moves £10,000 from France
  to Aldjazair (`treasury = -10000` / `ALD = { treasury = 10000 }`). In 1830 that is many
  years of French state income and it hands an uncivilised minor a war chest it cannot
  spend; the historical debt was a fraction of the budget. Suggest ~1000, or scale it.
- **1197 (37230) — [medium]** — Declining Tahiti gives `badboy = -2` for free. Infamy
  reduction with no cost or cooldown is exploitable (the event is `fire_only_once`, so the
  exposure is bounded, but the incentive is backwards: refusing an annexation should be
  neutral, not a reward). Suggest dropping the badboy line.
- **1291-1380 (37235) — [medium]** — The Algerian Rebellion has no `fire_only_once` and
  nothing ever clears `algerian_rebellion`; the flag only multiplies the MTTH by 4, so the
  event re-fires roughly yearly until 1860 and each acceptance stacks another
  `badboy = 2` plus `relation`/`diplomatic_influence` -200 on an already-hostile Aldjazair.
  Suggest gating repeats behind a cooldown modifier or making acceptance one-shot.
- **584-620 (37216 chain) — [medium]** — The whole Dreyfus chain (37216/37217/37218)
  requires `exists = GER`. In a game where unification produces NGF, fails, or Prussia is
  eaten, the affair never happens even though it needs no particular German state.
  Suggest `OR = { exists = GER exists = NGF exists = PRU }` or dropping the check.
- **1043-1140 (37226/37227/37228) — [low]** — These three secession events carry no
  `tag = FRA`; they fire for *any* owner of Corsica / Crete / Cyprus, including Sardinia
  or the Ottomans, and are only filed here by accident. Either add the tag check or move
  them to a shared file so their generality is intentional and discoverable.
- **1128 (37228) — [low]** — The Cyprus option applies `militancy = -8` to every pop in
  the ceded provinces with no culture limit, unlike its Corsican and Cretan siblings,
  so it also pacifies the coloniser's own settlers.
- **1411 (37240) — [low]** — `month = 9` with the comment "September 16th historicaly".
  The engine's `month` trigger is 0-indexed, so this is October and the accession lands a
  month late. Left alone because the intent is ambiguous and the drift is cosmetic.
- **1085 / 1112 / 1043 (37226-37228) — [low]** — `prestige = -20` on each. That is a large
  one-off hit for a garrison failure on a single island; -5 to -10 would sit better with
  the rest of the file, where flavour events move prestige by 2-5.
- **827 (37221) — [low]** — Sarah Bernhardt is the only event in the file whose trigger
  omits `exists = yes` alongside `tag = FRA`. Harmless (a dead tag owns nothing) but
  inconsistent.

## Checked and found sound

`NOT = { ... }` blocks with multiple members (37200, 37213, 37216, 37217, 37218, 37230,
37235, 37240) are all genuine NOR usage, matching the author's intent, not mistaken NANDs.
`add_casus_belli = { target = THIS }` inside `random_country` (37235) is correct: in event
effects `THIS` remains the event's root country, per vanilla `BoerWar.txt:67`.
The `three_glorious_days` flag required by 37244 is still produced after 37242 was
commented out — `decisions/France.txt:610` (`constitution_suspended`) sets it — so that
branch is not dead. France starts 1821 as `prussian_constitutionalism2`, which satisfies
both 37240 and 37244, and `history/countries/FRA - France.txt:155` sets `july_revolution`
only in the 1836 block, which the 1821 bookmark never executes. Every year window in the
file is reachable from an 1821 start, and no two events cover the same episode.
