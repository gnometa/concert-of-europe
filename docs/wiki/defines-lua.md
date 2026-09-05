# Defines.lua

Source: https://vic2.paradoxwikis.com/Defines.lua

### General

start_date = '1836.1.1',

end_date = '1935.12.31',

### Country

| variable name | default value | description |
|---|---|---|
| YEARS_OF_NATIONALISM | 20 | Years of Nationalism |
| MONTHS_UNTIL_BROKEN | 3 | OBSOLETE! (Months until rebel held capital results in broken country.) |
| REBEL_ACCEPTANCE_MONTHS | 60 |  |
| BASE_COUNTRY_TAX_EFFICIENCY | 0.2 | Basic efficiency for taxes without bureaucrats and tech |
| BASE_COUNTRY_ADMIN_EFFICIENCY | 0.2 | Basic administration efficiency without bureaucrats and tech |
| GOLD_TO_CASH_RATE | 0.5 | Amount of money generated per gold unit |
| GOLD_TO_WORKER_PAY_RATE | 3.5 | Multiplier for how much money gold pays to pops |
| GREAT_NATIONS_COUNT | 8 | Number of great powers. Note that there must be at least this number of GP candidates (candidates being countries) at game start or the game crashes. |
| GREATNESS_DAYS | 365 | how many days a country must be outside the top 8 nations to lose status as great power nation |
| BADBOY_LIMIT | 25 | The amount of infamy a nation can get before other countries gets the cut down to size Casus Belli |
| MAX_BUREAUCRACY_PERCENTAGE | 0.01 | More than max percent bureaucrats of population will give no additional benefits |
| BUREAUCRACY_PERCENTAGE_INCREMENT | 0.001 | For each social administrative reform level, this is added to MAX_BUREAUCRACY_PERCENTAGE |
| MIN_CRIMEFIGHT_PERCENT | 0.2 |  |
| MAX_CRIMEFIGHT_PERCENT | 0.99 |  |
| ADMIN_EFFICIENCY_CRIMEFIGHT_PERCENT | 0.5 | Crimefight depends on both state admin eff. and admin spending, admin spending percent effect is set to (1-ADMIN_EFFICIENCY_CRIMEFIGHT_PERCENT) |
| CONSERVATIVE_INCREASE_AFTER_REFORM | 0.25 | how many more conservatives are added in the upper house when a reform is enacted |
| CAMPAIGN_EVENT_BASE_TIME | 42 | once every 6 weeks. |
| CAMPAIGN_EVENT_MIN_TIME | 21 | never more often than 3 weeks between |
| CAMPAIGN_EVENT_STATE_SCALE | -3 | every non-colonial state reduces by 3 days. |
| CAMPAIGN_DURATION | 6 | a election campaign lasts these amount of months |
| COLONIAL_RANK | 16 | Minimum rank a nation must have to colonize |
| COLONY_TO_STATE_PRESTIGE_GAIN | 10 | Prestige gain when turning colony to state |
| COLONIAL_LIFERATING | 35 | The base life rating required to colonize a state before inventions |
| BASE_GREATPOWER_DAILY_INFLUENCE | 0.25 | Influence value which is distributed each day |
| AI_SUPPORT_REFORM | 0.05 | At least this many % needs to support a reform for the AI to take it |
| BASE_MONTHLY_DIPLOPOINTS | 0.3 | Base diplomatic points gained each month |
| DIPLOMAT_TRAVEL_TIME | 14 | The cooldown before a country can make another diplomatic interaction with the same country |
| PROVINCE_OVERSEAS_PENALTY | 0.005 | Each province req. this many goods flagged as overseas penalty |
| NONCORE_TAX_PENALTY | -0.05 | -5% taxes received for each non-core province in state |
| BASE_TARIFF_EFFICIENCY | 0.2 | baseline tariff efficiency |
| COLONY_FORMED_PRESTIGE | 1 | prestige from founding a colony. |
| CREATED_CB_VALID_TIME | 12 | how many months a casus belli will stay valid after fabricated<ref>Note that many CB's are always applicable and will thus never expire</ref> |
| LOYALTY_BOOST_ON_PARTY_WIN | 0.1 |  |
| MOVEMENT_RADICALISM_BASE | 25 |  |
| MOVEMENT_RADICALISM_PASSED_REFORM_EFFECT | -2 |  |
| MOVEMENT_RADICALISM_NATIONALISM_FACTOR | 1.0 |  |
| SUPPRESSION_POINTS_GAIN_BASE | 170 | monthly suppression points gain with max bureaucrats |
| SUPPRESS_BUREAUCRAT_FACTOR | 0.5 |  |
| WRONG_REFORM_MILITANCY_IMPACT | 1 |  |
| SUPPRESSION_RADICALISATION_HIT | 10 | Percentage base added to a movements radicalness |
| INVESTMENT_SCORE_FACTOR | 0.005 | how much foreign investment money counts towards your industrial score |
| UNCIV_TECH_SPREAD_MAX | 0.60 |  |
| UNCIV_TECH_SPREAD_MIN | 0.15 |  |
| MIN_DELAY_BETWEEN_REFORMS | 6 | How many months before a new reform can be enacted |
| ECONOMIC_REFORM_UH_FACTOR | -0.40 |  |
| MILITARY_REFORM_UH_FACTOR | -0.40 |  |
| WRONG_REFORM_RADICAL_IMPACT | 15 |  |
| TECH_YEAR_SPAN | 140 |  |
| TECH_FACTOR_VASSAL | 0.5 | cost reduction factor if overlord has researched the tech |
| MAX_SUPPRESSION | 100 | The max suppression points that can be stored |
| PRESTIGE_HIT_ON_BREAK_COUNTRY | -0.20 | percentage prestige reduction when country gets taken by rebels |
| MIN_MOBILIZE_LIMIT | 3 |  |
| POP_GROWTH_COUNTRY_CACHE_DAYS | 30 | period of cached pop growth (used for player) |
| NEWSPAPER_PRINTING_FREQUENCY | 350 | days frequency when the news attempt to be printed (may not print if not enough facts collected, and retry after another X days) |
| NEWSPAPER_TIMEOUT_PERIOD | 890 | the max period for news that may be printed. The probability is decreased with time. |
| NEWSPAPER_MAX_TENSION | 750 | when tension of printing gets this high, the newspaper will attempt to be printed immediately. |
| NAVAL_BASE_SUPPLY_SCORE_BASE | 10 | base value that is powered by level of naval base. Determines the naval supplying capabilities. |
| NAVAL_BASE_SUPPLY_SCORE_EMPTY | 2 | min value for coastal provinces with no naval base. |
| NAVAL_BASE_NON_CORE_SUPPLY_SCORE | 0.3 | modifier for supply score for naval bases that are not in core provinces. |
| COLONIAL_POINTS_FROM_SUPPLY_FACTOR | 1 |  |
| COLONIAL_POINTS_FOR_NON_CORE_BASE | 1 |  |
| MOBILIZATION_SPEED_BASE | 0.12 | Base speed for raising troops |
| MOBILIZATION_SPEED_RAILS_MULT | 3.0 | Speed modifier for raising troops. It's max value for max railways level in state. |
| COLONIZATION_INTEREST_LEAD | 3 |  |
| COLONIZATION_INFLUENCE_LEAD | 3 |  |
| COLONIZATION_MONTHS_TO_COLONIZE | 6 | The amount of time it takes to colonize a state if left unchallenged |
| COLONIZATION_DAYS_BETWEEN_INVESTMENT | 90 | The amount of days needed to pass to make another investment in a colonial race |
| COLONIZATION_DAYS_FOR_INITIAL_INVESTMENT | 270 |  |
| COLONIZATION_PROTECTORATE_PROVINCE_MAINTAINANCE | 4 |  |
| COLONIZATION_COLONY_PROVINCE_MAINTAINANCE | 5 |  |
| COLONIZATION_COLONY_INDUSTRY_MAINTAINANCE | 1 |  |
| COLONIZATION_COLONY_RAILWAY_MAINTAINANCE | 0.1 |  |
| COLONIZATION_INTEREST_COST_INITIAL | 100 |  |
| COLONIZATION_INTEREST_COST_NEIGHBOR_MODIFIER | -20 |  |
| COLONIZATION_INTEREST_COST | 20 |  |
| COLONIZATION_INFLUENCE_COST | 20 |  |
| COLONIZATION_EXTRA_GUARD_COST | 10 |  |
| COLONIZATION_RELEASE_DOMINION_COST | 30 |  |
| COLONIZATION_CREATE_STATE_COST | 300 |  |
| COLONIZATION_CREATE_PROTECTORATE_COST | 5 |  |
| COLONIZATION_CREATE_COLONY_COST | 4 | per province |
| COLONIZATION_COLONY_STATE_DISTANCE | 400 |  |
| COLONIZATION_INFLUENCE_TEMPERATURE_PER_DAY | 0.08 |  |
| COLONIZATION_INFLUENCE_TEMPERATURE_PER_LEVEL | 0.005 |  |
| PARTY_LOYALTY_HIT_ON_WAR_LOSS | 0.95 | Drops the ruling party loyalty if war is lost. |
| RESEARCH_POINTS_ON_CONQUER_MULT | 360 | multiplier to Research Points got by conquering as unciv when got enacted military reforms |
| MAX_RESEARCH_POINTS | 25000 | max Research Points you can store as an unciv |

