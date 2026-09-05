# rebel_types.txt and cb_types.txt: design or breakage?

*2026-09-06. Follow-up on the `common/rebel_types.txt` and `common/cb_types.txt` items in
`docs/audit/ai-balance.md`. Verdict: **all of them are deliberate design, inherited or
authored; no breakage found, no script changed.** Evidence below.*

## Method

Three sources of intent: (1) `git log --follow` on both files back to the 2014 initial
import (`fb286918` "version 1.14", tree `PDM_Concert/`), which is the PDM/CoE base this mod
started from; (2) a field-by-field diff of the current files against that base and against
vanilla HoD (`D:\Steam\...\Victoria 2\common\`); (3) reading how the values are actually
consumed - rebel `spawn_chance` modifier blocks, the 1848 event chain, and every
`add_casus_belli` / `war = { casus_belli = }` site under `events/` and `decisions/`.

## rebel_types.txt

**Every audited value is byte-identical to the 2014 base import.** Diffing
`fb286918:PDM_Concert/common/rebel_types.txt` against the current file shows no change to
any `spawn_chance`, `defection`, `independence`, `defect_delay`, `occupation_mult` or `area`
line (trailing whitespace only). The only commits that ever touched this file in the
Roar-of-Industry era are `55242918` / `7b2ef4e9` (added then reverted) and `6262c05d`
"balance", which changes `province_control_days = 90` -> `240` and nothing else. The 1-100
`spawn_chance` scale and `defection = none` are therefore **upstream PDM behaviour, not a
rework regression**.

### spawn_chance

| type | mod = 2014 base | vanilla | will_rise mod | will_rise vanilla |
|---|---|---|---|---|
| nationalist_rebels | 100 | 3 | 0.25 | 0.5 |
| unciv_reactionary_rebels | 100 | 3 | 1 | 1 |
| separatist_rebels | 50 | (new) | 0.5 | - |
| colonial / native / independence / turkish_nat. | 20 | (new) | 0.5 | - |
| pan_nat. / red_shirts / sepoys / carlist / christino | 10 | 1.1 | 0.5 | 0.5 |
| liberal_rebels | 2 | 1.02 | **1** | 0.5 |
| socialist_rebels | 2 | (new) | **1** | - |
| communist / reactionary / fascist | 2 | 1.02 | 0.5 | 0.5 |

The audit read the base factors as flat weights. They are not: `nationalist_rebels`'
`factor = 100` is immediately multiplied by `0.01` when the pop is a **primary** culture on
an owned core (net 1) and by `0.1` when **accepted** (net 10), and zeroed if no suitable
unreleased core tag exists (`rebel_types.txt:1602-1630`). The 100 applies only to unaccepted
minority cultures with a valid release target - precisely where nationalist rebels belong.
Against that, PDM *doubled* liberal/socialist `will_rise` to 1 and *halved* nationalist
`will_rise` to 0.25, so ideological types are twice as likely as vanilla to convert a
movement into an actual revolt. The two scales cancel; the file is coherent.

The 1848 chain does not depend on `spawn_chance` at all. `LiberalRevolutions.txt` (ids
10001/10000/10050/10051) drives the revolution by pumping pops directly - `any_pop = {
ideology = { value = liberal factor = 0.05 } scaled_consciousness = { ideology = liberal
factor = 4 } }` on the agitation event, then `any_owned = { any_pop = { scaled_militancy = {
ideology = liberal factor = 9 } } }` on Springtime of Nations - plus the
`global_liberal_agitation` / `springtime_of_nations` modifiers and the
`liberal_revolutions_should_now_fire` global flag. Event-driven, as suspected. **No change.**

### defection

| type | mod | vanilla | independence mod / vanilla | still secedes? |
|---|---|---|---|---|
| nationalist_rebels | none | culture | **culture** / culture | yes, via `independence` |
| pan_nationalist_rebels | none | pan_nationalist | none / none | n/a |
| red_shirts | none | pan_nationalist | none / none | n/a |
| communist_rebels | none | ideology | none / none | n/a, flips government |
| indian_sepoys | **pan_nationalist** (unchanged) | pan_nationalist | none / culture | n/a |

The audit's premise ("winning rebels only occupy") does not hold. `defection` controls which
*existing* country a province flips to; `independence` controls creating a new one.
`nationalist_rebels` keeps `independence = culture` and `area = nation_culture`, so it still
releases its national tag on victory - only the "hand the province to whichever neighbour
shares the culture" path is off, which is exactly what a Concert-of-Europe map does not
want. `communist_rebels` keeps the full 30-entry `government = { ... }` mapping
(`rebel_types.txt:762-795`), so a communist victory still installs
`proletarian_dictatorship` / `socialist_democracy`; `defection = ideology` would only have
handed provinces to an existing proletarian dictatorship, of which there are none for most
of the timeline. `indian_sepoys` was never changed (still `defection = pan_nationalist`).
Vanilla itself ships `defection = none` on liberal, reactionary, fascist, anarcho-liberal
and carlist rebels, so the value is ordinary. **No change.**

`separatist_rebels` (`occupation_mult = 5.0`, `defect_delay = 3`, `spawn_chance = 50`) is
likewise identical to the 2014 base. Aggressive, but authored, and gated behind the mod's
separatist events. **No change** - retune only as an explicit balance decision, not a fix.

## cb_types.txt

Unlike the rebel file this one *was* heavily reworked (~6,100 changed lines vs the 2014
base) - and the rework documents itself. Nearly every CB carries its previous value in an
inline comment: `months = 12 #months = 12`, `construction_speed = 0.25 #construction_speed =
0.25 0.8`, `truce_months = 12 #months = 0`, `always = no #always = yes`. A uniform 12-month
justification at quarter speed, uniform 12-month truces, most auto-available CBs demoted to
`always = no`, infamy up 7-14x, and `BADBOY_LIMIT` doubled to 50 in `defines.lua` are one
consistent statement: wars are slow, few and expensive. That is the mod's premise.

### The zero-infamy CBs are not reachable

Cross-referencing all 81 CB blocks against every `add_casus_belli` and `war = { casus_belli
= }` site in `events/`, `decisions/` and `common/`:

- **None of the 24 zero-infamy CBs is ever passed to `add_casus_belli`.** The 20 CB types
  events and decisions actually grant are `humiliate` (19 sites),
  `demand_concession_casus_belli` (14), `establish_protectorate_casus_belli` (13),
  `cut_down_to_size` (12), `make_puppet` (11), `conquest` (11), `take_from_sphere` (9),
  `add_to_sphere` (9), `release_puppet` (8), `place_in_the_sun` (8), `acquire_state` (8),
  `free_peoples` / `free_allied_cores` (4 each), the three `install_*` (3 each),
  `great_game_cb` (3), `dismantle_cb` (2), `sahel_jihad_cb` and `cut_down_to_size_boxer`
  (1 each). Every one has a nonzero `badboy_factor` (2.0-30.0).
- `conquest_any` (`po_annex`), `acquire_any_state`, `civil_war`, `call_allies_cb` and
  `colonial_competition` have `constructing_cb = no` **and** `can_use = { ... always = no }`.
  They exist only as wargoal objects for scripted `war = { casus_belli = conquest_any }`
  declarations (`AUSFlavor.txt:750`, `CLMFlavor.txt:693`, `decisions/PBC.txt:226`, ...),
  where the granting event sets the political price; charging infamy would double-bill it.
- `annex_africa_full` is `badboy_factor = 3`, not 0, and is `is_triggered_only = yes` with
  `always = no` - unreachable, not free.
- The `restore_*`, `great_war_install_*`, `unification_*`, `oriental_crisis`,
  `dismantle_cb_add*` and `east_indian_*` CBs are all `is_triggered_only = yes` plus
  `always = no`: engine- or script-granted only.
- The only four constructible CBs at `badboy_factor = 0` are `unification_casus_belli`,
  `unification_annex_casus_belli`, `rude_boy` and `colonial_reconquest_cb`. All four are
  **0 in vanilla and in the PDM base too** (vanilla `cb_types.txt:1394`, `:1462`, `:1521`;
  base line 628): free unification and free punishment of an over-infamous power are stock
  behaviour. The mod's only edit was `always = yes` -> `always = no`, which makes them
  *harder* to get. `colonial_reconquest_cb` is further gated to SPA/SPC vs PRI/CUB/PHL and
  NET vs JAV/MAL, target unsphered and under three states.

There is no free-annexation exploit to close, and per the brief the raised infamy on the
usable CBs is design and was left alone. **No change.**

## Residual notes (not fixed here)

- `scripts/audit_common.py` reports three vanilla CBs absent from the mod override:
  `acquire_substate_region` and `dismantle_forts` (both deliberately `#`-commented out of
  `peace_order`) and `peace_order` itself (false positive - an ordering list, not a CB).
  Left as-is; the file header warns against removing stock triggered CBs, so if substate
  wargoals ever show up in `error.log`, this is where to look.
- The `acquire_state1..6`, `place_in_the_sun1..6` and `demand_concession_casus_belli1..6`
  ladders (graduated infamy 3.5 -> 50.5) are defined but never granted and not
  constructible - an unfinished scaling design, inert rather than broken.

## Verification

`modcheck braces` 2 files ok; `refcheck names` 0 problems; `audit_common` high=0; cwtools at
baseline (12 x production_types + CBsAndCores:2448 + Indochina:188).
