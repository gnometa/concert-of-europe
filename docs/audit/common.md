# common/ audit

Read-only audit produced by `scripts/audit_common.py` (re-runnable). Vanilla reference: `D:\Steam\steamapps\common\Victoria 2`.

## Counts

| set | mod | vanilla |
|---|---|---|
| goods | 30 | - |
| pop types | 13 | - |
| unit files | 24 | - |
| buildings | 18 | - |
| production types | 46 | - |
| cultures / culture groups | 272 / 37 | - |
| ideologies | 14 | - |
| governments | 30 | - |
| issues / reform options | 45 / 175 | - |
| technologies | 200 | - |
| event modifiers | 490 | - |
| casus belli | 81 | 32 |
| defines.lua keys | 639 | 640 |
| distinct modifier keys used | 492 | 429 |

Valid modifier vocabulary = 66 wiki entries + 429 keys vanilla itself uses = 439 accepted names.
Vanilla `defines.lua` keys absent from the mod copy: 1 (LONE_BACKER_PRESTIGE_FACTOR)
Vanilla casus belli absent from the mod override: 3 (acquire_substate_region, dismantle_forts, peace_order)

## defines.lua diff (vanilla -> mod)

| key | vanilla | mod | line |
|---|---|---|---|
| ADMINISTRATOR_WEIGHT | 10.0 | 3.0 | 694 |
| AGGRESSION_UNCIV_BONUS | 10 | 15 | 727 |
| AI_ARMY_TAXBASE_FRACTION | 0.3 | 0.2 | 181 |
| AI_BIGSHIP_PROPORTION | 0.4 | 0.5 | 174 |
| AI_BLOCKADE_RANGE | 200 | 2000 | 183 |
| AI_LIGHTSHIP_PROPORTION | 0.4 | 0.3 | 175 |
| AI_NAVY_TAXBASE_FRACTION | 0.3 | 0.2 | 182 |
| AI_SUPPORT_PROPORTION | 0.3 | 0.6 | 178 |
| AI_SUPPORT_REFORM | 0.05 | 0.025 | 31 |
| AI_TRANSPORT_PROPORTION | 0.2 | 0.3 | 176 |
| ALLIANCE_RELATION_ON_ACCEPT | 100 | 80 | 413 |
| ARTISAN_MIN_PRODUCTIVITY | 1 | 0.50 | 671 |
| ASKMILACCESS_DIPLOMATIC_COST | 1 | 10 | 425 |
| ASSIMILATION_SCALE | 0.004 | 0.03 | 623 |
| BANKRUPCY_DURATION | 2 | 3 | 111 |
| BASE_CLERGY_FOR_LITERACY | 0.005 | 0.003 | 619 |
| BASE_COUNTRY_TAX_EFFICIENCY | 0.2 | 0.50 | 10 |
| BASE_GOODS_DEMAND | 0.8 | 1.2 | 630 |
| BASE_GREATPOWER_DAILY_INFLUENCE | 0.25 | 0.275 | 30 |
| BASE_TARIFF_EFFICIENCY | 0.2 | 0.0 | 36 |
| BASE_TRUCE_MONTHS | 60 | 12 | 515 |
| CANCELALLIANCE_RELATION_ON_ACCEPT | -20 | -90 | 416 |
| CANCELASKMILACCESS_DIPLOMATIC_COST | 1 | 10 | 427 |
| CAPITALIST_FRACTION | 0.001 | 0.05 | 699 |
| CB_DETECTION_CHANCE_BASE | 15 | 1000 | 552 |
| CHANCE_BUILD_NAVAL_BASE | 0.75 | 1.0 | 707 |
| CHANCE_BUILD_RAILROAD | 0.2 | 0.5 | 706 |
| CHANCE_FOREIGN_INVEST | 0.16 | 0.4 | 710 |
| CHANCE_INVEST_POP_PROJ | 0.16 | 0.25 | 709 |
| COLONIAL_LIFERATING | 35 | 30 | 29 |
| COLONIZATION_COLONY_PROVINCE_MAINTAINANCE | 5 | 3 | 76 |
| COLONIZATION_COLONY_RAILWAY_MAINTAINANCE | 0.1 | 1 | 78 |
| COLONIZATION_CREATE_STATE_COST | 300 | 0 | 85 |
| COLONIZATION_INFLUENCE_TEMPERATURE_PER_DAY | 0.08 | 0.10 | 89 |
| COLONIZATION_MONTHS_TO_COLONIZE | 6 | 12 | 72 |
| COLONIZATION_PROTECTORATE_PROVINCE_MAINTAINANCE | 4 | 2 | 75 |
| COLONIZATION_RELEASE_DOMINION_COST | 30 | 100 | 84 |
| COLONY_TO_STATE_PRESTIGE_GAIN | 10 | 2 | 28 |
| COLONY_WEIGHT | 5.0 | 4.0 | 693 |
| CONVERSION_SCALE | 0.01 | 0.03 | 624 |
| CON_COLONIAL_FACTOR | 0.5 | -0.2 | 652 |
| CON_LITERACY | 0.1 | 0.3 | 647 |
| CON_LUXURY_GOODS | 0.1 | 0.05 | 648 |
| CON_MIDRICH_CLERGY | -1.25 | 0 | 650 |
| CON_POOR_CLERGY | -2.5 | 0 | 649 |
| CRISIS_BASE_CHANCE | 20 | 10 | 573 |
| DECLAREWAR_DIPLOMATIC_COST | 1 | 0 | 403 |
| EDUCATOR_WEIGHT | 10.0 | 1.0 | 696 |
| EMPLOYMENT_FIRE_LOWEST | 0.001 | 0.01 | 123 |
| EMPLOYMENT_HIRE_LOWEST | 0.001 | 0.01 | 122 |
| FACTORY_PAYCHECKS_LEFTOVER_FACTOR | 0.25 | 0.20 | 115 |
| FACTORY_PURCHASE_DRAWDOWN_FACTOR | 0.025 | 0.01 | 128 |
| FACTORY_PURCHASE_MIN_FACTOR | 0.75 | 0.50 | 127 |
| FACTORY_UPGRADE_EMPLOYEE_FACTOR | 0.8 | 0.75 | 118 |
| FLEET_SIZE | 30 | 50 | 728 |
| GOLD_TO_CASH_RATE | 0.5 | 0.20 | 12 |
| GOLD_TO_WORKER_PAY_RATE | 3.5 | 1 | 13 |
| GOODS_FOCUS_SWAP_CHANCE | 0 | 0.1 | 108 |
| GW_JUSTIFY_CB_BADBOY_IMPACT | 0.33 | 0.75 | 558 |
| GW_WARGOAL_JINGOISM_REQUIREMENT_MOD | 0.25 | 0.2 | 560 |
| GW_WARSCORE_COST_MOD | 0.65 | 0.55 | 561 |
| IMMIGRATION_SCALE | 0.004 | 0.007 | 625 |
| INFAMY_ADD_TO_SPHERE | 2 | 1 | 217 |
| INFAMY_ANNEX | 10 | 1 | 229 |
| INFAMY_COLONY | 0 | 1 | 233 |
| INFAMY_DEMAND_STATE | 5 | 1 | 230 |
| INFAMY_DESTROY_FORTS | 2 | 1.0 | 221 |
| INFAMY_DESTROY_NAVAL_BASES | 2 | 1 | 222 |
| INFAMY_DISARMAMENT | 5 | 1 | 220 |
| INFAMY_INSTALL_COMMUNIST_GOV_TYPE | 5 | 1 | 231 |
| INFAMY_MAKE_PUPPET | 5 | 1 | 219 |
| INFAMY_PRESTIGE | 2 | 1 | 226 |
| INFAMY_RELEASE_PUPPET | 0.5 | 1.0 | 218 |
| INFAMY_REMOVE_CORES | 0 | 1 | 225 |
| INFAMY_REPARATIONS | 5 | 1 | 223 |
| INFAMY_TRANSFER_PROVINCES | 5 | 1 | 224 |
| INFAMY_UNINSTALL_COMMUNIST_GOV_TYPE | 5 | 1 | 232 |
| INVENTION_IMPACT_ON_DEMAND | 0.005 | 0.02 | 669 |
| INVESTMENT_SCORE_FACTOR | 0.005 | 0.001 | 47 |
| LEADER_PRESTIGE_TO_MORALE_FACTOR | 0.8 | 0.9 | 151 |
| LIFE_RATING_GROWTH_BONUS | 0.0001 | 0.00015 | 633 |
| LITERACY_CHANGE_SPEED | 0.1 | 0.05 | 621 |
| LOAN_BASE_INTEREST | 0.02 | 0.005 | 98 |
| MAKE_CB_RELATION_LIMIT | 100 | 300 | 551 |
| MAX_CLERGY_FOR_LITERACY | 0.04 | 0.05 | 620 |
| MAX_LOAN_CAP_FROM_BANKS | 3 | 10 | 102 |
| MAX_RESEARCH_POINTS | 25000 | 35000 | 93 |
| MAX_WARSCORE_FROM_BATTLES | 50 | 75 | 507 |
| MIL_NON_ACCEPTED | 0.05 | 0.03 | 645 |
| MIL_TO_AUTORISE | 9 | 12 | 665 |
| MIL_TO_JOIN_REBEL | 7 | 8 | 663 |
| MIL_TO_JOIN_RISING | 8 | 9 | 664 |
| MIN_CRIMEFIGHT_PERCENT | 0.2 | 0.1 | 19 |
| MOBILIZATION_SPEED_BASE | 0.12 | 0.10 | 68 |
| MOBILIZATION_SPEED_RAILS_MULT | 3.0 | 4.0 | 69 |
| MONTHS_BEFORE_DISBAND | 6 | 8 | 731 |
| NAVAL_BASE_SUPPLY_SCORE_BASE | 10 | 5 | 63 |
| NAVAL_LOW_SUPPLY_DAMAGE_MIN_STR | 5.0 | 50.0 | 194 |
| NAVAL_LOW_SUPPLY_DAMAGE_SUPPLY_STATUS | 0.25 | 0.1 | 192 |
| NONCORE_TAX_PENALTY | -0.05 | -0.075 | 35 |
| ONE_SIDE_MAX_WARSCORE | 150 | 100 | 702 |
| PEACE_COST_CLEAR_UNION_SPHERE | 0.6 | 0.35 | 535 |
| PEACE_DIPLOMATIC_COST | 1 | 0 | 411 |
| POP_GROWTH_COUNTRY_CACHE_DAYS | 30 | 365 | 59 |
| POP_MIN_SIZE_FOR_REGIMENT_COLONY_MULTIPLIER | 5 | 4 | 145 |
| POP_MIN_SIZE_FOR_REGIMENT_PROTECTORATE_MULTIPLIER | 8 | 6 | 144 |
| POP_SAVINGS | 0.018 | 0.10 | 660 |
| POP_SIZE_PER_REGIMENT | 3000 | 5000 | 137 |
| PRESTIGE_DEMAND_STATE_BASE | 2 | 1 | 248 |
| PRODUCTION_WEIGHT | 0.05 | 5.0 | 700 |
| PROMOTION_ASSIMILATION_CHANCE | 1.0 | 0 | 628 |
| PROMOTION_SCALE | 0.002 | 0.0250 | 627 |
| PROVINCE_OVERSEAS_PENALTY | 0.005 | 0.05 | 34 |
| RECON_SIEGE_EFFECT | 0.5 | 0.1 | 189 |
| REDUCTION_AFTER_DEFEAT | 3.0 | 10.0 | 667 |
| RELATION_INFLUENCE_MODIFIER | 1000 | 200 | 554 |
| RELEASE_NATION_INFAMY | -5 | -1 | 524 |
| RELEASE_NATION_PRESTIGE | 0 | 10 | 523 |
| REPARATIONS_TAX_HIT | 0.25 | 0.2 | 478 |
| RESEARCH_POINTS_ON_CONQUER_MULT | 360 | 200 | 92 |
| RGO_SUPPLY_DEMAND_FACTOR_FIRE | 0.4 | 0.1 | 121 |
| RGO_SUPPLY_DEMAND_FACTOR_HIRE_LO | 0.02 | 0.1 | 120 |
| SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT | 1500 | 10000000 | 101 |
| SIEGE_BRIGADES_BONUS | 0.5 | 1.0 | 188 |
| SIEGE_BRIGADES_MAX | 13 | 10 | 187 |
| SIEGE_BRIGADES_MIN | 3 | 1 | 186 |
| SLAVE_GROWTH_DIVISOR | 10 | 1.0 | 672 |
| SMALL_DEBT_LIMIT | 10000 | 20000 | 117 |
| SOLDIER_FRACTION | 0.03 | 0.045 | 698 |
| SOLDIER_TO_POP_DAMAGE | 0.2 | 0.10 | 138 |
| SOLDIER_WEIGHT | 30.0 | 2.0 | 697 |
| SPAM_PENALTY | 10 | 20 | 701 |
| SUPPLY_RANGE | 250 | 50 | 143 |
| SUPPRESSION_POINTS_GAIN_BASE | 170 | 150 | 43 |
| TECH_FACTOR_VASSAL | 0.5 | 0.75 | 55 |
| TECH_YEAR_SPAN | 140 | 50 | 54 |
| TENSION_ON_REVOLT | 50 | 40 | 570 |
| TRADE_CAP_LOW_LIMIT_CONSTRUCTIONS | 0 | 0.50 | 126 |
| TRADE_CAP_LOW_LIMIT_LAND | 0 | 0.75 | 124 |
| TRADE_CAP_LOW_LIMIT_NAVAL | 0.3 | 0.75 | 125 |
| UNCIV_TECH_SPREAD_MAX | 0.60 | 0.15 | 48 |
| UNCIV_TECH_SPREAD_MIN | 0.15 | 0.10 | 49 |
| WARGOAL_JINGOISM_REQUIREMENT | 0.07 | 0.055 | 511 |
| WARSUBSIDIES_PERCENT | 0.20 | 0.30 | 517 |
| WAR_FAILED_GOAL_PRESTIGE_BASE | -10 | 0 | 393 |
| WRONG_REFORM_MILITANCY_IMPACT | 1 | 6 | 45 |

