# Logic audit — `CoE_RoI_R/events/PoliticalEvents.txt`

Generic political events (ids 3100–4439) that every civilised country sees, so
every defect here is high-exposure. Reviewed line by line against the vanilla
file (`Victoria 2/events/PoliticalEvents.txt`) to separate deliberate PDM/RoI
tuning from accidental damage, and against `common/issues.txt` for every
`political_reform = <option>` effect.

Baseline notes:
- All 25 `political_reform` / party-issue option names used in effects exist in
  `common/issues.txt`. No unknown reform options.
- The file contains **no `year =` gate at all**, so nothing is locked out by the
  1821 start date.
- All `EVTNAME/EVTDESC/EVTOPT*` keys referenced resolve in `localisation/`.

Legend: `line id — problem — fix`. [FIXED] items were changed in this pass.

## [high]

- **1493 · 4100 "Mass Protests!"** — option B was `name = "EVTOPTB14100"`, a typo
  for `EVTOPTB4100`. `EVTOPTB14100` is defined in `localisation/newtext.csv` as
  *"The economic planners knows what they are doing."* (a planned-economy line
  also used by `ElectionEvents.txt:870`), so the option that grants `plurality = 2`
  on an upper-house protest event displayed unrelated economic-planning text —
  text directly contradicting the effect. — **[FIXED]** now `EVTOPTB4100`
  ("All voices will be heard."), which matches the effect.

- **236–246 · 3102 "Circulation Doubles!" option C** — `aristocrats` had been
  search-replaced with `capitalists`, producing a dead trigger branch
  (`OR = { has_pop_type = capitalists has_pop_type = capitalists }`) and the
  effect block twice, i.e. capitalists took **militancy +14** instead of +7 while
  aristocrats took nothing. — **[FIXED]** restored the vanilla `aristocrats`
  branch and effect block (`poptypes/aristocrats.txt` exists in this mod).

- **1098–1108 and 1119–1129 · 3752 "Brick St. Gentlemen's Club" options A/B** —
  same duplication: capitalists got consciousness ±4 / militancy ∓2 (double), and
  the aristocrat half of a *gentlemen's club* event was silently deleted. —
  **[FIXED]** same way.

## [medium]

- **3101 · 4412 "Pluralist Peace"** — MTTH modifier used `NOT = { consciousness = 7 }`.
  `consciousness` is a pop-scope condition; in a country-scope MTTH it is not the
  country average, so the ×1.3 slowdown was unreliable. Every other modifier in
  the file uses `average_consciousness`. — **[FIXED]** → `average_consciousness = 7`.

- **2607 / 2695 / 2753 / 3579 · 4403, 4404, 4405, 4419** — `treasury = -50000`.
  Vanilla spent `treasury = -100` (4403) or a goods stockpile (4405, 4419). At the
  1821 start 50 000 is several years of a secondary power's entire income, and
  these events are repeatable at 200–400 month MTTH. The `ai_chance` guards
  (`factor = 0.1` when `NOT = { money = 50000 }`) protect the AI but leave the
  player a ruinous option. — *Not fixed: pure balance number, needs a design call.*
  Suggested: `-5000` to `-10000`, or restore the goods cost.

- **1813–1877 · 4202 "Mandate For Reform"** — trigger requires
  `voting_system = proportional_representation`, a 30 % liberal upper house and
  `political_reform_want = 0.3`, but option A sets `first_past_the_post`, option B
  sets `jefferson_method` (both *regressions*), and option C is a no-op. A mandate
  for reform can therefore only be answered by de-reforming. Vanilla-inherited. —
  *Not fixed: reversing reform direction is a design change.*

- **3135 / 3406 · 4413 "Moralist Resurgence", 4417 "Moralism & War"** — the mod
  deleted vanilla's `civilized = yes` from both triggers (confirmed by diff), so
  both now fire for uncivilised nations. 4417 hands out `war_exhaustion = -2`. If
  intentional it is undocumented; every other event in the file is gated. —
  *Not fixed: may be deliberate unciv coverage.*

## [low]

- **2064, 2068 · 4302** — MTTH uses `plurality = 0.3` and `plurality = 0.5`.
  `plurality` is a 0–100 scale (this file uses 4–8 elsewhere), so both modifiers
  are always true and the event is permanently ×0.72 faster than written.

- **3151–3161 · 4413** — the same modifier `NOT = { moralism = 5 }` appears twice
  (factor 1.5 and factor 2), compounding to ×3. Almost certainly meant to be two
  different thresholds.

- **3632 · 4420 option A** — `add_country_modifier = { name = CB_gen_plus duration = 100 }`
  with no `NOT = { has_country_modifier = CB_gen_plus }` guard on a repeatable
  event. `duration` is 100 *days* against a 200-month MTTH, so real stacking of the
  +25 % CB speed is very unlikely; left alone rather than adding a guard clause.

- **3647 · 4420 option B** — `badboy = 5` plus three neighbour casus belli, with no
  `ai_chance` on either option, so the AI takes the +5 infamy option about half the
  time. (The `add_casus_belli = { target = THIS }` inside `random_country` is
  correct: that effect grants the *target* the CB, i.e. the event owner.)

- **1393 · 3756 "Workhouse Strike"** — another `aristocrats` → `capitalists`
  substitution, but without duplication, so only the flavour changed (capitalists
  rather than landowners resent the strike). Left as is.

- **1571 · 4102 option B** — `prestige = -20` for merely musing that population-weighted
  representation might be better. Vanilla value; large for a purely domestic option.

- **4102–4483 · 4435–4439 (immigration chain, mod-added)** — option names are raw
  English strings (`name = "This dissension cannot be permitted."`) instead of
  `EVTOPT*` localisation keys. Works in game but is untranslatable and inconsistent
  with the rest of the file.

- **Options without `ai_chance`** — 3751 (grants `yes_meeting`), 4418 (repeals it via
  `political_reform = no_meeting`), 4421 (`gerrymandering`), 4422 (`non_socialist`),
  4425 (`censored_press`), 4430 (`appointed`). The AI picks 50/50 between reforming
  and reform-blocking on all six. Not wrong, but it is why AI reform paths look
  random; worth weighting by `ruling_party_ideology` in a later pass.
