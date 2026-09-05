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
| event modifiers | 469 | - |
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
| BADBOY_LIMIT | 25 | 50 | 16 |
| BANKRUPCY_DURATION | 2 | 3 | 111 |
| BASE_CLERGY_FOR_LITERACY | 0.005 | 0.003 | 619 |
| BASE_COUNTRY_ADMIN_EFFICIENCY | 0.2 | 1.0 | 11 |
| BASE_COUNTRY_TAX_EFFICIENCY | 0.2 | 0.50 | 10 |
| BASE_GOODS_DEMAND | 0.8 | 1.2 | 630 |
| BASE_GREATPOWER_DAILY_INFLUENCE | 0.25 | 0.275 | 30 |
| BASE_TARIFF_EFFICIENCY | 0.2 | 0.0 | 36 |
| BASE_TRUCE_MONTHS | 60 | 12 | 515 |
| BUREAUCRACY_PERCENTAGE_INCREMENT | 0.001 | 0.000 | 18 |
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
| INFAMY_STATUS_QUO | 0 | 1 | 228 |
| INFAMY_TRANSFER_PROVINCES | 5 | 1 | 224 |
| INFAMY_UNINSTALL_COMMUNIST_GOV_TYPE | 5 | 1 | 232 |
| INVENTION_IMPACT_ON_DEMAND | 0.005 | 0.02 | 669 |
| INVESTMENT_SCORE_FACTOR | 0.005 | 0.001 | 47 |
| LEADER_PRESTIGE_TO_MORALE_FACTOR | 0.8 | 0.9 | 151 |
| LIFE_RATING_GROWTH_BONUS | 0.0001 | 0.00015 | 633 |
| LITERACY_CHANGE_SPEED | 0.1 | 0.0050 | 621 |
| LOAN_BASE_INTEREST | 0.02 | 0.005 | 98 |
| MAKE_CB_RELATION_LIMIT | 100 | 300 | 551 |
| MAX_BUREAUCRACY_PERCENTAGE | 0.01 | 0.001 | 17 |
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

151 changed or mod-only values.

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


### [medium] (5)

- `CoE_RoI_R/common/defines.lua:17` - MAX_BUREAUCRACY_PERCENTAGE cut 10x (0.01 -> 0.001): at most 0.1% of a pop may be bureaucrats, while BUREAUCRACY_PERCENTAGE_INCREMENT is 0, so admin efficiency is effectively frozen at BASE_COUNTRY_ADMIN_EFFICIENCY - fix: confirm the trio MAX_BUREAUCRACY_PERCENTAGE / BUREAUCRACY_PERCENTAGE_INCREMENT / BASE_COUNTRY_ADMIN_EFFICIENCY is intended, otherwise restore a non-zero increment
- `CoE_RoI_R/common/defines.lua:18` - BUREAUCRACY_PERCENTAGE_INCREMENT set to 0, so bureaucrats add no administrative efficiency at all - fix: restore a small positive increment or document the flat-admin design
- `CoE_RoI_R/common/defines.lua:228` - INFAMY_STATUS_QUO raised from 0 to 1: a white peace now costs infamy, which vanilla never does - fix: set back to 0 unless charging infamy for status quo is deliberate
- `CoE_RoI_R/common/defines.lua:101` - SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT raised from 1500 to 10000000, i.e. effectively unlimited loans from shadowy financiers - fix: cap it at a value the AI cannot exploit
- `CoE_RoI_R/common/defines.lua:16` - BADBOY_LIMIT doubled from 25 to 50, so containment coalitions almost never form - fix: confirm intended for a Concert-of-Europe game where infamy is the main brake

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

Real balance decisions, not script errors - each was a deliberate edit during the Roar of Industry rework and needs a play-test, not a patch:

- **MAX_BUREAUCRACY_PERCENTAGE** 0.01 -> 0.001 (c4a60eb3, 2020-12-16, "more bureaucrats needed") - lowering the cap on how much of a state's admin need one bureaucrat pop covers was meant to force players to keep far larger bureaucracies.
- **BUREAUCRACY_PERCENTAGE_INCREMENT** 0.001 -> 0 (669e751c, 2021-10-16, "disabled admin efficiency for now") - explicitly a temporary switch-off while BASE_COUNTRY_ADMIN_EFFICIENCY was raised to 1.0; it was never switched back on.
- **INFAMY_STATUS_QUO** 0 -> 1 (bf2f82c2, 2020-12-12, "better cb fabrication") - part of the CB rework; charging infamy for a white peace stops the AI from spamming wars it then walks away from.
- **SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT** 1500 -> 10000000 (a236e0a8, 2021-05-16, "loans") - raised alongside MAX_LOAN_CAP_FROM_BANKS 3 -> 10 and LOAN_BASE_INTEREST 0.02 -> 0.005 so the reworked economy could actually finance industrialisation on credit; effectively uncapped.
- **BADBOY_LIMIT** 25 -> 50 (4182c8e5, 2018-11-26, "higher badboy (will see)") - doubled so a Concert-of-Europe game can tolerate sustained expansion before a containment coalition forms; the commit message says it was already provisional.