146 changed or mod-only values.

## Checks that came back clean

- goods referenced by buildings/production_types/units/poptypes all exist in goods.txt (308 refs)
- activate_unit / activate_building / activate_production in technologies+inventions all resolve
- production_types poptype/owner entries all have a poptypes/ file (30 refs); every building production_type is defined
- cultures and ideologies referenced by rebel_types, governments, issues, on_actions and poptypes all exist
- every `reform = option` used by events/decisions is a real option of that issue
- triggered_modifiers triggers reference only flags that are set somewhere and modifiers that exist
- no casus belli is added by an event/decision without being defined, and none marked `available = no` is still granted; every cb has sprite_index and badboy_factor
- no duplicate tech, invention, building, production type, government, good or ideology names

Repeated `rgo_goods_*` / `factory_goods_*` blocks inside one tech are vanilla idiom (vanilla industry_tech.txt does the same) and are not reported.

## Defects

### [high] (0)


### [medium] (1)

- `CoE_RoI_R/common/defines.lua:101` - SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT raised from 1500 to 10000000, i.e. effectively unlimited loans from shadowy financiers - fix: cap it at a value the AI cannot exploit

### [low] (5)

- `CoE_RoI_R/common/defines.lua:233` - INFAMY_COLONY raised from 0 to 1 (colonial wargoals now cost infamy) - fix: confirm intended
- `CoE_RoI_R/common/defines.lua:552` - CB_DETECTION_CHANCE_BASE raised from 15 to 1000: CB justification is always detected - fix: confirm intended; it disables covert CB fabrication
- `CoE_RoI_R/common/defines.lua:143` - SUPPLY_RANGE cut from 250 to 50, which shrinks overseas supply reach sharply - fix: sanity-check colonial campaigns with this value
- `CoE_RoI_R/common/defines.lua:54` - TECH_YEAR_SPAN cut from 140 to 50 while the mod runs 1821-1936, so the year-based tech cost ramp ends around 1871 - fix: widen it or confirm the intended late-game pacing
- `CoE_RoI_R/common/defines.lua:628` - PROMOTION_ASSIMILATION_CHANCE set to 0, disabling assimilation on promotion (ASSIMILATION_SCALE was raised 0.004 -> 0.03 instead) - fix: confirm the two changes are meant together

