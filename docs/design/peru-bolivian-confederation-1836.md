# The Peru-Bolivian Confederation (1835-1839) — design

## Problem

The Confederation is **not** missing content: PDM ships a whole apparatus for it,
and the gap is a different one. What already exists, all read and verified:

- **The tag.** `PBC` is registered (`common/countries.txt:37`,
  `"countries/Peru-Bolivia Confederation.txt"`), has a history file
  (`history/countries/PBC - Peru-Bolivian Confederation.txt`, capital 2310 La Paz,
  primary culture `south_andean`, accepted `peruvian`/`bolivian`). `SPU` (South
  Peru) and `NPU` (North Peru) also exist. So the union must **not** be faked with
  a country flag; the existing tag machinery is what this chain feeds.
- **Formation.** `decisions/PBC.txt` holds `eject_sucre`, `form_PBC_BOL`
  (BOL beats PEU, `inherit = PEU`, capital 2310, releases SPU and PEU as vassals,
  `change_tag = PBC`) and `form_PBC_PEU` (the mirror, capital 2304, sets
  `three_republics`). Both require an ongoing PEU/BOL war plus `war_exhaustion = 40`
  and 25% occupation of the loser.
- **The road to it.** `events/PBCFlavor.txt:97040` (PEU) offers "The Perus must be
  united!", which sets `ejecting_sucre` and fires 97041 at BOL; 97041 option A
  starts the BOL/PEU war, option B sets `wants_to_unify` on BOL. 97045
  ("Confederation Conflict") restarts that war whenever BOL carries
  `wants_to_unify` and nobody is fighting. 97043 pulls GCO/CLM in against PEU.
- **Dissolution.** `PBCFlavor.txt:97055` (`has_recently_lost_war = yes`,
  `war = no`, PEU/NPU no longer vassals) releases the vassals and tags back to
  BOL or SPU; `decisions/PBC.txt` `end_of_confederation_SPU` /
  `end_of_confederation_BOL` / `pbc_in_chaos` cover the same ground from the other
  side. `treaty_of_la_paz` and `centralizer_act_huayna_capac` are the survival path.

Four things are genuinely wrong or absent, and this chain addresses exactly those:

1. **No date gate and the wrong direction.** 97040 has no `year` in its trigger and
   an MTTH of 12 months, so a 1821 game can produce "A Peruvian Confederation?" in
   1822, and it always starts as *Peru conquering Bolivia*. Historically it was
   Andres de Santa Cruz, president of **Bolivia**, who marched into Peru in 1835 at
   Orbegoso's invitation, beat Salaverry at Socabaya in February 1836, and had the
   Confederation proclaimed in October 1836. Nothing in the tree mentions
   Santa Cruz, Salaverry, Orbegoso, Socabaya, Paucarpata or Yungay: grepping
   `events/`, `decisions/` and `common/` for `santa_cruz`, `yungay`, `salaverry`
   and `paucarpata` returns nothing (`2316 Santa Cruz` in `map/definition.csv` is
   the Bolivian town, unrelated).