### Economy

| variable name | default value | description |
|---|---|---|
| MAX_DAILY_RESEARCH | 100 | The maximum stored research points that can be transferred to actual research per day |
| LOAN_BASE_INTEREST | 0.02 | Base interest rate per 30 days, see Interest |
| BANKRUPTCY_EXTERNAL_LOAN_YEARS | 10 |  |
| BANKRUPTCY_FACTOR | 0.2 |  |
| SHADOWY_FINANCIERS_MAX_LOAN_AMOUNT | 1500 |  |
| MAX_LOAN_CAP_FROM_BANKS | 3 | can loan max % of country tax base from single country |
| GUNBOAT_LOW_TAX_CAP | 0.0 |  |
| GUNBOAT_HIGH_TAX_CAP | 1.0 |  |
| GUNBOAT_FLEET_SIZE_FACTOR | 100 |  |
| PROVINCE_SIZE_DIVIDER | 50 |  |
| CAPITALIST_BUILD_FACTORY_STATE_EMPLOYMENT_PERCENT | 0.7 | Capitalists don't build factories if less than this percent is employed in existing factories |
| GOODS_FOCUS_SWAP_CHANCE | 0 | Percent increased chance that artisans want to change goods independantly of how well he is doing presently |
| NUM_CLOSED_FACTORIES_PER_STATE_LASSIEZ_FAIRE | 1 | Number of closed factories allowed per state under Laissez Faire |
| MIN_NUM_FACTORIES_PER_STATE_BEFORE_DELETING_LASSIEZ_FAIRE | 2 | Min number of factories per state before starting to delete under Laissez Faire |
| BANKRUPCY_DURATION | 2 | Years until a bancrupcy clears all loans |
| SECOND_RANK_BASE_SHARE_FACTOR | 0.5 |  |
| CIV_BASE_SHARE_FACTOR | 0.75 |  |
| UNCIV_BASE_SHARE_FACTOR | 1 |  |
| FACTORY_PAYCHECKS_LEFTOVER_FACTOR | 0.25 | % of how much we pay to the pops and capitalists, from the leftovers. |
| MAX_FACTORY_MONEY_SAVE | 1000 | how much money is stored maximum in a factory. |
| SMALL_DEBT_LIMIT | 500 |  |
| FACTORY_UPGRADE_EMPLOYEE_FACTOR | 0.95 | determines how close to the employee limit we need to be before "upgrade all" will upgrade/expand a given factory (1 = 100%). |
| RGO_SUPPLY_DEMAND_FACTOR_HIRE_HI | 0.2 | how fast pops are Hired when there is a high demand |
| RGO_SUPPLY_DEMAND_FACTOR_HIRE_LO | 0.02 | how fast pops are Hired when there is a medium demand |
| RGO_SUPPLY_DEMAND_FACTOR_FIRE | 0.4 | how fast pops are Fired when there is a low demand |
| EMPLOYMENT_HIRE_LOWEST | 0.001 | we Hire pops no slower then x% of total required per day |
| EMPLOYMENT_FIRE_LOWEST | 0.001 | we Fire pops no slower then x% of total required per day |
| TRADE_CAP_LOW_LIMIT_LAND | 0 | the lowest % the budget slider can go for land units |
| TRADE_CAP_LOW_LIMIT_NAVAL | 0.3 | the lowest % the budget slider can go for naval units |
| TRADE_CAP_LOW_LIMIT_CONSTRUCTIONS | 0 | the lowest % the budget slider can go for constructions |
| FACTORY_PURCHASE_MIN_FACTOR | 0.75 | the lowest % of its daily needs a factory will purchase |
| FACTORY_PURCHASE_DRAWDOWN_FACTOR | 0.025 | the % a factory will reduce its input purchases each day if it did not sell all its goods (also used for scaling up production if all goods are sold) |

### Military