## Fixed (2026-09-06)

- `crime.txt` - `local_artisan_throughput` -> `local_artisan_output` (x2). Only province-scope artisan modifier the engine has; the same file already used it for `immoral_business`.
- `event_modifiers.txt` - `mobilisation_impact` -> `mobilisation_economy_impact` (dervish_dhaanto_modifier); vanilla nationalvalues.txt/event_modifiers.txt use the long name.
- `event_modifiers.txt` - `global_pop_militancy` -> `global_pop_militancy_modifier` (papal_rule).
- `event_modifiers.txt` - deleted the first of the two `silk_famine` blocks (was line 138); the one kept is under the `##### WORKPLACE EVENTS #####` header, matching events/WorkPlaceEvents.txt, which is the only user of the modifier.
- `triggered_modifiers.txt` - `factory_maintenance` -> `factory_owner_cost` in the ten `admin_found_*` blocks. No `factory_maintenance` exists; vanilla issues.txt uses `factory_owner_cost` for owner-borne factory cost, at comparable magnitudes (0.3-0.6).
- `triggered_modifiers.txt` - the four `pensions = 5.0 / 10 / 100 / 2500` lines in `money_hoarder_*` commented out rather than renamed. `pensions` is the issue name; the modifier is `pension_level`, a 0-1 fraction, so `pension_level = 2500` would be a 250,000% pension. The engine has always ignored these lines, and `min_social_spending = 0.50` in the same blocks already carries the intent, so commenting them out is behaviour-preserving.
- `issues.txt` - the four `artisan_throughput` lines (immigration_policy, diplomatic_reform) commented out. There is no national artisan modifier; each line was a twin of the `rgo_throughput` line beside it with the same value, which still applies.
- `defines.lua` - `CEASECOLONIZATION_DIPLOMATIC_COST` was assigned twice (448 and 473) with the same value; the earlier one was deleted, so the surviving value is **1**.