2. **Chile never actually goes to war.** `events/ChileanEvents.txt:97050` ("The
   Peru-Bolivian Confederation") sets `fight_the_PBC`, hands out
   `cut_down_to_size` CBs to CHL and ARG, applies `usa_draft` — and then contains
   a commented-out war block with the author's note `#I can't get this to work`.
   It does not work because it was written `attacker_goal = { type = cut_down_to_size }`;
   the `war` effect takes `attacker_goal = { casus_belli = ... }`
   (`docs/wiki/list-of-effects.md:260`, and every working example in this tree:
   `PBCFlavor.txt:88`, `:251`, `:525`, `decisions/PBC.txt:222`). `type =` belongs to
   `add_casus_belli` (`list-of-effects.md:245`). So the War of the Confederation
   only ever happens if the AI decides to use the CB on its own.
3. **Dead content.** `PBCFlavor.txt:97047` ("1836 PBC Setup") fires on
   `has_country_flag = 1836_pbc`; that flag is set nowhere in the mod (the only
   other occurrence is a `NOT` check in `decisions/PBC.txt:387`). It is a leftover
   of the 1836 bookmark and can never fire in a 1821 game.
4. **No Yungay.** Nothing marks the Battle of Yungay (20 January 1839) or the
   Chilean Treaty of Paucarpata (1837) that preceded it.

Two adjacent facts, verified, that the design leans on:

- `events/ChileanEvents.txt:198260502` (Portales assassinated) requires
  `has_country_modifier = great_statesman`, `has_country_flag = DiegoPortales`,
  `NOT = { year = 1839 }` **and** `war_with = PBC` or `war_with = BOL`. Today
  that war almost never happens, so the event is effectively unreachable; this
  chain makes it reachable in its historical window.
- The `1836.1.1` blocks in `history/provinces/south america/2310 - La Paz.txt`,
  `2313 - Chuquisaca.txt`, `2305 - Antofagasta.txt`, `2309 - Calama.txt` and
  `2304 - Arequipa.txt` hand those provinces to PBC/SPU. Province history is only
  read up to the start date, so in a 1821 game they never execute; they belong to
  the vanilla 1836 bookmark. No province history file is touched by this chain.

Start-state facts (`history/provinces/south america/`, `map/definition.csv`):
at 1821.9.1 **BOL does not exist**. All of Upper Peru — 2310 La Paz, 2311
Cochabamba, 2312 Oruro, 2313 Chuquisaca, 2314 Potosi, 2315 Tarija, 2316 Santa
Cruz, 2321 Cobija, 2305 Antofagasta, 2309 Calama — is `owner = SPA` with
`add_core = BOL` (La Paz, Santa Cruz and Cobija are `controller = PEU`, the
Expedicion Libertadora's front line). PEU owns 2295 Lima, 2298 Huaraz, 2304
Arequipa and the rest of Lower Peru; CHL owns 2324 Santiago; ARG (not LPL) owns
2348 Buenos Aires. Bolivia therefore has to be created in play, which is the
chain's main dependency (see Risks).

Provinces used in triggers, all checked against `map/definition.csv`: **2295
Lima**, **2298 Huaraz** (the Ancash province Yungay stands in) and **2310 La
Paz**. 2304 Arequipa, 2305, 2309 and 2313 appear above only as start-state
evidence; no event in this chain references them.

## Chain — `events/PEUConfederationGVG.txt`, ids 1002900-1002905

| id | who | when | options |
|---|---|---|---|
| 1002900 | BOL | `year = 1835`, `NOT = { year = 1841 }`, owns 2310, PEU exists and owns 2295, both at peace, no PBC, MTTH 4mo, news | A march on Peru (AI 70) / B armed mediation (AI 20) / C stay out of Peru (AI 10) |
| 1002901 | PEU | triggered from 1002900 A, +10 days — "Salaverry, the Regenerator" | A rally to Salaverry (AI 55) / B buy Chilean and Argentine backing (AI 30) / C Orbegoso opens the gates (AI 15) |
| 1002902 | CHL | `year = 1836`, `NOT = { year = 1846 }`, `exists = PBC`, `war = no`, MTTH 6mo, news | A send the Restoration Army, declaring the war (AI 75) / B Chile cannot afford it (AI 25) |
| 1002903 | ARG or LPL | `year = 1837`, `NOT = { year = 1846 }`, `CHL = { war_with = PBC }`, `war = no`, MTTH 6mo | A Rosas joins the war (AI 60) / B Rosas has enemies enough (AI 40) |
| 1002904 | CHL | at war with PBC, `war_exhaustion = 5`, `NOT = { war_score = 10 }`, MTTH 10mo — "The Treaty of Paucarpata" | A repudiate it, send Bulnes (AI 70) / B accept and withdraw (AI 30) |
| 1002905 | CHL | at war with PBC and winning it (controls 2298 or 2295, or `war_score = 25`), MTTH 3mo, news + major — "Yungay" | A restore the three republics (AI 70) / B take the settlement and go home (AI 30) |

Every option of every *self-firing* event sets a country flag
(`santa_cruz_decided`, `restoration_war_declared`, `rosas_declared`,
`paucarpata_answered`, `yungay_won`), which is also the re-fire guard in that
event's trigger. 1002901 is `is_triggered_only` and needs no such guard; its
options set descriptive flags only (`salaverry_regime`, `orbegoso_faction`). `fire_only_once` is not used anywhere in the chain: it is engine-wide,
not per country (`docs/audit/fire-only-once.md`). Only 1002905 is `major = yes`;
1002900 and 1002902 are `news = yes` without the popup, so `audit_pacing.py`
counts one interrupting event for the whole chain.

**1002900 — Santa Cruz and the Peruvian Civil War.** Trigger is
`tag = BOL`, `exists = yes`, `is_vassal = no`, `owns = 2310`, `war = no`,
`PEU = { exists = yes owns = 2295 is_vassal = no war = no }`, `year = 1835`,
`NOT = { year = 1841 }`, and one NOR block
`NOT = { truce_with = PEU has_global_flag = peru_bolivia_confederated has_country_flag = wants_to_unify has_country_flag = santa_cruz_decided exists = PBC }`
— NOR is what is wanted here (none of those five may hold), so the shorthand is
correct as written. MTTH 4 months, halved if PEU is at war or if any PEU-owned
province has `average_militancy = 4`.

Option A (`ai_chance` 70, zeroed by `war = yes` or `truce_with = PEU`) is the
historical intervention: `set_country_flag = wants_to_unify` — the flag
`form_PBC_BOL` and `PBCFlavor.txt:97045` already key off, so the chain terminates
in the *existing* formation decision rather than in a second, parallel
`change_tag` — plus `prestige = 2`,
`add_country_modifier = { name = small_country_draft duration = 730 }`,
`any_pop = { dominant_issue = { value = jingoism factor = 0.03 } }`,
`war = { target = PEU attacker_goal = { casus_belli = cut_down_to_size } defender_goal = { casus_belli = humiliate } }`,
and `PEU = { country_event = { id = 1002901 days = 10 } }`. No `FROM` is used in
1002901, so firing it from a country scope is safe. Setting the flag opens *both*
formation decisions, not only Bolivia's: `form_PBC_PEU`'s potential is
`tag = PEU`, `war_with = BOL`, `BOL = { has_country_flag = wants_to_unify }`. So
whichever side wins the 1835 war can proclaim the Confederation - Santa Cruz's
Bolivia by `form_PBC_BOL` (capital 2310, PEU and SPU released as vassals) or a
victorious Peru by `form_PBC_PEU` (capital 2304, `three_republics`, closing on
97046). The chain sets up the war and leaves the outcome to the players.
Option B is armed mediation: prestige 1, `relation = { who = PEU value = 50 }`,
`diplomatic_influence = { who = PEU value = 25 }`, `usa_draft` for a year — the
Confederation is not attempted and the two republics stay friendly.
Option C is isolation: `prestige = -2`, `any_pop = { militancy = -1 }`,
+50 relations with CHL and ARG. Vic2 options cannot carry triggers, so "Bolivia is
in no state for a war" is expressed only through the `ai_chance` modifiers on A.

**1002901 — Salaverry, the Regenerator.** `is_triggered_only = yes`.
Option A: `set_country_flag = salaverry_regime`, `small_country_draft` for two
years, `any_pop = { dominant_issue = { value = jingoism factor = 0.04 } militancy = 1 }`,
prestige 2, `relation = { who = BOL value = -100 }` — Peru fights.
Option B buys foreign help: `prestige = -2`, +100 relations with CHL and ARG, and
two `random_country = { limit = { tag = CHL exists = yes } ... }` blocks (the
guard pattern from `PBCFlavor.txt:404`) that grant
`add_casus_belli = { target = BOL type = cut_down_to_size months = 60 }` and set
`peru_asked_for_help`, which halves 1002902's MTTH. Note `type =` is correct here
and `casus_belli =` is correct inside `war` — the two effects genuinely differ.
Option C is the Orbegoso faction: `set_country_flag = orbegoso_faction`,
`prestige = -5`, `war_exhaustion = 10`,
`any_pop = { militancy = 2 consciousness = 1 }`,
`relation = { who = BOL value = 100 }`,
`add_country_modifier = { name = coup_risk duration = 1095 }`.
It makes `form_PBC_BOL`'s `war_exhaustion = 40` gate reachable for the AI, which
is the only realistic way an AI Bolivia ever forms the union.

**1002902 — Portales and the Restoration Army.** This is the event that finishes
the job `ChileanEvents.txt:97050` gave up on. Trigger: `tag = CHL`, `exists = yes`,
`is_vassal = no`, `war = no`, `exists = PBC`, `year = 1836`,
`NOT = { year = 1846 }`, and
`NOT = { truce_with = PBC num_of_revolts = 1 has_country_flag = restoration_war_declared has_country_flag = peace_with_the_PBC PBC = { has_country_flag = the_confederation_is_legitime } }`.
The last clause is a deliberate choice: 97050 also stands down once PBC has taken
the `treaty_of_la_paz` decision, and a Confederation that has survived its
`national_instability` and been recognised should not be attacked by script.
`neighbour = PBC` is deliberately *not* required, unlike 97050: a PBC formed by
rebels or short of 2305/2309 need not border Chile, the war was fought largely at
sea, and requiring the border would silently kill the chain.
MTTH 6 months, halved by `has_country_flag = DiegoPortales`
(`ChileanEvents.txt:198260501`), by `fight_the_PBC` (97050 option A) and by
`peru_asked_for_help`.

Option A sets `restoration_war_declared` **and** `fight_the_PBC` so 97050 stops
firing behind it, then `prestige = 2`, `badboy = 2`, `treasury = -2000` (small on
purpose: `treasury` is fixed-point hundredths and Andean minors are poor),
`add_country_modifier = { name = usa_draft duration = 1095 }`,
`any_pop = { dominant_issue = { value = jingoism factor = 0.05 } }`,
`leave_alliance = PBC`, and
`war = { target = PBC attacker_goal = { casus_belli = cut_down_to_size } defender_goal = { casus_belli = humiliate } call_ally = yes }`.
`cut_down_to_size` is used rather than `release_puppet` because
`common/cb_types.txt:3113` requires `is_our_vassal = FROM`, and PEU is only a PBC
vassal on the `form_PBC_BOL` branch — `cut_down_to_size` is also the CB 97050
already hands Chile. Option B sets `restoration_war_declared` and
`peace_with_the_PBC`, `prestige = -3`, `relation = { who = PBC value = 100 }`, and
a jingoist backlash via
`any_pop = { scaled_militancy = { issue = jingoism factor = 3 } }`.

**1002903 — Rosas Declares War.** Self-triggering rather than fired from 1002902,
so it cannot arrive after PBC has already collapsed: `OR = { tag = ARG tag = LPL }`
(ARG holds 2348 at the 1821 start, but `claim_cochinoca` in `decisions/PBC.txt`
treats both, so this does too), `exists = yes`, `war = no`, `exists = PBC`,
`CHL = { war_with = PBC }`, `year = 1837`, `NOT = { year = 1846 truce_with = PBC has_country_flag = rosas_declared }`.
Option A: `prestige = 1`, `badboy = 1`, `small_country_draft` for two years, and
`war = { target = PBC attacker_goal = { casus_belli = humiliate } }`. Option B:
`prestige = -1`, +50 with PBC, -50 with CHL. No cores are handed out — the
`claim_cochinoca` decision already owns that ground.

**1002904 — The Treaty of Paucarpata.** The historical off-ramp: Blanco Encalada's
first expedition signed a withdrawal treaty in November 1837 which the Chilean
government then repudiated. Trigger: `tag = CHL`, `war_with = PBC`,
`has_country_flag = restoration_war_declared`, `war_exhaustion = 5`,
`NOT = { has_country_flag = paucarpata_answered war_score = 10 }`. The
"the expedition is not winning" test is `war_score`
(`SPAAyacuchoGVG.txt:49` uses the same trigger) rather than control of Lima,
because Chile can be stalled in a war whose front never reaches Lima at all. Option A repudiates it:
`prestige = -2`, `badboy = 1`, `war_exhaustion = -5`,
`add_country_modifier = { name = small_country_draft duration = 1095 }`,
jingoism +0.03 — the war continues and Yungay stays reachable. Option B accepts:
`set_country_flag = peace_with_the_PBC`, `prestige = -5`, `end_war = PBC`,
`relation = { who = PBC value = 100 }`, `PBC = { prestige = 10 }`,
`any_pop = { militancy = 1 }`. The Confederation survives and the chain ends
there for that game.

**1002905 — Yungay.** Trigger: `tag = CHL`, `war_with = PBC`,
`has_country_flag = restoration_war_declared`,
`OR = { 2298 = { controlled_by = THIS } 2295 = { controlled_by = THIS } war_score = 25 }`,
`NOT = { has_country_flag = yungay_won }`. The `war_score` branch matters: on the
`form_PBC_BOL` route PBC-the-tag holds only the Bolivian cores and 2295/2298
belong to its Peruvian vassal, so an AI Peru that takes `pbc_in_chaos` (below)
carries Lima and Huaraz out of Chile's war and neither `controlled_by` test can
ever pass. `war_score` keeps the closing event reachable.
(`controlled_by` is a province-scope trigger addressed by id from country scope,
the pattern in `decisions/PBC.txt:19` and `:58`.) Option A imposes the restoration:
`prestige = 10`, `badboy = 1`, and inside `PBC = { ... }` `prestige = -10`,
`war_exhaustion = 15`,
`add_country_modifier = { name = national_instability duration = 1095 }`
and `any_owned = { limit = { is_core = PEU } any_pop = { militancy = 4 consciousness = 2 } add_province_modifier = { name = nationalist_agitation duration = 1095 } }`
(the exact shape `PBCFlavor.txt:480-496` already uses), plus +100 relations from
PEU/NPU/SPU/BOL where they exist. It deliberately does **not** dissolve PBC: 97055,
`pbc_in_chaos` and `end_of_confederation_*` already do that. Note that it is
1002902's declaration, not anything Yungay does, that opens `pbc_in_chaos` — its
`allow` is `PBC = { OR = { war_with = CHL national_provinces_occupied = 0.01 } }`,
so the moment Chile declares, PBC's Peruvian vassals may break away, end their war
with Chile and turn on the Confederation. That defection is the expected and
historical sequence, not a bug, and it is why 1002904 and 1002905 test war score
rather than Peruvian provinces. Option B is
the lesser peace: `prestige = 5`, `end_war = PBC`,
`PBC = { prestige = -5 war_exhaustion = 5 }`, +50 relations. Both options are
real; the closing event is not an OK button.

## New modifiers

**None.** Everything used already exists in `common/event_modifiers.txt` and is
already used for these purposes elsewhere in the tree: `small_country_draft` and
`usa_draft` (mobilisation; `usa_draft` is what 97050 and 97041 apply for exactly
this war), `coup_risk` (97041 option A), `national_instability` (both formation
decisions and 97047), `nationalist_agitation` (province modifier, 97055 option B).
No `docs/design/_pending/` file is needed and `common/event_modifiers.txt` is not
touched.

## Localisation

New file `localisation/GVG_confederation.csv`, written only through
`python scripts/modcheck.py loc-add GVG_confederation.csv KEY "text"` (Edit/Write
on `localisation/*.csv` is hook-blocked and would save UTF-8). ASCII only, so
"Andres de Santa Cruz", "Agustin Gamarra" and "Paucarpata" carry no accents.
Keys: `EVTNAME`/`EVTDESC` for 1002900-1002905; `EVTOPTA`/`EVTOPTB` for all six and
`EVTOPTC` for 1002900 and 1002901; and the four news keys
(`EVTNAME<id>_NEWS_TITLE`, `EVTDESC<id>_NEWS_LONG/MEDIUM/SHORT`) for the three
`news = yes` events 1002900, 1002902 and 1002905. No pre-existing csv is edited.

## Pictures

Existing art only, all six verified present in `CoE_RoI_R/gfx/pictures/events/`
by listing the directory: `peru-bolivia.tga` (1002900 — already the Confederation
picture, used by `PBCFlavor.txt:97046`/`97047`), `mexico_soldiers.tga` (1002901),
`deliberation.tga` (1002902 — 97050's own picture), `nationalists.tga` (1002903),
`derrota.tga` (1002904, the withdrawal; used by `AFGWarGVG.txt:128` and
`ASHWarGVG.txt:98`), `war_ended.tga` (1002905; used by `AFGWarGVG.txt:223`).
Nothing is downloaded, `gfx/CREDITS.md` is unchanged and `gfxtool.py missing`
stays silent.

## Risks

1. **Bolivia may never exist.** Verified above: at the 1821 start SPA owns every
   Upper Peruvian province and nothing in `events/`, `decisions/` or
   `history/diplomacy/` creates BOL (`history/diplomacy/Alliances.txt:3` even
   comments "Bolivia is created 1825.8.6" for an alliance whose partner does not
   exist yet). The only in-play routes are BOL nationalist rebels in SPA's cored
   provinces and a `liberate_country` war. If neither happens the whole chain
   silently never fires — `exists = BOL` and `owns = 2310` are hard gates, so it
   fails closed rather than crashing. Fixing Upper Peru's independence belongs to
   the 1824-1830 window (`docs/design/ayacucho-1824.md`), not here; it is flagged
   as the follow-up this chain depends on.
2. **`wants_to_unify` has side effects.** Setting it on BOL is what PDM itself does
   (`PBCFlavor.txt:107`, `decisions/PBC.txt:30`), but it is a shared flag: in
   `common/rebel_types.txt:1958` it zeroes `pan_nationalist_rebels` spawn chance
   (harmless, arguably right), and `PBCFlavor.txt:97043` fires a GCO/CLM war on
   Peru off it. That war is a decade late historically; it is `fire_only_once`, its
   option B is weighted x40 when Colombia is already at war, and it needs GCO or
   CLM to still exist. Accepted rather than worked around, because avoiding the
   flag would mean duplicating `form_PBC_BOL`. The other `wants_to_unify` readers
   (`decisions/NationalUnification.txt:63/238/1143/1230`,
   `rebel_types.txt:3579/4000/4952`) are all gated on germanic, italian or south
   asian culture groups and cannot see a `south_andean` Bolivia.
3. **PBC may already exist before 1835.** 97040 has no date gate, so an early
   PEU-led Confederation is possible. 1002900 is gated with `NOT = { exists = PBC }`
   and simply stands down; 1002902-1002905 only need `exists = PBC` plus their year
   gates, so Chile's war and Yungay still run against an early Confederation.
4. **Two Chilean events can both fire.** 97050 and 1002902 are independent; the
   sequence 97050-A (CBs) then 1002902-A (the war) is the intended reading, a Chile
   that takes 97050-B is excluded from 1002902 by `peace_with_the_PBC`, and
   1002902's options set 97050's flags so it cannot fire afterwards. 97050 is not
   edited: no legacy file is touched by this chain.
5. **`war` effects and existing truces.** All three `war` effects are guarded by
   `war = no` and `NOT = { truce_with = ... }` in their triggers, but the engine
   will still refuse a declaration in odd states (already at war with the target
   through an ally). Worst case the option pays its costs and no war starts;
   nothing in the chain assumes the war exists afterwards except 1002904 and
   1002905, which both test `war_with = PBC` themselves.
6. **Province ids** are the historical crash source in this repo. Only 2295, 2298
   and 2310 are referenced in script, all confirmed in `map/definition.csv`, and
   `modcheck` re-checks them on write. No file under `history/provinces/` is
   created, moved or renamed.
7. **The Confederation can come apart before Yungay.** `pbc_in_chaos` becomes
   available to PEU/NPU the instant 1002902-A declares war, and an AI vassal will
   usually take it, ending its own war with Chile and taking Lima and Huaraz out of
   Chile's reach. 1002904 and 1002905 therefore key off `war_score` as well as
   province control, and 1002905 option A is written so that it adds pressure
   rather than performing the dissolution itself. Worst case the Confederation
   collapses through the existing PDM route with no Yungay popup, which is an
   acceptable outcome rather than a stuck state.

## Review pass: making the chain reachable (1002906, 1002907)

The chain as first written depended on a Bolivia that the mod never creates. At
the 1821 start every Upper Peruvian province is held by the royalists (the
`~`-prefixed shadow copies in `history/provinces/south america/` give Lima the
same provinces instead - either way BOL owns nothing), and the only
`release_vassal = BOL` / `change_tag = BOL` sites in the tree sit inside the
dissolution of a Confederation that cannot form without Bolivia.

`1002906` (The Congress of Chuquisaca, 1825) and `1002907` (The Republic Will Not
Wait, 1828) supply the missing birth:

- Both are gated on `owns = 2313` (Chuquisaca, Bolivia's history capital) rather
  than on a tag, so they fire for whoever actually holds Upper Peru - the
  royalists in the default game, Lima or Buenos Aires in a game that went
  differently.
- 1002906 option A releases Bolivia with
  `any_owned = { limit = { is_core = BOL } secede_province = BOL }`, the same
  effect vanilla `Taiping.txt` 160001 uses to create a tag that does not exist
  yet. `release_vassal` is deliberately not used: the wiki records that it
  creates the country as a *vassal* when the releaser owns its capital, and
  1002900 requires `is_vassal = no`.
- 1002906 option B holds the sierra (nationalist agitation, no release); 1002907
  then fires from 1828 and both of its options release Bolivia, so the chain can
  be delayed but never blocked.
- `bolivia_independent` is a global flag; `chuquisaca_answered` and
  `upper_peru_held` are the per-country guards.
- 1002900's gate was relaxed from `owns = 2310` to `OR = { owns = 2310 owns = 2313 }`
  so a Bolivia born without La Paz still answers Orbegoso.

Three further review fixes:

- **1002902 guard flag.** Both options now set the neutral `portales_decided`,
  which is what the trigger tests. `restoration_war_declared` is set only by
  option A, next to `fight_the_PBC`, so 1002904 (Paucarpata) and 1002905 (Yungay)
  can no longer fire for a Chile that declined the war and was later attacked.
- **1002905 payload.** The Peruvian agitation now runs over
  `any_country = { limit = { OR = { tag = PBC vassal_of = PBC } } ... }`. On the
  `form_PBC_BOL` path the Confederation itself owns no `is_core = PEU` province -
  `release_vassal = PEU`/`SPU` handed them all away - so the old `PBC = { any_owned
  ... }` block matched nothing.
- **News wording.** 1002900 and 1002902 publish their article whichever option is
  taken, so both now point at option-neutral keys (`EVTNEWS1002900_*`,
  `EVTNEWS1002902_*`): the appeal and the debate, not a march or a declaration of
  war that the peace branch never made. The superseded `EVTNAME1002900_NEWS_*` /
  `EVTNAME1002902_NEWS_*` rows are left in the csv as dead rows and can be pruned.