| variable name | default value | description |
|---|---|---|
| DIG_IN_INCREASE_EACH_DAYS | 5 |  |
| REINFORCE_SPEED | 0.2 |  |
| COMBAT_DIFFICULTY_IMPACT | 0.2 |  |
| BASE_COMBAT_WIDTH | 30 |  |
| POP_MIN_SIZE_FOR_REGIMENT | 1000 | Amount of POPs per regiment in primary culture divisions |
| POP_SIZE_PER_REGIMENT | 3000 | Amount of POPs per regiment in non-primary culture divisions |
| SOLDIER_TO_POP_DAMAGE | 0.2 | POP casualties per soldier |
| LAND_SPEED_MODIFIER | 1 |  |
| NAVAL_SPEED_MODIFIER | 2 |  |
| EXP_GAIN_DIV | 0.05 |  |
| LEADER_RECRUIT_COST | 20 | the amount of leadership points it takes to recruit an officer |
| SUPPLY_RANGE | 250 |  |
| POP_MIN_SIZE_FOR_REGIMENT_PROTECTORATE_MULTIPLIER | 8 |  |
| POP_MIN_SIZE_FOR_REGIMENT_COLONY_MULTIPLIER | 5 |  |
| POP_MIN_SIZE_FOR_REGIMENT_NONCORE_MULTIPLIER | 3 | VALUE * POP_MIN_SIZE_FOR_REGIMENT is min for noncores |
| GAS_ATTACK_MODIFIER | 3 |  |
| COMBATLOSS_WAR_EXHAUSTION | 3 | base war exhaustion in combat |
| LEADER_MAX_RANDOM_PRESTIGE | 0.05 | max percent of prestige, when randomizing stats for leaders. |
| LEADER_AGE_DEATH_FACTOR | 4 | higher value means leaders live longer |
| LEADER_PRESTIGE_TO_MORALE_FACTOR | 0.8 | f.ex. 100% of prestige = +10% morale |
| LEADER_PRESTIGE_TO_MAX_ORG_FACTOR | 0.7 | f.ex. 100% of prestige = +10 max org |
| LEADER_TRANSFER_PENALTY_ON_COUNTRY_PRESTIGE | 0.05 | country prestige penalty on unassign leader (f.ex if leader has 100% prestige, the country loose 4% of its prestige) |
| LEADER_PRESTIGE_LAND_GAIN | 0.3 | extra speed gain on prestige for land combat |
| LEADER_PRESTIGE_NAVAL_GAIN | 0.3 | extra speed gain on prestige for naval combat |
| NAVAL_COMBAT_SEEKING_CHANCE | 0.5 | base chance of picking a target (increased by leader reconaissance) |
| NAVAL_COMBAT_SEEKING_CHANCE_MIN | 0.1 | low cap for chance of picking the target |
| NAVAL_COMBAT_SELF_DEFENCE_CHANCE | 2.0 | scale up the chance of choosing the target that is already shooting at us. |
| NAVAL_COMBAT_SHIFT_BACK_ON_NEXT_TARGET | 0.2 | max shift back from center line when got new target |
| NAVAL_COMBAT_SHIFT_BACK_DURATION_SCALE | 7 | shifting back from center line on new target - scaled down as long the combat takes |
| NAVAL_COMBAT_SPEED_TO_DISTANCE_FACTOR | 0.05 | cast the ship speed to the "in combat" speed that moves it towards center line on the field range 0-1. |
| NAVAL_COMBAT_CHANGE_TARGET_CHANCE | 0.03 | chance of changing the target to another one |
| NAVAL_COMBAT_DAMAGE_ORG_MULT | 0.4 | scale the damage to ORG for balancing gameplay |
| NAVAL_COMBAT_DAMAGE_STR_MULT | 0.2 | scale the damage to STR for balancing gameplay |
| NAVAL_COMBAT_DAMAGE_MULT_NO_ORG | 2.0 | damage multiplier (to STR) when opponent has no ORG. |
| NAVAL_COMBAT_RETREAT_CHANCE | 0.07 | base chance for retreating when STR or ORG is low. Increased by leader experiance and speed. |
| NAVAL_COMBAT_RETREAT_STR_ORG_LEVEL | 0.15 | the retreating is available when STR or ORG % drops below this value (it's 0% to 100% value) |
| NAVAL_COMBAT_RETREAT_SPEED_MOD | 0.4 | slow down when retreating so there is a chance to hit the runner |
| NAVAL_COMBAT_RETREAT_MIN_DISTANCE | 0.25 | how close (in average) all alive ships must be to the center line to be able to retreat. |
| NAVAL_COMBAT_DAMAGED_TARGET_SELECTION | 2.5 | multiply chance of seleting target that has low average of STR/ORG |
| NAVAL_COMBAT_STACKING_TARGET_CHANGE | 0.03 | increase chance to change/drop target when suffering stacking penalty |
| NAVAL_COMBAT_STACKING_TARGET_SELECT | 0.2 | modifier for how much the stacking penalty affects the target selection. |
| NAVAL_COMBAT_MAX_TARGETS | 6 | max number of ships that may target the same enemy ship |
| AI_BIGSHIP_PROPORTION | 0.4 | fraction of ships in the navy that should be ships of the line |
| AI_LIGHTSHIP_PROPORTION | 0.4 | fraction of ships in the navy that should be cruisers, frigates etc |
| AI_TRANSPORT_PROPORTION | 0.2 | fraction of ships in the navy that should be should be transports |
| AI_CAVALRY_PROPORTION | 0.15 | fraction of brigades that should be cavalry |
| AI_SUPPORT_PROPORTION | 0.3 | fraction of brigades that should be artillery and other support units |
| AI_SPECIAL_PROPORTION | 0.15 | fraction of brigades that should be engineers and tanks |
| AI_ESCORT_RATIO | 2.0 | ratio of escorts to transports in invasion fleets |
| AI_ARMY_TAXBASE_FRACTION | 0.3 | max of tax base that AI will spend on army supply costs (based on peacetime costs) |
| AI_NAVY_TAXBASE_FRACTION | 0.3 | max of tax base that AI will spend on navy supply costs (based on peacetime costs) |
| AI_BLOCKADE_RANGE | 200 | max distance the AI will send out blockade fleets from their home base |
| RECON_UNIT_RATIO | 0.1 | the % of units in the army that must have a recon value to get the full bonus |
| ENGINEER_UNIT_RATIO | 0.1 | the % of units in the army that must have a fort attack value to get the full bonus |
| SIEGE_BRIGADES_MIN | 3 | the number of brigades needed for a siege to progress at normal speed |
| SIEGE_BRIGADES_MAX | 13 | the number of brigades above which you get no addition benefit in sieges |
| SIEGE_BRIGADES_BONUS | 0.5 | the bonus to siege speed from each brigade |
| RECON_SIEGE_EFFECT | 0.5 | multiplier to effect of recon on speeding up sieges |
| SIEGE_ATTRITION | 2 | fixed attrition on sieging units |
| BASE_MILITARY_TACTICS | 1.5 | base mil tactics before tech |
| NAVAL_LOW_SUPPLY_DAMAGE_SUPPLY_STATUS | 0.25 | how little supply is acceptable before getting damage to STR |
| NAVAL_LOW_SUPPLY_DAMAGE_DAYS_DELAY | 30 | delay in days before the STR will get damage due to no supplies. Sometimes supply status may jump bcoz of the market. |
| NAVAL_LOW_SUPPLY_DAMAGE_MIN_STR | 5.0 | when low supply, the navy will supply STR damage but no less then X% to avoid destruction (value from 0 to 100.0) |
| NAVAL_LOW_SUPPLY_DAMAGE_PER_DAY | 0.25 | damage to navies STR per day if totally 0% supplies (value from 0 to 100.0) |

### Diplomacy

#### Warfare and casus belli

| variable name | default value | description |
|---|---|---|
| PEACE_COST_ADD_TO_SPHERE | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_RELEASE_PUPPET | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_MAKE_PUPPET | 85 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_DISARMAMENT | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_DESTROY_FORTS | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_DESTROY_NAVAL_BASES | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_REPARATIONS | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_TRANSFER_PROVINCES | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_REMOVE_CORES | 0 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_PRESTIGE | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_CONCEDE | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_STATUS_QUO | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_ANNEX | 85 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_DEMAND_STATE | 10 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_INSTALL_COMMUNIST_GOV_TYPE | 70 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_UNINSTALL_COMMUNIST_GOV_TYPE | 1 | The amount of war score required when negotiating a peace deal |
| PEACE_COST_COLONY | 10 | The amount of war score required when negotiating a peace deal |
| INFAMY_ADD_TO_SPHERE | 2 | The max amount of infamy gained when fabricating a add to sphere casus belli |
| INFAMY_RELEASE_PUPPET | 0.5 | The max amount of infamy gained when fabricating a release puppet casus belli |
| INFAMY_MAKE_PUPPET | 5 | The max amount of infamy gained when fabricating a puppet casus belli |
| INFAMY_DISARMAMENT | 5 |  |
| INFAMY_DESTROY_FORTS | 2 |  |
| INFAMY_DESTROY_NAVAL_BASES | 2 |  |
| INFAMY_REPARATIONS | 5 |  |
| INFAMY_TRANSFER_PROVINCES | 5 | The base amount of infamy gained when fabricating a Acquire State casus belli |
| INFAMY_REMOVE_CORES | 0 |  |
| INFAMY_PRESTIGE | 2 |  |
| INFAMY_CONCEDE | 1 |  |
| INFAMY_STATUS_QUO | 0 |  |
| INFAMY_ANNEX | 10 | The base amount of infamy gained when fabricating a Conquest casus belli |
| INFAMY_DEMAND_STATE | 5 |  |
| INFAMY_INSTALL_COMMUNIST_GOV_TYPE | 5 |  |
| INFAMY_UNINSTALL_COMMUNIST_GOV_TYPE | 5 |  |
| INFAMY_COLONY | 0 |  |
| PRESTIGE_ADD_TO_SPHERE_BASE | 5 |  |
| PRESTIGE_RELEASE_PUPPET_BASE | 5 |  |
| PRESTIGE_MAKE_PUPPET_BASE | 5 |  |
| PRESTIGE_DISARMAMENT_BASE | 5 |  |
| PRESTIGE_DESTROY_FORTS_BASE | 5 |  |
| PRESTIGE_DESTROY_NAVAL_BASES_BASE | 5 |  |
| PRESTIGE_REPARATIONS_BASE | 5 |  |
| PRESTIGE_TRANSFER_PROVINCES_BASE | 2 |  |
| PRESTIGE_REMOVE_CORES_BASE | 0 |  |
| PRESTIGE_PRESTIGE_BASE | 5 |  |
| PRESTIGE_CONCEDE_BASE | 1 |  |
| PRESTIGE_STATUS_QUO_BASE | 5 |  |
| PRESTIGE_ANNEX_BASE | 2 |  |
| PRESTIGE_DEMAND_STATE_BASE | 2 |  |
| PRESTIGE_CLEAR_UNION_SPHERE_BASE | 15 | Prestige for winning a war with the *asserting hegemony* war goal |
| PRESTIGE_GUNBOAT_BASE | 1 | Prestige for winning a war with the *debt collection* war goal |
| PRESTIGE_INSTALL_COMMUNIST_GOV_TYPE_BASE | 2 |  |
| PRESTIGE_UNINSTALL_COMMUNIST_GOV_TYPE_BASE | 2 |  |
| PRESTIGE_COLONY_BASE | 2 |  |
| PRESTIGE_ADD_TO_SPHERE | 0.05 | Prestige for winning a war with the *add to sphere* war goal |
| PRESTIGE_RELEASE_PUPPET | 0.05 | Prestige for winning a war with the *release puppet* war goal |
| PRESTIGE_MAKE_PUPPET | 0.05 | Prestige for winning a war with the *make puppet* war goal |
| PRESTIGE_DISARMAMENT | 0.05 |  |
| PRESTIGE_DESTROY_FORTS | 0.05 |  |
| PRESTIGE_DESTROY_NAVAL_BASES | 0.05 |  |
| PRESTIGE_REPARATIONS | 0.05 |  |
| PRESTIGE_TRANSFER_PROVINCES | 0.02 |  |
| PRESTIGE_REMOVE_CORES | 0 |  |
| PRESTIGE_PRESTIGE | 0.05 |  |
| PRESTIGE_CONCEDE | 0.01 |  |
| PRESTIGE_STATUS_QUO | 0.05 | Prestige for winning a war with the *Status Quo* war goal |
| PRESTIGE_ANNEX | 0.02 |  |
| PRESTIGE_DEMAND_STATE | 0.02 |  |
| PRESTIGE_CLEAR_UNION_SPHERE | 0.15 |  |
| PRESTIGE_GUNBOAT | 0.01 | Prestige for winning a war with the *debt collection* war goal |
| PRESTIGE_INSTALL_COMMUNIST_GOV_TYPE | 0.02 | Prestige for winning a war with the *Install Communism* war goal |
| PRESTIGE_UNINSTALL_COMMUNIST_GOV_TYPE | 0.02 | Prestige for winning a war with the *Uninstall Communism* war goal |
| PRESTIGE_COLONY | 0.02 |  |

##### Unused Casus belli

These defines are not in use in the game, as it is not possible to break truces in vanilla Victoria 2.

| variable name | default value | description |
|---|---|---|
| BREAKTRUCE_INFAMY_ADD_TO_SPHERE | 1 |  |
| BREAKTRUCE_INFAMY_RELEASE_PUPPET | 1 |  |
| BREAKTRUCE_INFAMY_MAKE_PUPPET | 1 |  |
| BREAKTRUCE_INFAMY_DISARMAMENT | 1 |  |
| BREAKTRUCE_INFAMY_DESTROY_FORTS | 1 |  |
| BREAKTRUCE_INFAMY_DESTROY_NAVAL_BASES | 1 |  |
| BREAKTRUCE_INFAMY_REPARATIONS | 1 |  |
| BREAKTRUCE_INFAMY_TRANSFER_PROVINCES | 1 |  |
| BREAKTRUCE_INFAMY_REMOVE_CORES | 0 |  |
| BREAKTRUCE_INFAMY_PRESTIGE | 1 |  |
| BREAKTRUCE_INFAMY_CONCEDE | 1 |  |
| BREAKTRUCE_INFAMY_STATUS_QUO | 1 |  |
| BREAKTRUCE_INFAMY_ANNEX | 1 |  |
| BREAKTRUCE_INFAMY_DEMAND_STATE | 1 |  |
| BREAKTRUCE_INFAMY_INSTALL_COMMUNIST_GOV_TYPE | 1 |  |
| BREAKTRUCE_INFAMY_UNINSTALL_COMMUNIST_GOV_TYPE | 1 |  |
| BREAKTRUCE_INFAMY_COLONY | 1 |  |
| BREAKTRUCE_PRESTIGE_ADD_TO_SPHERE | -20 |  |
| BREAKTRUCE_PRESTIGE_RELEASE_PUPPET | -20 |  |
| BREAKTRUCE_PRESTIGE_MAKE_PUPPET | -20 |  |
| BREAKTRUCE_PRESTIGE_DISARMAMENT | -20 |  |
| BREAKTRUCE_PRESTIGE_DESTROY_FORTS | -20 |  |
| BREAKTRUCE_PRESTIGE_DESTROY_NAVAL_BASES | -20 |  |
| BREAKTRUCE_PRESTIGE_REPARATIONS | -20 |  |
| BREAKTRUCE_PRESTIGE_TRANSFER_PROVINCES | -20 |  |
| BREAKTRUCE_PRESTIGE_REMOVE_CORES | 0 |  |
| BREAKTRUCE_PRESTIGE_PRESTIGE | -20 |  |
| BREAKTRUCE_PRESTIGE_CONCEDE | -20 |  |
| BREAKTRUCE_PRESTIGE_STATUS_QUO | -20 |  |
| BREAKTRUCE_PRESTIGE_ANNEX | -20 |  |
| BREAKTRUCE_PRESTIGE_DEMAND_STATE | -20 |  |
| BREAKTRUCE_PRESTIGE_INSTALL_COMMUNIST_GOV_TYPE | -20 |  |
| BREAKTRUCE_PRESTIGE_UNINSTALL_COMMUNIST_GOV_TYPE | -20 |  |
| BREAKTRUCE_PRESTIGE_COLONY | -20 |  |
| BREAKTRUCE_MILITANCY_ADD_TO_SPHERE | 2 |  |
| BREAKTRUCE_MILITANCY_RELEASE_PUPPET | 2 |  |
| BREAKTRUCE_MILITANCY_MAKE_PUPPET | 2 |  |
| BREAKTRUCE_MILITANCY_DISARMAMENT | 2 |  |
| BREAKTRUCE_MILITANCY_DESTROY_FORTS | 2 |  |
| BREAKTRUCE_MILITANCY_DESTROY_NAVAL_BASES | 2 |  |
| BREAKTRUCE_MILITANCY_REPARATIONS | 2 |  |
| BREAKTRUCE_MILITANCY_TRANSFER_PROVINCES | 2 |  |
| BREAKTRUCE_MILITANCY_REMOVE_CORES | 0 |  |
| BREAKTRUCE_MILITANCY_PRESTIGE | 2 |  |
| BREAKTRUCE_MILITANCY_CONCEDE | 2 |  |
| BREAKTRUCE_MILITANCY_STATUS_QUO | 2 |  |
| BREAKTRUCE_MILITANCY_ANNEX | 2 |  |
| BREAKTRUCE_MILITANCY_DEMAND_STATE | 2 |  |
| BREAKTRUCE_MILITANCY_INSTALL_COMMUNIST_GOV_TYPE | 2 |  |
| BREAKTRUCE_MILITANCY_UNINSTALL_COMMUNIST_GOV_TYPE | 2 |  |
| BREAKTRUCE_MILITANCY_COLONY | 2 |  |

#### Diplomatic actions

| variable name | default value | description |
|---|---|---|
| DISCREDIT_DAYS | 180 | How long the effects of discrediting another great power will be in place |
| DISCREDIT_INFLUENCE_COST_FACTOR | 2 |  |
| DISCREDIT_INFLUENCE_GAIN_FACTOR | -0.75 | The influence effects of discrediting |
| BANEMBASSY_DAYS | 365 | How long banning an embassy will have effect |
| DECLAREWAR_RELATION_ON_ACCEPT | -50 | The relation effect of declaring war. |
| DECLAREWAR_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to declare war |
| ADDWARGOAL_RELATION_ON_ACCEPT | 0 |  |
| ADDWARGOAL_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to add additional war goals |
| ADD_UNJUSTIFIED_GOAL_BADBOY | 1 |  |
| PEACE_RELATION_ON_ACCEPT | 5 | The relation effect of accepting a peace offer. |
| PEACE_RELATION_ON_DECLINE | -10 | The relation effect of refusing a peace offer. |
| PEACE_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to send a peace offer |
| ALLIANCE_RELATION_ON_ACCEPT | 100 | The relation effect of accepting an alliance. |
| ALLIANCE_RELATION_ON_DECLINE | -50 | The relation effect of refusing an alliance. |
| ALLIANCE_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to propose an alliance |
| CANCELALLIANCE_RELATION_ON_ACCEPT | -20 | The relation effect of canceling an alliance. |
| CANCELALLIANCE_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to cancel an alliance |
| CALLALLY_RELATION_ON_ACCEPT | 20 | The relation effect of accepting a call to war. |
| CALLALLY_RELATION_ON_DECLINE | -20 | The relation effect of refusing a call to war. |
| CALLALLY_DIPLOMATIC_COST | 0 | A value of 0 means, there is no actual ingame effect |
| ASKMILACCESS_RELATION_ON_ACCEPT | 30 | The relation effect of providing military access when it was asked for. |
| ASKMILACCESS_RELATION_ON_DECLINE | -10 | The relation effect of refusing to provide military access when it was asked for. |
| ASKMILACCESS_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to give military access  when it was asked for |
| CANCELASKMILACCESS_RELATION_ON_ACCEPT | 0 | The relation effect of cancelling military access |
| CANCELASKMILACCESS_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to cancel military access |
| GIVEMILACCESS_RELATION_ON_ACCEPT | 10 | The relation effect of providing military access when the provider took the initiative |
| GIVEMILACCESS_RELATION_ON_DECLINE | 0 | A value of 0 means, there is no actual ingame effect. |
| GIVEMILACCESS_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to give military access when the provider took the initiative |
| CANCELGIVEMILACCESS_RELATION_ON_ACCEPT | -10 | The relation effect of cancelling military access |
| CANCELGIVEMILACCESS_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to cancel military access |
| WARSUBSIDY_RELATION_ON_ACCEPT | 20 | The relation effect of providing war subsidies |
| WARSUBSIDY_DIPLOMATIC_COST | 1 | The amount of diplomatic points it takes to start war subsidies. There is no ongoing DP cost. |
| CANCELWARSUBSIDY_RELATION_ON_ACCEPT | 0 | A value of 0 means, there is no actual ingame effect |
| CANCELWARSUBSIDY_DIPLOMATIC_COST | 0 | A value of 0 means, there is no actual ingame effect |
| DISCREDIT_RELATION_ON_ACCEPT | -5 | The relation effect of discrediting another great power |
| DISCREDIT_INFLUENCE_COST | 25 | The amount of influence it takes to discredit another great power |
| EXPELADVISORS_RELATION_ON_ACCEPT | -5 | The relation effect of expelling the advisors of another great power |
| EXPELADVISORS_INFLUENCE_COST | 50 | The amount of influence it takes to expel the advisors of another great power |
| CEASECOLONIZATION_RELATION_ON_ACCEPT | 20 |  |
| CEASECOLONIZATION_RELATION_ON_DECLINE | -20 |  |
| CEASECOLONIZATION_DIPLOMATIC_COST | 1 |  |
| BANEMBASSY_RELATION_ON_ACCEPT | -10 | the relation effect between the two great powers when banning an embassy |
| BANEMBASSY_INFLUENCE_COST | 65 | The amount of influence it takes to ban another GP's embassy |
| INCREASERELATION_RELATION_ON_ACCEPT | 15 | The relation effect of increasing relations |
| INCREASERELATION_RELATION_ON_DECLINE | 0 |  |
| INCREASERELATION_DIPLOMATIC_COST | 2 | The cost in diplomatic points of increasing relations |
| DECREASERELATION_RELATION_ON_ACCEPT | -25 | The relation effect of decreasing relations |
| DECREASERELATION_DIPLOMATIC_COST | 1 | The cost in diplomatic points of decreasing relations |
| ADDTOSPHERE_RELATION_ON_ACCEPT | 0 | The relation effect of adding a country to a sphere of influence (a value of 0 means there is no actual effect in Vanilla Victoria 2) |
| ADDTOSPHERE_INFLUENCE_COST | 100 | The amount of influence it takes to add a country to a sphere of influence |
| REMOVEFROMSPHERE_RELATION_ON_ACCEPT | -10 | The relation effect of removing a country from another country's sphere of influence between the formerly sphered country and their former spheremaster |
| REMOVEFROMSPHERE_INFLUENCE_COST | 100 | The amount of influence it takes to removing a country from another GP's sphere of influence |
| REMOVEFROMSPHERE_PRESTIGE_COST | 10 | only applied if removing country is sphere leader |
| REMOVEFROMSPHERE_INFAMY_COST | 1 | only applied if removing country is sphere leader |
| INCREASEOPINION_RELATION_ON_ACCEPT | 20 | The relation effect of increasing the opinion of a country |
| INCREASEOPINION_INFLUENCE_COST | 50 | The amount of influence it takes to increase the opinion of a country |
| DECREASEOPINION_RELATION_ON_ACCEPT | -10 | The relation effect of decreasing the opinion of another GB in a certain country |
| DECREASEOPINION_INFLUENCE_COST | 50 | The amount of influence it takes to decrease the opinion of a country |
| CEASECOLONIZATION_DIPLOMATIC_COST | 1 |  |
| MAKE_CB_DIPLOMATIC_COST | 1 |  |
| MAKE_CB_RELATION_ON_ACCEPT | 0 |  |

#### Other

| variable name | default value | description |
|---|---|---|
| GOODRELATION_INFAMY_ADD_TO_SPHERE | 1 |  |
| GOODRELATION_INFAMY_RELEASE_PUPPET | 1 |  |
| GOODRELATION_INFAMY_MAKE_PUPPET | 1 |  |
| GOODRELATION_INFAMY_DISARMAMENT | 1 |  |
| GOODRELATION_INFAMY_DESTROY_FORTS | 1 |  |
| GOODRELATION_INFAMY_DESTROY_NAVAL_BASES | 1 |  |
| GOODRELATION_INFAMY_REPARATIONS | 1 |  |
| GOODRELATION_INFAMY_TRANSFER_PROVINCES | 1 |  |
| GOODRELATION_INFAMY_REMOVE_CORES | 0 |  |
| GOODRELATION_INFAMY_PRESTIGE | 1 |  |
| GOODRELATION_INFAMY_CONCEDE | 1 |  |
| GOODRELATION_INFAMY_STATUS_QUO | 1 |  |
| GOODRELATION_INFAMY_ANNEX | 1 |  |
| GOODRELATION_INFAMY_DEMAND_STATE | 1 |  |
| GOODRELATION_INFAMY_INSTALL_COMMUNIST_GOV_TYPE | 1 |  |
| GOODRELATION_INFAMY_UNINSTALL_COMMUNIST_GOV_TYPE | 1 |  |
| GOODRELATION_INFAMY_COLONY | 1 |  |
| GOODRELATION_PRESTIGE_ADD_TO_SPHERE | -20 |  |
| GOODRELATION_PRESTIGE_RELEASE_PUPPET | -20 |  |
| GOODRELATION_PRESTIGE_MAKE_PUPPET | -20 |  |
| GOODRELATION_PRESTIGE_DISARMAMENT | -20 |  |
| GOODRELATION_PRESTIGE_DESTROY_FORTS | -20 |  |
| GOODRELATION_PRESTIGE_DESTROY_NAVAL_BASES | -20 |  |
| GOODRELATION_PRESTIGE_REPARATIONS | -20 |  |
| GOODRELATION_PRESTIGE_TRANSFER_PROVINCES | -20 |  |
| GOODRELATION_PRESTIGE_REMOVE_CORES | 0 |  |
| GOODRELATION_PRESTIGE_PRESTIGE | -20 |  |
| GOODRELATION_PRESTIGE_CONCEDE | -20 |  |
| GOODRELATION_PRESTIGE_STATUS_QUO | -20 |  |
| GOODRELATION_PRESTIGE_ANNEX | -20 |  |
| GOODRELATION_PRESTIGE_DEMAND_STATE | -20 |  |
| GOODRELATION_PRESTIGE_INSTALL_COMMUNIST_GOV_TYPE | -20 |  |
| GOODRELATION_PRESTIGE_UNINSTALL_COMMUNIST_GOV_TYPE | -20 |  |
| GOODRELATION_PRESTIGE_COLONY | -20 |  |
| GOODRELATION_MILITANCY_ADD_TO_SPHERE | 2 |  |
| GOODRELATION_MILITANCY_RELEASE_PUPPET | 2 |  |
| GOODRELATION_MILITANCY_MAKE_PUPPET | 2 |  |
| GOODRELATION_MILITANCY_DISARMAMENT | 2 |  |
| GOODRELATION_MILITANCY_DESTROY_FORTS | 2 |  |
| GOODRELATION_MILITANCY_DESTROY_NAVAL_BASES | 2 |  |
| GOODRELATION_MILITANCY_REPARATIONS | 2 |  |
| GOODRELATION_MILITANCY_TRANSFER_PROVINCES | 2 |  |
| GOODRELATION_MILITANCY_REMOVE_CORES | 0 |  |
| GOODRELATION_MILITANCY_PRESTIGE | 2 |  |
| GOODRELATION_MILITANCY_CONCEDE | 2 |  |
| GOODRELATION_MILITANCY_STATUS_QUO | 2 |  |
| GOODRELATION_MILITANCY_ANNEX | 2 |  |
| GOODRELATION_MILITANCY_DEMAND_STATE | 2 |  |
| GOODRELATION_MILITANCY_INSTALL_COMMUNIST_GOV_TYPE | 2 |  |
| GOODRELATION_MILITANCY_UNINSTALL_COMMUNIST_GOV_TYPE | 2 |  |
| GOODRELATION_MILITANCY_COLONY | 2 |  |
| WAR_PRESTIGE_COST_BASE | 100 |  |
| WAR_PRESTIGE_COST_HIGH_PRESTIGE | 1 |  |
| WAR_PRESTIGE_COST_NEG_PRESTIGE | 1 |  |
| WAR_PRESTIGE_COST_TRUCE | 100 |  |
| WAR_PRESTIGE_COST_HONOR_ALLIANCE | -100 |  |
| WAR_PRESTIGE_COST_HONOR_GUARNATEE | -50 |  |
| WAR_PRESTIGE_COST_UNCIVILIZED | -50 |  |
| WAR_PRESTIGE_COST_CORE | -50 |  |
| WAR_FAILED_GOAL_MILITANCY | 2 |  |
| WAR_FAILED_GOAL_PRESTIGE_BASE | -10 | When a war is lost the country loses 10 prestige as a base (+ 10 % of its current prestige, see below) |
| WAR_FAILED_GOAL_PRESTIGE | -0.1 | When a war is lost the country loses 10% of its current prestige (+ 10 prestige as a base, see above) |
| DISARMAMENT_ARMY_HIT | 0.5 |  |
| REPARATIONS_TAX_HIT | 0.25 |  |
| PRESTIGE_REDUCTION_BASE | 25 |  |
| PRESTIGE_REDUCTION | 0.1 | Base value + % of recipient's prestige |
| REPARATIONS_YEARS | 5 | The amount of years the reperations Casus belli effect lasts for |
| MIN_WARSCORE_TO_INTERVENE | -1 | The minimum war score needed for GB to be able to intervene in another war |
| MIN_MONTHS_TO_INTERVENE | 0 | A value of 0 means, there is no actual ingame effect |
| MAX_WARSCORE_FROM_BATTLES | 50 | The maximum warscore that can be achieved solely from winning battles |
| GUNBOAT_DIPLOMATIC_COST | 1 |  |
| GUNBOAT_RELATION_ON_ACCEPT | 1 |  |
| WARGOAL_JINGOISM_REQUIREMENT | 0.07 |  |
| LIBERATE_STATE_RELATION_INCREASE | 50 |  |
| DISHONORED_CALLALLY_PRESTIGE_PENALTY | -3 |  |
| BASE_TRUCE_MONTHS | 60 | The time a truce last |
| MAX_INFLUENCE | 100 | The maximum influence that a GB can store within a country |
| WARSUBSIDIES_PERCENT | 0.20 | How many percent of imports you are going to pay each day(mil. constructions and mil. maintainence) |
| NEIGHBOUR_BONUS_INFLUENCE_PERCENT | 0.50 | Bonus to neighbouring countries when influencing |
| SPHERE_NEIGHBOUR_BONUS_INFLUENCE_PERCENT | 0.2 | Bonus to countries in your sphere neighbouring when influencing |
| OTHER_CONTINENT_BONUS_INFLUENCE_PERCENT | -0.50 | Bonus to neighbouring countries when influencing |
| PUPPET_BONUS_INFLUENCE_PERCENT | 1.0 | bonus if they are our puppet |
| RELEASE_NATION_PRESTIGE | 0 |  |
| RELEASE_NATION_INFAMY | -5 | Infamy removed pr released country |
| INFAMY_CLEAR_UNION_SPHERE | 0 | Infamy for asserting hegemony |
| BREAKTRUCE_INFAMY_CLEAR_UNION_SPHERE | 1 | Infamy for breaking truce for asserting hegemony |
| BREAKTRUCE_PRESTIGE_CLEAR_UNION_SPHERE | -20 | Prestige for breaking truce for asserting hegemony |
| BREAKTRUCE_MILITANCY_CLEAR_UNION_SPHERE | 2 | Militancy for breaking truce for asserting hegemony |
| GOODRELATION_INFAMY_CLEAR_UNION_SPHERE | 1 | Militancy for asserting hegemony with good relations |
| GOODRELATION_PRESTIGE_CLEAR_UNION_SPHERE | -20 | Prestige for asserting hegemony with good relations |
| GOODRELATION_MILITANCY_CLEAR_UNION_SPHERE | 2 | Prestige for asserting hegemony with good relations |
| PEACE_COST_CLEAR_UNION_SPHERE | 0.6 | Peace cost to assert hegemony per affected country |
| GOOD_PEACE_REFUSAL_MILITANCY | 1.0 | Militancy hit from refusing a good peace offer |
| GOOD_PEACE_REFUSAL_WAREXH | 5.0 | War exhaustion hit from refusing a good peace offer |
| PEACE_COST_GUNBOAT | 5 | Cost of forcing a defaulting country to pay its debt |
| INFAMY_GUNBOAT | 0 | Infamy cost for debt collection |
| BREAKTRUCE_INFAMY_GUNBOAT | 0 | Truce breaking penalty for debt collection |
| BREAKTRUCE_PRESTIGE_GUNBOAT | 0 |  |
| BREAKTRUCE_MILITANCY_GUNBOAT | 0 |  |
| GOODRELATION_INFAMY_GUNBOAT | 0 |  |
| GOODRELATION_PRESTIGE_GUNBOAT | 0 |  |
| GOODRELATION_MILITANCY_GUNBOAT | 0 |  |
| CB_GENERATION_BASE_SPEED | 0.5 |  |
| CB_GENERATION_SPEED_BONUS_ON_COLONY_COMPETITION | 1.0 | speed bonus when 2 countries compete for colony province |
| CB_GENERATION_SPEED_BONUS_ON_COLONY_COMPETITION_TROOPS_PRESENCE | 1.0 | even bigger bonus when having |
| MAKE_CB_RELATION_LIMIT | 100 | Above this relation (on a -100 to 100 scale) makes fabricating casus belli impossible |
| CB_DETECTION_CHANCE_BASE | 15 | chance to be discovered when fabricating a casus belli out of 1000 every day |
| INVESTMENT_INFLUENCE_DEFENSE | 0.5 | maximum defense factor in sphere of having invested in a country |
| RELATION_INFLUENCE_MODIFIER | 1000 | divisor for relation |
| ON_CB_DETECTED_RELATION_CHANGE | -50 | relations decreased when CB detected. |
| GW_INTERVENE_MIN_RELATIONS | 100 | minimum relations required to intervene in great war |
| GW_INTERVENE_MAX_EXHAUSTION | 1 | max war exhaustion required to intervene in great war |
| GW_JUSTIFY_CB_BADBOY_IMPACT | 0.33 | % deduction of infamy cost for justify CB in great war |
| GW_CB_CONSTRUCTION_SPEED | 0.25 | faster Casus Belli construction against enemies while at great war |
| GW_WARGOAL_JINGOISM_REQUIREMENT_MOD | 0.25 | % deduction of required jingoists in country to add a secondary war goal during a great war |
| GW_WARSCORE_COST_MOD | 0.65 | cost reduction factor on warscore needed to fulfill goal if great war |
| TENSION_DECAY | -0.08 | base tension decay pr day |
| TENSION_FROM_CB | 0.04 |  |
| TENSION_FROM_MOVEMENT | 0.02 | tension per 1000 in nationalist movement |
| TENSION_FROM_MOVEMENT_MAX | 1.2 | max total value no matter the size of the movement |
| AT_WAR_TENSION_DECAY | -0.12 | for each potentially interested GP at war (value is if all possible GPs are at war) |
| TENSION_ON_CB_DISCOVERED | 20 |  |
| TENSION_ON_REVOLT | 50 |  |
| TENSION_WHILE_CRISIS | -1.0 |  |
| CRISIS_COOLDOWN_MONTHS | 18 |  |
| CRISIS_BASE_CHANCE | 20 |  |
| CRISIS_TEMPERATURE_INCREASE | 0.05 |  |
| CRISIS_OFFER_DIPLOMATIC_COST | 0 |  |
| CRISIS_OFFER_RELATION_ON_ACCEPT | 0 |  |
| CRISIS_OFFER_RELATION_ON_DECLINE | 0 |  |
| CRISIS_DID_NOT_TAKE_SIDE_PRESTIGE_FACTOR_BASE | -0.1 | the percentage of current prestige a great power loses from not taking sides during a crisis |
| CRISIS_DID_NOT_TAKE_SIDE_PRESTIGE_FACTOR_YEAR | -0.002 |  |
| CRISIS_WINNER_PRESTIGE_FACTOR_BASE | 10 |  |
| CRISIS_WINNER_PRESTIGE_FACTOR_YEAR | 0.4 |  |
| CRISIS_WINNER_RELATIONS_IMPACT | 25 | negative for losers and backers with unfulfilled goals |
| BACK_CRISIS_DIPLOMATIC_COST | 0 |  |
| BACK_CRISIS_RELATION_ON_ACCEPT | 0 |  |
| BACK_CRISIS_RELATION_ON_DECLINE | 0 |  |
| CRISIS_TEMPERATURE_ON_OFFER_DECLINE | 0 |  |
| CRISIS_TEMPERATURE_PARTICIPANT_FACTOR | 10 | How much faster a crisis heats up if all interested parties have taken sides (linear, multiplied) |
| CRISIS_TEMPERATURE_ON_MOBILIZE | 10 | added temperature if a participant mobilizes |
| CRISIS_WARGOAL_INFAMY_MULT | 1 | Applied to all infamy from adding wargoals in a crisis |
| CRISIS_WARGOAL_PRESTIGE_MULT | 1 | Applied to all prestige effects on wargoals in a crisis |
| CRISIS_WARGOAL_MILITANCY_MULT | 0 | Applied to all militancy from failed wargoals in a crisis |
| CRISIS_INTEREST_WAR_EXHAUSTION_LIMIT | 20 | GPs with WE above this will not get invited to a crisis |
| RANK_1_TENSION_DECAY | -0.5 | extra flashpoint tension decay for GPs |
| RANK_2_TENSION_DECAY | -0.4 |  |
| RANK_3_TENSION_DECAY | -0.3 |  |
| RANK_4_TENSION_DECAY | -0.2 |  |
| RANK_5_TENSION_DECAY | -0.08 |  |
| RANK_6_TENSION_DECAY | -0.06 |  |
| RANK_7_TENSION_DECAY | -0.04 |  |
| RANK_8_TENSION_DECAY | -0.02 |  |
| TWS_FULFILLED_SPEED | 0.1 | Ticking War Score grows with this speed daily once CB is fulfilled |
| TWS_NOT_FULFILLED_SPEED | 0.1 | Ticking War Score falls when CB is not fulfilled (or after grace period) |
| TWS_GRACE_PERIOD_DAYS | 730 | Ticking War Score delay before it starts falling down for not fulfilling CB. |
| TWS_CB_LIMIT_DEFAULT | 100 |  |
| TWS_FULFILLED_IDLE_SPACE | 0.75 | How much % the CB fulfillment must done, so TWS starts ticking. |
| TWS_BATTLE_MIN_COUNT | 5 | At least X battles before the aspect of wins will count |
| TWS_BATTLE_MAX_ASPECT | 8.0 | Max allowed battle wins aspect for TWS |
| LARGE_POPULATION_INFLUENCE_PENALTY | -0.4 |  |

### Pops

| variable name | default value | description |
|---|---|---|
| BASE_CLERGY_FOR_LITERACY | 0.005 |  |
| MAX_CLERGY_FOR_LITERACY | 0.04 | The percentage of clergymen where they stop having any more influence on literacy |
| LITERACY_CHANGE_SPEED | 0.1 |  |
| ASSIMILATION_SCALE | 0.004 |  |
| CONVERSION_SCALE | 0.01 |  |
| IMMIGRATION_SCALE | 0.004 |  |
| PROMOTION_SCALE | 0.002 |  |
| PROMOTION_ASSIMILATION_CHANCE | 1.0 |  |
| LUXURY_THRESHOLD | 500 |  |
| BASE_GOODS_DEMAND | 0.8 |  |
| BASE_POPGROWTH | 0.0001 |  |
| MIN_LIFE_RATING_FOR_GROWTH | 30 |  |
| LIFE_RATING_GROWTH_BONUS | 0.0001 |  |
| LIFE_NEED_STARVATION_LIMIT | 0.5 |  |
| MIL_LACK_EVERYDAY_NEED | 0.1 | militancy change from not having everyday needs fulfilled |
| MIL_HAS_EVERYDAY_NEED | -0.1 | militancy change from having everyday needs fulfilled |
| MIL_HAS_LUXURY_NEED | -0.2 | militancy change from having luxury needs fulfilled |
| MIL_NO_LIFE_NEED | 0.2 |  |
| MIL_REQUIRE_REFORM | 0.2 |  |
| MIL_IDEOLOGY | -0.1 |  |
| MIL_RULING_PARTY | -0.1 |  |
| MIL_REFORM_IMPACT | 2 |  |
| MIL_WAR_EXHAUSTION | 0.005 |  |
| MIL_NON_ACCEPTED | 0.05 |  |
| CON_LITERACY | 0.1 |  |
| CON_LUXURY_GOODS | 0.1 |  |
| CON_POOR_CLERGY | -2.5 |  |
| CON_MIDRICH_CLERGY | -1.25 |  |
| CON_REFORM_IMPACT | -50 |  |
| CON_COLONIAL_FACTOR | 0.5 |  |
| RULING_PARTY_HAPPY_CHANGE | -1 |  |
| RULING_PARTY_ANGRY_CHANGE | 2 |  |
| PDEF_BASE_CON | 20.0 | so half'ed effect. |
| NATIONAL_FOCUS_DIVIDER | 400000.0 | POPs needed per national focus point |
| POP_SAVINGS | 0.018 |  |
| STATE_CREATION_ADMIN_LIMIT | 0.01 |  |
| MIL_TO_JOIN_REBEL | 7 | Rebels over this will join a faction |
| MIL_TO_JOIN_RISING | 8 | Rebels over this will join a general rising |
| MIL_TO_AUTORISE | 9 | Rebels over this rise no matter what |
| REDUCTION_AFTER_RISEING | 0.0 | After a pop spawns a rebellion, its militancy will be reduced this much |
| REDUCTION_AFTER_DEFEAT | 3.0 | After a rebellion is being defeated in combat, its pop militancy will be divided by this number. (if value < 1.0 the MIL will be increased) (Beware! value must be > 0) |
| POP_TO_LEADERSHIP | 0.0001 | how much leadership every 1000 officer pops gives each day. |
| ARTISAN_MIN_PRODUCTIVITY | 1 | Minimum efficiency of an artisan pop |
| SLAVE_GROWTH_DIVISOR | 10 | Slaves have N times lower growth |
| MIL_HIT_FROM_CONQUEST | 4 | how much militancy grows in a province if taken without being core. |
| LUXURY_CON_CHANGE | 0.001 | conciousness boost from over-buying luxury goods |
| INVENTION_IMPACT_ON_DEMAND | 0.005 | how much each invention in a country increases demand for a product in percent |
| ARTISAN_SUPPRESSED_COLONIAL_GOODS_CATEGORY | 0 | Goods category index not produced in colonies |
| ISSUE_MOVEMENT_JOIN_LIMIT | 8 |  |
| ISSUE_MOVEMENT_LEAVE_LIMIT | 7 |  |
| MOVEMENT_CON_FACTOR | 0.05 |  |
| MOVEMENT_LIT_FACTOR | 0.3 |  |
| MIL_ON_REB_MOVE | 8 |  |
| POPULATION_SUPPRESSION_FACTOR | 0.0 | controls base pop size for factor of supression/radicalness cost. zero  disables the feature and jsut uses radicalness |
| POPULATION_MOVEMENT_RADICAL_FACTOR | 300 |  |
| NATIONALIST_MOVEMENT_MIL_CAP | 3.0 |  |
| MOVEMENT_SUPPORT_UH_FACTOR | 3 | 3x means 30% country support equals full UH support |
| REBEL_OCCUPATION_STRENGTH_BONUS | 0.01 | the amount of strength given to rebel movements when they occupy a province |
| LARGE_POPULATION_LIMIT | 9000000 |  |
| LARGE_POPULATION_INFLUENCE_PENALTY_CHUNK | 250000 |  |

### AI

| variable name | default value | description |
|---|---|---|
| COLONY_WEIGHT | 5.0 | ai weight for colonising |
| ADMINISTRATOR_WEIGHT | 10.0 | ai weight for new bureaucrat |
| INDUSTRYWORKER_WEIGHT | 10.0 | ai weight for new industry workers |
| EDUCATOR_WEIGHT | 10.0 | ai weigth for new clergy |
| SOLDIER_WEIGHT | 30.0 | ai weight for soldiers |
| SOLDIER_FRACTION | 0.03 | max amount of population AI wants to be soldiers |
| CAPITALIST_FRACTION | 0.001 | max amount of population AI wants to be capis |
| PRODUCTION_WEIGHT | 0.05 | ai weight for new production |
| SPAM_PENALTY | 10 | makes certain diplomatic action less common |
| ONE_SIDE_MAX_WARSCORE | 150 | don't add too many wargoals to one side in a war |
| POP_PROJECT_INVESTMENT_MAX_BUDGET_FACTOR | 0.25 | how much % of our current budget can be spend on the pop project investments. |
| RELATION_LIMIT_NO_ALLIANCE_OFFER | 0 | if relation lower then this value, AI will not ally |
| NAVAL_SUPPLY_PENALTY_LIMIT | 0.2 | AI will allow to have max X% of supply penalty (when too little naval bases) |
| CHANCE_BUILD_RAILROAD | 0.2 | chances in % of AI decisions (max value 1.0) |
| CHANCE_BUILD_NAVAL_BASE | 0.75 |  |
| CHANCE_BUILD_FORT | 0.5 |  |
| CHANCE_INVEST_POP_PROJ | 0.16 |  |
| CHANCE_FOREIGN_INVEST | 0.16 |  |
| TWS_AWARENESS_SCORE_LOW_CAP | 0.2 | AI will always add CBs if current warscore is less then that number (including TWS) |
| TWS_AWARENESS_SCORE_ASPECT | 0.5 | AI will not add any more CBs when TWS is more then X% of total WS. (to not destroy the progress) |
| PEACE_BASE_RELUCTANCE | 20 | AI base stubbornness to refuse peace (always applied) |
| PEACE_TIME_MONTHS | 30 | months of additional AI stubbornness in a war |
| PEACE_TIME_FACTOR | 0.6 | after months of stubbornness the effect of time passed is multiplied by this |
| PEACE_TIME_FACTOR_NO_GOALS | 2.0 | this extra time factor is applied after PEACE_TIME_FACTOR if we ahve no wargoals |
| PEACE_WAR_EXHAUSTION_FACTOR | 0.5 | AI willingness to peace based on war exhaustion |
| PEACE_WAR_DIRECTION_FACTOR | 1.0 | AI willingness to peace based on who's making gains in the war |
| PEACE_WAR_DIRECTION_WINNING_MULT | 5.0 | Multiplies AI emphasis on war direction if it's the one making gains |
| PEACE_FORCE_BALANCE_FACTOR | 0.3 | AI willingness to peace based on strength estimation of both sides |
| PEACE_ALLY_BASE_RELUCTANCE_MULT | 2.0 | Multiplies PEACE_BASE_RELUCTANCE for allies in a war |
| PEACE_ALLY_TIME_MULT | 0 | Multiplies PEACE_TIME_FACTOR for allies in a war |
| PEACE_ALLY_WAR_EXHAUSTION_MULT | 1.0 | Multiplies PEACE_WAR_EXHAUSTION_FACTOR for allies in a war |
| PEACE_ALLY_WAR_DIRECTION_MULT | 0 | Multiplies PEACE_WAR_DIRECTION_FACTOR for allies in a war |
| PEACE_ALLY_FORCE_BALANCE_MULT | 0 | Multiplies PEACE_FORCE_BALANCE_FACTOR for allies in a war |
| AGGRESSION_BASE | 5 | general AI aggression |
| AGGRESSION_UNCIV_BONUS | 10 | additional AI civ aggression against uncivs |
| FLEET_SIZE | 30 | AI will attempt to keep fleets of roughly this size (fewer fleets generally results in more competent naval AI) |
| MIN_FLEETS | 1 | Minimum amount of main fleets the AI will divide its navy into (does not include specialized fleets such as blockades and naval invasions) |
| MAX_FLEETS | 10 | Maximal amount of main fleets the AI will divide its navy into (does not include specialized fleets such as blockades and naval invasions) |
| MONTHS_BEFORE_DISBAND | 6 | Months from start date before AI will disband armies/navies (to avoid disbands because of early economic turmoil) |

### Graphics

| variable name | default value | description |
|---|---|---|
| CITIES_SPRAWL_OFFSET | 2 |  |
| CITIES_SPRAWL_WIDTH | 52 |  |
| CITIES_SPRAWL_HEIGHT | 52 |  |
| CITIES_SPRAWL_ITERATIONS | 30 |  |
| CITIES_MESH_POOL_SIZE_FOR_COUNTRY | 64 |  |
| CITIES_MESH_POOL_SIZE_FOR_CULTURE | 64 |  |
| CITIES_MESH_POOL_SIZE_FOR_GENERIC | 256 |  |
| CITIES_MESH_TYPES_COUNT | 3 |  |
| CITIES_MESH_SIZES_COUNT | 3 |  |
| CITIES_SPECIAL_BUILDINGS_POOL_SIZE | 64 |  |
| CITIES_SIZE_MAX_POPULATION_K | 1000 | When province population reach 1mln, the city will get it's maximum size. |
