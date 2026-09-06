# The Centralist Turn (1833-1836) - design

## Problem

`docs/design/1821-1836-coverage.md:53` calls the centralist turn **partial**:
"events/MEXFlavor.txt:44853, one event, no reform effect". The second half of
that is **stale**. Read at `events/MEXFlavor.txt:1758-1878`, the Plan of
Cuernavaca event does carry reform effects: option A ("Long live President
Lopez de Santa Anna!") applies `political_reform = state_equal_weight`,
`none_voting`, `state_press`, `underground_parties`, sets
`government = presidential_dictatorship`, adds `national_confusion` for 365
days and shifts primary-culture pops away from liberalism; option B ("Defend
the federal constitution!") adds `coup_risk` + `conservative_reaction` and
leaves the federal republic standing. Both options set `cuernavaca_plan`.

The real gap is everything around that single event:

- **Before it.** `events/MEXFlavor.txt` goes 44850 First Mexican Empire ->
  44852 Plan of Casa Mata -> 44853 Cuernavaca with nothing in between. Grepping
  `events/` and `decisions/` for `farias|zacatecas|siete|centralist` returns
  only `decisions/Mexican Minors.txt:30` (province 2158 listed among the
  Rio Grande cores) and `decisions/extra_decisions.txt:1664`
  `total_war_in_yucatan` (a Caste War draft decision). The 1833 Gomez Farias
  program - secular education, the end of compulsory tithe collection, the
  attack on the military fuero - is not scripted anywhere, so the reaction of
  1834 has nothing to react against.
- **After it.** No closing of the congress and the state legislatures, no 1835
  militia law and no Zacatecas, no Siete Leyes, no Yucatan. 44853 ends the
  story on the day Santa Anna takes power.
- **44853 may never fire at all.** Its trigger needs `tag = MEX`, a democracy
  government, `year = 1830`, and `any_owned_province = { is_core = MEX
  OR = { controlled_by = REB state_scope = { average_militancy = 6 } } }`.
  A state *average* of 6 militancy in practice means a revolt is already
  running. A chain gated on `cuernavaca_plan` would therefore be dead in a
  large fraction of games, so the spine below is gated on flags this chain
  sets itself and **supersedes 44853 explicitly** when it has not fired.
- **The republic itself arrives through 44850/44852.** MEX starts
  `government = prussian_constitutionalism` (`history/countries/MEX -
  Mexico.txt`); 44850 First Mexican Empire needs
  `UCA = { has_country_flag = join_mexico }`, set by
  `events/USCAFlavor.txt:97580` in 1821-22, and 44852 Plan of Casa Mata turns
  the empire into `government = democracy`. Everything below assumes that has
  happened - see Risks.
- **The 1821 start cannot reach the centralist republic any other way.**
  `history/countries/MEX - Mexico.txt` has a `1836.1.1` block that hands MEX
  `government = presidential_dictatorship`, `none_voting`, `state_press`,
  `underground_parties` and the flags `first_empire`, `casa_mata_plan`,
  `cuernavaca_plan`, `texas_seceded`. `common/bookmarks.txt` contains exactly
  one bookmark, `1821.9.1`, so that block never executes in this mod: whatever
  the 1836 history describes has to be produced by events instead.

Two neighbouring chains are already covered and are **not** touched here:

- **Texas.** `events/MEXFlavor.txt:44854` (Cherokee in Tejas), `44855` /
  `996542` (Empresarios in Tejas), `44856` Republic of Texas - which secedes
  provinces 132, 133, 134, 137 to TEX and declares war - and `44842`-`44846`
  (Velasco, ceasefire, war), plus `events/USAFlavorGVG.txt:1000100`/`1000101`
  (the Texan call for help). 44856's `mean_time_to_happen` already carries
  `modifier = { factor = 0.1 OR = { government = presidential_dictatorship
  presidential_dictatorship2 presidential_dictatorship3 } }`, so installing the
  dictatorship on the centralist path multiplies the Texan revolt's rate by ten
  on its own. **No edit to the Texas chain is needed or made**; this chain only
  sets the `siete_leyes_proclaimed` country flag, which it reads itself and which the
  Texas chain may read later if anyone wants a tighter link.
- **Yucatan secession.** `events/MEXFlavor.txt:44821` The Yucatan Republic
  fires from `year = 1841`, only when MEX is neither a democracy nor an
  hms_government, and secedes the `MEX_2183` cores to YUC. This chain stops
  well short of that: it scripts the 1835-36 grievance the later secession
  grows out of, and hands nothing to YUC.

Provinces used, all verified in `map/definition.csv` and owned by MEX at the
start date (`history/provinces/mexico/`, `owner = MEX controller = MEX
add_core = MEX` in each): 2158 Zacatecas, 2159 San Luis Potosi, 2160
Aguascalientes, 2183 Merida, 2184 Campeche, 2185 Bacalar, 2165 Villahermosa.
2172 Mexico City is MEX's capital. `map/region.txt:1167` names
`MEX_2173 = { 2173 2167 2159 2158 }` "Zacatecas", but 2173 is Queretaro and
2167 is Guanajuato, so the Zacatecas event lists province ids explicitly rather
than using that region. `MEX_2183 = { 2183 2185 2184 2165 }`
(`map/region.txt:1159`) is clean and is used as a region, exactly as 44821 uses
it.

## Chain - `events/MEXCentralistGVG.txt`, ids 1003100-1003104

| id | who | when | options |
|---|---|---|---|
| 1003100 | MEX | year >= 1833, democracy1/2/3, not yet `cuernavaca_plan`, MTTH 3mo | A the whole program (AI 45) / B restrain the vice-president (AI 35) / C dismiss Farias (AI 20) |
| 44853 | MEX | *existing, unchanged* - Plan of Cuernavaca, fires here if its militancy condition is met | A dictatorship / B defend the constitution |
| 1003101 | MEX | year >= 1834, `farias_program` OR `farias_dismissed`, MTTH 4mo (halved if `cuernavaca_plan`) | A close the congress and the state legislatures (AI 80) / B let the new congress sit (AI 20) |
| 1003102 | MEX | triggered, 240 days after 1003101 A - the militia law and Zacatecas | A march on Zacatecas (AI 85) / B accept Governor Garcia's terms (AI 15) |
| 1003103 | MEX | triggered, 180 days after either option of 1003102 - Las Siete Leyes, news | A the seven laws entire (AI 75) / B departments with elected assemblies (AI 25) |
| 1003104 | MEX | `siete_leyes_proclaimed`, `owns = 2183`, MTTH 4mo - Yucatan and the departments | A garrison Merida (AI 60) / B confirm the fueros (AI 40) |

None of these use `fire_only_once`: it is engine-wide, so every option sets a
country flag and every self-firing trigger `NOT`-guards all of that event's
flags. Multi-clause `NOT = { a b }` is NOR, which happens to be the wanted
"none of these flags" semantics; the guards are written as separate `NOT`
blocks anyway so the intent is unambiguous.

### 1003100 - The Reforms of Gomez Farias (1833)

Trigger: `tag = MEX`, `exists = yes`, `OR = { government = democracy democracy2
democracy3 }`, `year = 1833`, `NOT = { year = 1840 }`, and `NOT` guards on
`cuernavaca_plan`, `farias_program`, `farias_restrained`, `farias_dismissed`.
The government check *is* the "federal republic exists" check, so
`has_country_flag = casa_mata_plan` is deliberately **not** required: it would
add a coupling the government check already implies, and it would lock the
event out if MEX ever reaches a democracy by some other route.

- **A - "Let the reforms proceed."** `set_country_flag = farias_program`;
  `political_reform = censored_press` (one step up from Mexico's starting
  `state_press`; the press order in `common/issues.txt` is `state_press`,
  `censored_press`, `free_press`, and 1003101 A / 44853 A both roll it back, so
  the arc closes); `add_country_modifier = { name = educational_reform
  duration = 3650 }` (research +15%, consciousness +0.05 - the Direccion
  General de Instruccion Publica); `add_country_modifier = { name =
  liberal_reaction duration = 1825 }`, the same modifier 44850/44852 use;
  `treasury = 15000` for the tithe and mission revenues diverted to the state -
  deliberately four digits, because treasury literals are fixed-point
  hundredths. Pops: `any_pop = { limit = { type = clergymen } militancy = 4
  consciousness = 2 ideology = { value = reactionary factor = 0.15 } }`, and
  primary-culture officers/soldiers get `scaled_militancy = { ideology =
  reactionary factor = 8 }` plus a conservative ideology shift for the fuero;
  primary-culture pops overall get `scaled_militancy = { ideology = liberal
  factor = -3 }`. This is the branch that earns the reaction.
  The `education` reform itself is **not** used: it is `next_step_only = yes`
  in `common/issues.txt` and Mexico starts at `elite`, so the state-schools
  option `public` is two steps away and cannot be reached cleanly. The
  `educational_reform` modifier carries the same idea.
- **B - "Restrain the vice-president."** `set_country_flag =
  farias_restrained`; `add_country_modifier = { name = conservative_reaction
  duration = 1825 }`; `plurality = -1`; clergy militancy -1; primary-culture
  pops `scaled_militancy = { ideology = liberal factor = 4 }`. No reform, no
  research bonus, no money - and the chain stops here, because 1003101 requires
  `farias_program` or `farias_dismissed`. Stability bought with the whole
  centralist storyline, which is a real trade.
- **C - "Dismiss Farias and govern with the church and the army."**
  `set_country_flag = farias_dismissed`; `add_country_modifier = { name =
  conservative_reaction duration = 3650 }`; `add_country_modifier = { name =
  coup_risk duration = 730 }`; clergy and officers shift conservative and lose
  2 militancy; primary-culture pops `scaled_militancy = { ideology = liberal
  factor = 6 }`. Santa Anna's April 1834 turn taken a year early: it reaches
  1003101 without ever paying for the reforms.

`ai_chance` uses only weights and `war = yes` / flag modifiers - Vic2 options
cannot carry triggers.

### 1003101 - The Plan of Cuernavaca and the Closing of the Congress (1834)

This is the hinge with the existing content. Trigger: `tag = MEX`,
`exists = yes`, `year = 1834`, `NOT = { year = 1842 }`, `OR = {
has_country_flag = farias_program has_country_flag = farias_dismissed }`, and
`NOT` guards on `congress_dissolved` and `federal_compromise`. It does **not**
require `cuernavaca_plan`, because 44853 often never fires; instead
`mean_time_to_happen` carries `modifier = { factor = 0.5 has_country_flag =
cuernavaca_plan }` and option A's `ai_chance` weights the same flag up, so an
actual Plan of Cuernavaca makes the closure both faster and likelier.

- **A - "Close the congress and the state legislatures."**
  `set_country_flag = congress_dissolved` **and** `set_country_flag =
  cuernavaca_plan`. Setting the second flag is the explicit supersession: it is
  in 44853's own `NOT` guard, so once this option is taken 44853 can no longer
  fire and re-ask the same question. The option then re-applies exactly 44853
  option A's package - `government = presidential_dictatorship`,
  `political_reform = state_equal_weight`, `none_voting`, `state_press`,
  `underground_parties` - which is idempotent when 44853 already ran and
  completes the picture when it did not, so both paths converge on the same
  constitutional state. Plus `add_country_modifier = { name = rights_suspended
  duration = 730 }` (global militancy and consciousness -0.05: martial calm),
  `add_country_modifier = { name = national_instability duration = 1095 }`
  (core militancy +0.1, `issue_change_speed` 0.5),
  `remove_country_modifier = liberal_reaction` (a no-op when absent, exactly as
  44852 and 44853 already call `remove_country_modifier` unconditionally),
  liberal `scaled_militancy` +8 and reactionary -4, and
  `country_event = { id = 1003102 days = 240 }` - block form, the bare form
  does not work.
- **B - "Let the new congress sit."** `set_country_flag = federal_compromise`;
  `add_country_modifier = { name = republican_reforms duration = 3650 }`
  (research +10%, core militancy -10%); `plurality = 2`; reactionary
  `scaled_militancy` +10 and conservative +6; clergy and officers +2 militancy.
  The federalist counterfactual: a research and stability payoff, no
  administrative bonus, and the chain ends - the Siete Leyes are never written.
  Its `ai_chance` carries `modifier = { factor = 0.25 OR = { government =
  presidential_dictatorship presidential_dictatorship2
  presidential_dictatorship3 } }`: if 44853 already installed the dictatorship,
  a government re-opening the congress is the unlikely branch (the pattern for
  the three-variant government check is 44856's own MTTH modifier).

### 1003102 - The Militia Law and Zacatecas (1835)

`is_triggered_only = yes`, fired only by 1003101 A, so it lands around March
1835 - the law reducing the state militias to one man per five hundred
inhabitants, and the refusal of Zacatecas to disband.

- **A - "March on Zacatecas."** `set_country_flag = zacatecas_crushed`;
  `prestige = 3`; `treasury = 10000` (the forced loan and the Zacatecas mint;
  four digits on purpose); `2158 = { add_province_modifier = { name =
  nationalist_agitation duration = 1825 } }` and the same for 1095 days on
  `2160` - Aguascalientes was detached from Zacatecas as its own department in
  May 1835; `any_owned = { limit = { OR = { province_id = 2158 province_id =
  2159 province_id = 2160 } } any_pop = { militancy = 3 consciousness = 2 } }`
  (the `any_owned` -> `any_pop` nesting is the pattern used at
  `events/AFGWarGVG.txt:172` and throughout `ACW2_Events.txt`); primary-culture
  officers and soldiers lose 2 militancy and shift conservative.
- **B - "Accept Governor Garcia's terms."** `set_country_flag =
  state_militias_intact`; `prestige = -3`; the same three provinces get
  `any_pop = { militancy = -2 }`; `add_country_modifier = { name =
  growing_unrest duration = 1825 }` - backing down in front of one state
  emboldens the rest. `ai_chance` weights this up under `war = yes`.

Both options end with `country_event = { id = 1003103 days = 180 }`.

### 1003103 - Las Siete Leyes (1835-36)

`is_triggered_only = yes`, `news = yes`, `major = yes`. Reached from either
Zacatecas option, which is right: the Bases of October 1835 and the seventh law
of December 1836 happened whether or not the army had to march.

- **A - "The seven laws entire, and a Supremo Poder Conservador."**
  `set_country_flag = siete_leyes_proclaimed`; `political_reform = appointed` (upper house
  named by the executive - the same effect 44850 option A uses),
  `political_reform = none_voting`, `political_reform = no_meeting`,
  `political_reform = underground_parties` (all four verified against
  `common/issues.txt`; `no_meeting` and `harassment` are used together at
  `events/2nd_grand_revolution.txt:249-252`, `appointed` at
  `events/CleanUp.txt:2230`); `add_country_modifier = { name = siete_leyes
  duration = 7300 }` (new, below); `add_country_modifier = { name =
  national_confusion duration = 365 }`; `prestige = 5`; primary-culture pops
  `scaled_militancy = { ideology = liberal factor = 8 }`, while clergy,
  aristocrats and officers shift conservative and lose 2 militancy.
- **B - "Departments, but let them elect their assemblies."**
  `set_country_flag = siete_leyes_proclaimed` as well - the constitution exists either way
  and 1003104 keys off it - plus `set_country_flag = moderate_centralism`,
  which 1003104's `ai_chance` reads. `political_reform = landed_voting` (one
  step up from `none_voting`; used at `events/ARGFlavor.txt:342`) and
  `political_reform = harassment` (one step up from `underground_parties`);
  `add_country_modifier = { name = national_instability duration = 1825 }`;
  `prestige = 2`; liberal `scaled_militancy` +3 only, reactionary and clergy
  +4. No `siete_leyes` modifier: the administrative dividend is the price of
  the full centralism.

### 1003104 - Yucatan and the Departments (1836)

Self-firing rather than triggered, so that the `siete_leyes_proclaimed` flag is genuinely
read: `tag = MEX`, `exists = yes`, `has_country_flag = siete_leyes_proclaimed`,
`owns = 2183`, `NOT` guards on `yucatan_subordinated` and
`yucatan_conciliated`, MTTH 4 months. The `owns = 2183` clause also keeps the
`any_owned` blocks from being the silent no-op `audit_owner_scope.py` looks
for, if Merida has been lost in a war.

- **A - "The departments are the law: garrison Merida."** `set_country_flag =
  yucatan_subordinated`; `prestige = 2`; `any_owned = { limit = { region =
  MEX_2183 } add_province_modifier = { name = secessionist_agitation
  duration = 1825 } }` and, in the same region, `any_pop = { limit = {
  has_pop_culture = mayan } militancy = 2 consciousness = 1 }`.
  `secessionist_agitation` is heavy (`local_RGO_throughput -0.25`,
  `assimilation_rate -1`, militancy +0.25) - it is confined to the four Yucatan
  provinces and expires after five years, and it is exactly the estrangement
  that 44821 collects on in 1841. Merida, Campeche and Bacalar are majority
  mayan by pop (`history/pops/1821.9.1/Mexico.txt`), so the culture limit
  bites; `has_pop_culture` is correct here because this is pop scope
  (`any_pop = { limit = ... }`), the same shape as
  `events/MEXFlavor.txt:2270`, whereas inside an `all_core`/`any_owned` limit
  the province-scope `culture` trigger would be the one to use.
- **B - "Confirm the fueros of Yucatan."** `set_country_flag =
  yucatan_conciliated`; `prestige = -2`; `treasury = -5000` for the customs
  exemption Merida extracted; `any_owned = { limit = { region = MEX_2183 }
  any_pop = { militancy = -3 consciousness = 1 } }`. `ai_chance` weights this
  up on `state_militias_intact` and `moderate_centralism` - a government that
  has already conceded once concedes again.

No option in this chain releases a tag, cedes a province or starts a war.
Zacatecas and Yucatan are provincial crises and are paid for in modifiers,
militancy and money.

## New modifiers - one, written to `docs/design/_pending/MEXCentralistGVG_modifiers.txt`

- `siete_leyes` (country): `administrative_efficiency_modifier = 0.10`,
  `suppression_points_modifier = 0.25`, `issue_change_speed = -0.25`,
  `global_pop_consciousness_modifier = -0.05`,
  `core_pop_militancy_modifier = 0.05`, `icon = 15`. Every key is already in
  use in `common/event_modifiers.txt`: `administrative_efficiency_modifier` in
  `kolowrat_administration`, `suppression_points_modifier` /
  `issue_change_speed` / `global_pop_consciousness_modifier` in
  `metternich_system`, `core_pop_militancy_modifier` in `national_instability`.
  The country flag the chain sets is `siete_leyes_proclaimed`, deliberately
  distinct from the modifier name so flag and modifier never read as the same
  identifier in `refcheck.py`.

Everything else is reused, and each was read in `common/event_modifiers.txt`
before being chosen: `educational_reform`, `liberal_reaction`,
`conservative_reaction`, `coup_risk`, `rights_suspended`,
`national_instability`, `republican_reforms`, `growing_unrest`,
`national_confusion`, `nationalist_agitation` (province),
`secessionist_agitation` (province).

## Localisation

New file `localisation/GVG_sieteleyes.csv`, keys added only with
`python scripts/modcheck.py loc-add CoE_RoI_R/localisation/GVG_sieteleyes.csv
KEY "text"` (Edit/Write on a csv is blocked by the PreToolUse hook, and the
file must stay Windows-1252/CRLF, ASCII text, terminator column `x`):

- `EVTNAME1003100` .. `EVTNAME1003104`, `EVTDESC1003100` .. `EVTDESC1003104`.
- `EVTOPTA1003100`, `EVTOPTB1003100`, `EVTOPTC1003100`; `EVTOPTA`/`EVTOPTB` for
  1003101, 1003102, 1003103 and 1003104.
- News keys for 1003103 only: `EVTNAME1003103_NEWS_TITLE`,
  `EVTDESC1003103_NEWS_LONG`, `EVTDESC1003103_NEWS_MEDIUM`,
  `EVTDESC1003103_NEWS_SHORT`.
- The modifier name `siete_leyes` (already added:
  `siete_leyes;The Seven Laws;;;;;;;;;;;;;x`), matching how `java_war` and
  `cultuurstelsel` are localised in `GVG_events.csv`.

26 keys in total. No accented characters: "Gomez Farias", "Yucatan",
"Queretaro" and "Merida" are written unaccented in both the design and the
localisation.

## Pictures

No new art. Verified by listing both directories:

- `mexico_soldiers`, `national_congress`, `streetriot` -
  `CoE_RoI_R/gfx/pictures/events/` (the mod's own; `mexico_soldiers` is the
  picture every existing MEX flavour event uses, `national_congress` is used by
  `events/India.txt:226`).
- `churchmexico`, `Administration` - the vanilla folder
  `D:\Steam\steamapps\common\Victoria 2\gfx\pictures\events\`. `Administration`
  is already referenced by `events/USAFlavorGVG.txt:6` and `churchmexico` by
  `events/USCAFlavor.txt:97580`, the 1821 "Joining Mexico?" event - so both are
  known-good in this mod. Neither file is shipped under
  `CoE_RoI_R/gfx/pictures/events/`; the engine falls back to the game folder for
  pictures the mod does not ship, which is what `gfxtool.py missing` checks.

Assignment: 1003100 `churchmexico`, 1003101 `national_congress`, 1003102
`mexico_soldiers`, 1003103 `Administration`, 1003104 `streetriot`.

## Risks

- **Dead flags.** HEAD is a dead-flag sweep, so every flag has a reader:
  `farias_program` / `farias_dismissed` in 1003101's trigger and `ai_chance`,
  `farias_restrained` in 1003100's own guard, `congress_dissolved` and
  `federal_compromise` in 1003101's guards, `cuernavaca_plan` in 44853's
  trigger and in 1003101's MTTH and `ai_chance`, `zacatecas_crushed` in
  1003103's `ai_chance`, `state_militias_intact` and `moderate_centralism` in
  1003104's `ai_chance`, `siete_leyes_proclaimed` in 1003104's trigger,
  `yucatan_subordinated` and `yucatan_conciliated` in 1003104's guards.
  `scripts/refcheck.py flags` must stay clean.
- **Double-asking the Cuernavaca question.** If 44853 fires first, 1003101 A
  re-applies reforms that are already in place (harmless) and re-sets a flag
  that is already set (harmless). If 1003101 A fires first, 44853 is locked out
  by its own `NOT = { has_country_flag = cuernavaca_plan }`. The one case not
  covered is 44853 option B ("defend the federal constitution") followed by
  1003101 A, which reverses that choice - historically what happened, and the
  player is asked again rather than overridden silently.
- **Chain length.** 1003100 (1833) -> 1003101 (1834) -> +240d -> 1003102
  (1835) -> +180d -> 1003103 (late 1835/1836) -> ~4 months -> 1003104. Five
  player-facing events over three years for one tag; `audit_pacing.py` should
  see no same-day cascade, since every hand-off carries a delay of at least
  120 days.
- **The chain still sits downstream of a fragile spine, one step further up.**
  Escaping 44853's militancy gate does not escape 44852's: the Plan of Casa
  Mata (`events/MEXFlavor.txt:1616-1640`) uses the identical
  `any_owned_province = { is_core = MEX OR = { controlled_by = REB state_scope =
  { average_militancy = 6 } } }` condition, and it needs `first_empire` from
  44850, which needs `UCA = { has_country_flag = join_mexico }`. That flag comes
  from `events/USCAFlavor.txt:97580` ("Joining Mexico?"), which fires for UCA by
  `year = 1822` on a 30-day MTTH with `ai_chance = 100` on the annexation
  option, and UCA does exist at the 1821 start
  (`history/countries/UCA - United States of Central America.txt`, capital
  2186). So the AI path normally resolves, helped by the ten-year
  `nationalist_agitation` and `liberal_reaction` that 44850 option A hands out -
  but a player-run UCA that goes its own way, or a Mexico that never sees a
  state reach 6 average militancy, keeps MEX a `prussian_constitutionalism`
  monarchy and this chain simply never starts. That is a real dependency, not a
  gap this chain can close from below: Gomez Farias presupposes the republic,
  and inventing a second route to it would step on 44850/44852.
- **Nothing is added to `common/on_actions.txt`**, so no pulse weights are
  diluted.
- **Province ids** are the historical crash source here: 2158, 2159, 2160,
  2183, 2184, 2185 and 2165 are all in `map/definition.csv` and MEX-owned at
  the start date; `modcheck provinces` re-checks the event file.
- **`MEX_2173` is not used.** It is called Zacatecas but contains Queretaro and
  Guanajuato; the Java War note records the identical trap with `NET_1413`.
- **`secessionist_agitation` is a strong province modifier.** Five years of
  -25% RGO throughput on four Yucatan provinces is a real economic hit; it is
  the deliberate price of option A, and option B avoids it entirely.
- **The 1836 history block** in `history/countries/MEX - Mexico.txt` is dead
  code under the single 1821 bookmark. If a 1836 bookmark is ever added, this
  chain will not fire into it: 1003100 requires `NOT = { has_country_flag =
  cuernavaca_plan }`, which that block sets.
- **Naming assumption.** The pending-modifier filename uses the event file stem
  `MEXCentralistGVG` as the chain key, since the task did not define one.