## Deferred to balance pass

Real balance decisions, not script errors - each was a deliberate edit during the Roar of Industry rework and needs a play-test, not a patch. Four of the five were decided on 2026-09-06; see "Follow-ups after the defines change" below.

- ~~**MAX_BUREAUCRACY_PERCENTAGE** 0.01 -> 0.001~~ **restored to 0.01 on 2026-09-06.** (c4a60eb3, 2020-12-16, "more bureaucrats needed") - lowering the cap on how much of a state's admin need one bureaucrat pop covers was meant to force players to keep far larger bureaucracies.
- ~~**BUREAUCRACY_PERCENTAGE_INCREMENT** 0.001 -> 0~~ **restored to 0.001 on 2026-09-06.** (669e751c, 2021-10-16, "disabled admin efficiency for now") - explicitly a temporary switch-off while BASE_COUNTRY_ADMIN_EFFICIENCY was raised to 1.0; it was never switched back on.
- ~~**INFAMY_STATUS_QUO** 0 -> 1~~ **restored to 0 on 2026-09-06.** (bf2f82c2, 2020-12-12, "better cb fabrication") - part of the CB rework; charging infamy for a white peace stops the AI from spamming wars it then walks away from.
- **SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT** 1500 -> 10000000 (a236e0a8, 2021-05-16, "loans") - raised alongside MAX_LOAN_CAP_FROM_BANKS 3 -> 10 and LOAN_BASE_INTEREST 0.02 -> 0.005 so the reworked economy could actually finance industrialisation on credit; effectively uncapped. **Still open.**
- ~~**BADBOY_LIMIT** 25 -> 50~~ **restored to 25 on 2026-09-06.** (4182c8e5, 2018-11-26, "higher badboy (will see)") - doubled so a Concert-of-Europe game can tolerate sustained expansion before a containment coalition forms; the commit message says it was already provisional.

## Follow-ups after the defines change (2026-09-06)

Owner decision, applied to `common/defines.lua`: `INFAMY_STATUS_QUO` 1 -> **0**,
`BADBOY_LIMIT` 50 -> **25**, `MAX_BUREAUCRACY_PERCENTAGE` 0.001 -> **0.01**,
`BUREAUCRACY_PERCENTAGE_INCREMENT` 0.000 -> **0.001**, and in the follow-up pass
`BASE_COUNTRY_ADMIN_EFFICIENCY` 1.0 -> **0.2**. All five are now the vanilla /
real-world values and all five therefore dropped out of the defines diff table above.
Each changed line carries a
`-- CoE 2026-09: real-world value, see docs/audit/common.md` trailing comment.

The script that was written against the old values has now been retuned. What was done,
and what was deliberately left, is below.

### Which `badboy` reading was verified

Two different things use the word `badboy`:

- As an **effect** (`badboy = 4` inside an `option` / `effect`) it is straight infamy
  points. Halving the limit doubles the sting of every one of these without touching a
  single number.
- As a **trigger** (`badboy = 0.8` inside a `trigger` / `limit` / `allow` /
  `ai_will_do` / `ai_chance` / `mean_time_to_happen` modifier) it is a *fraction of the
  infamy limit*.

The fraction reading is the correct one, verified two ways.
`docs/wiki/list-of-conditions.md:317` states it outright: "X in this case is not a
straight integer. It's a percentage of 25 (the 'infamy limit'). So 20 infamy is 0.8, and
50 infamy is 2.0." Vanilla usage agrees without a single exception: across
`events/` and `decisions/` in the base game every effect-scope `badboy` is an integer
1-10 and every trigger-scope `badboy` is a fraction 0.2-0.8 (e.g.
`decisions/France.txt:243` grants `badboy = 4` while the `ai_will_do` eight lines below
tests `badboy = 0.5`; `events/GreatPowers.txt:84` grants `badboy = 1` while the
`mean_time_to_happen` at :127-:131 tests 0.4 and 0.8). A third, mod-internal
confirmation: the twelve `badboy = -1000` / `badboy = 24.99` pairs in
`events/GreatWar_Events.txt` and `events/InfamyWar_Events.txt:511` are commented
"reduce infamy to 24.99" - they were written for a limit of **25** all along and are
correct again now.

So a trigger written `badboy = 15` never meant "15 infamy"; it meant 15x the limit
(375 infamy), which is unreachable. Those were bugs under the old limit too.

### Absolute infamy grants, halved (applied)

Every effect-scope grant above 10 was halved so it keeps the same share of the limit it
had at 50. 38 lines in 17 files:

| file | before -> after |
|---|---|
| `events/1german_revolution_1848.txt` (10 options) | 150 -> 75, 125 -> 63, 100 -> 50 (x2), 80 -> 40, 75 -> 38 (x2), 50 -> 25, 40 -> 20, 20 -> 10 |
| `events/Greater Germany.txt` (6 options) | 40 -> 20 (x2), 20 -> 10 (x4) |
| `events/ACW.txt` | 25 -> 13 (x2), 15 -> 8 |
| `events/2nd_grand_revolution.txt` | 30 -> 15 |
| `events/BELFlavor.txt` | 15 -> 8 (x2) |
| `events/CLMFlavor.txt`, `events/PERFlavour.txt` | 15 -> 8 |
| `events/ITAFlavor.txt:797` | 18 -> 9 |
| `events/PORFlavor.txt:1699` | 25 -> 13 |
| `decisions/BYZ_Expansion.txt` (4 effects) | 20 -> 10, 18 -> 9, 15 -> 8, 12 -> 6 |
| `decisions/AUS.txt`, `decisions/GRE.txt`, `decisions/SWI_neutrality.txt` | 25 -> 13 |
| `decisions/France.txt:570` (`fra_setup`), `decisions/Ottoman_Dec.txt:86` | 40 -> 20 |
| `decisions/KRA.txt:219` | 20 -> 10 |
| `decisions/NationalUnification.txt:153/:159` | 20 -> 10 and 10 -> 5 |

Halves were rounded to the nearest integer, ties up. `NationalUnification.txt:159` is
the one grant of 10 that was halved anyway: it is the other branch of the same
`random_owned` pair as :153, and leaving it would have flattened the vassal /
non-vassal distinction the effect exists to draw.

**Left alone on purpose:**

- **Grants of 10 and below** - 32 grants of exactly 10 and roughly 250 of 1-9. At a
  limit of 25 a grant of 10 is 40% of the limit, which is a heavy but defensible price
  for annexing a neighbour, and these were never "sized for 50" the way the 40-150 tier
  was. The 10s sit in `decisions/AUS.txt:146`, `GRE.txt:119`, `Irredentism.txt:464`,
  `Italy.txt:628`, `KRA.txt:563`, `TUR.txt:732`, `events/ACW.txt:2727`,
  `BELFlavor.txt:601, :1304`, `CLMFlavor.txt:683`, `ChileanEvents.txt:308`,
  `CrimeanWar.txt:561`, `Greater Germany.txt:239, :1606`,
  `NationalUnification.txt:84, :777, :1020, :1187, :1496`, `Oriental Crisis.txt:74`,
  `PERFlavour.txt:2296`, `POLflavor.txt:98, :153, :183, :236, :266, :319, :406`,
  `PanNationalists.txt:1262`, `SPAFlavor.txt:3521, :4515`. Revisit as a block if a
  play-test says expansion is now impossible.
- **The `badboy = -1000` wipes** (13 in `GreatWar_Events.txt` / `InfamyWar_Events.txt`)
  and the `badboy = 24.99` that follows each of them. That pair means "clamp infamy to
  just under the limit", and the limit it was written for is exactly the 25 now in
  force, so the pattern is correct for the first time in years.
- The negative grants `-50` / `-25` / `-15` / `-10` and below. They are relief, not
  cost; halving them would only make relief stingier.

### Trigger thresholds written as absolute infamy, converted (applied)

Twelve `ai_will_do` / `ai_chance` modifiers used integers where the engine wanted a
fraction, so they demanded 125-500 infamy and never fired. Converted to fractions of the
25 limit that preserve the infamy each author meant:

- `decisions/BYZ_Expansion.txt:77, :216, :303` - `badboy = 5` -> **0.2**
- `decisions/BYZ_Expansion.txt:143, :409, :477, :570, :644` - `badboy = 10` -> **0.4**
- `decisions/BYZ_Expansion.txt:356, :525` - `badboy = 15` -> **0.6**
- `events/RUSFlavor.txt:1897` - `badboy = 20` -> **0.8** (completes an
  `ai_chance` ladder whose other rungs are 0.2 / 0.4 / 0.6)
- `events/RUSFlavor.txt:3181` - `badboy = 15` -> **0.6**
- `inventions/culture_inventions.txt:1804` - the `expansionism` invention's `chance`
  modifier used `badboy = 5` (125 infamy, never true), so the intended "warmongers get
  this invention sooner" `factor = 2` never applied -> **0.4**. It is the only
  trigger-scope `badboy` anywhere in `inventions/` or `technologies/`.

Each of these was previously a dead `factor = 0` guard, so the AI took decisions it was
supposed to refuse at high infamy; they now bite.

**Not converted:** the containment thresholds in `events/InfamyWar_Events.txt`
(`badboy = 1.5` at :24, `badboy = 2` at :106, :145, :241, :255-:339, :375, :431) and
`events/crises.txt:625, :629` (1.5 / 2). These are already fractions and read as "at the
limit", "1.5x the limit", "2x the limit" - a coherent ladder. What changed is that they
now trip at 25 / 37.5 / 50 infamy instead of 50 / 75 / 100, which is the intended
consequence of the smaller limit and the first thing to watch in a play-test.
The roughly 200 other fractional triggers across `events/` and `decisions/` rescale by
themselves for the same reason and were not touched.

**[low] `INFAMY_STATUS_QUO` 1 -> 0.** No script reads the define and nothing tests for
"infamy from a white peace"; the 56 `casus_belli = status_quo` grants across 23 event
and decision files are unaffected. The status-quo wargoal is free again, as in vanilla.
Nothing to retune.

### Bureaucracy and administrative efficiency (applied)

**`BASE_COUNTRY_ADMIN_EFFICIENCY` 1.0 -> 0.2** (`defines.lua:11`, the vanilla value).
The 1.0 was set by the same 2021 commit that zeroed `BUREAUCRACY_PERCENTAGE_INCREMENT`
("disabled admin efficiency for now"); the pair was one switch-off, and leaving 1.0 in
place would have kept the restored cap and increment inert - every country would sit at
100% administrative efficiency no matter how few bureaucrats it employed. Lowering it is
what makes administrative efficiency something a country earns.

What this changes in game:

- **Administrative efficiency** now starts at 20% and climbs with the bureaucrat share
  of each state's population, capped at `MAX_BUREAUCRACY_PERCENTAGE` (1.0%) plus
  `BUREAUCRACY_PERCENTAGE_INCREMENT` (0.1%) per administrative reform level. The only
  administrative reform ladder is `admin_reform` (`common/issues.txt:1103`) and it has
  **three** steps - `no_admin_reform`, `yes_admin_reform`, `advanced_admin_reform` - the
  last of which is `allow = { year = 1850 }`. So the real cap is **1.1%** for a reformed
  country before 1850 and **1.2%** after it, never more. A 1821 state with no reform and
  no bureaucrats is at 20% efficiency; hiring to ~1% takes it to 100%.
- **Tax efficiency** is the visible consequence. `BASE_COUNTRY_TAX_EFFICIENCY` is 0.50
  in this mod and administrative efficiency multiplies on top of it, so an
  unadministered country collects far less than it did yesterday. Early-game budgets get
  tighter and the gap between a well-run and a badly-run state widens; this is the
  intended realism, but it is the single largest economic consequence of the whole
  defines pass and needs a play-test on a poor tag as well as on a great power.
- **Bureaucrat demand** rises by an order of magnitude relative to the 0.1% cap regime
  (there was no reason to hire past 0.1% before, and no reward for it either since
  efficiency was pinned at 100%). `common/national_focus.txt:42` (`promote_bureaucrats`)
  and the `bureaucrats` promotion effects in the education / RGO chain
  (`events/+education_RGO.txt:146, :183`, `events/00_CoE_RoI.txt:717`) now do something
  rather than nothing. Bureaucrats are `state_capital_only` middle-strata pops paid out
  of the administration budget, so the cost shows up as administrative spending.

**`common/triggered_modifiers.txt:872-1052` - the `admin_found_*` ladder re-cut.** The
ten tiers stepped `bureaucrats = 0.005 / 0.010 / ... / 0.050`, i.e. up to forty times the
useful ceiling; every rung above 0.012 rewarded hiring the engine ignores, and under the
old 0.1% cap every single rung did. They now step **0.001** at a time, 0.003 -> 0.012,
which is the whole reachable band: tier 8 sits at the base cap (1.0%), tier 9 at the
pre-1850 reformed cap (1.1%) and tier 10 at the post-1850 `advanced_admin_reform` cap
(1.2%). Nothing in the ladder is dead script any more, and the top tier is a genuine
end-state reward. Only the `trigger` blocks moved; every modifier payload is unchanged.

**[low] `common/issues.txt:1106, :1140, :1607, :1638`** - the four
`administrative_efficiency(_modifier)` reform effects (-0.05, +0.05, +0.025, +0.05) and
`common/event_modifiers.txt:3632` (+0.05) are relative and still need no edit, but they
were sized while admin efficiency was pinned at 1.0 and now apply to a number that
actually moves. Worth a second look after a play-test.
