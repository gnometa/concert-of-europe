# Modifier effects

Source: https://vic2.paradoxwikis.com/Modifier_effects

List of the variables that modifiers can affect. It is mainly used in [modding](modding.md) or to understand the files, if you want to read the exact effects of [decision](decision.md)s, [event](event.md)s and so forth.

### Country Modifiers

#### administrative_efficiency_modifier

Increases or reduces the country's administrative efficiency modifier. Affects states as well as the country wide admin efficiency.

Syntax: 
```
administrative_efficiency_modifier = n
```
```
where n = -0.1 is -0.1 admin efficiency or, in other words, -10% admin efficiency.
```

#### badboy

Fixed increase or decrease in infamy at the start of every month.

Syntax: 
```
 badboy = n
```
```
where n = -0.1 is -0.1 infamy
```

#### cb_generation_speed_modifier

Percentage increase/decrease in the rate at which CB's are justified by a country.

Syntax: 
```
cb_generation_speed_modifier = n
```
```
where n = 0.1 is a 10% increase in the speed.
```

#### core_pop_(trait)_modifer

Monthly increase or decrease in (trait) for all pops in core provinces (can be consciousness or militancy).

Syntax: 
```
core_pop_militancy_modifier = n
```
```
where n = 1 would add 1 MIL each month.
```

#### diplomatic_points_modifier

Percentage change in the monthly diplomatic points given to the country.

Syntax: 
```
diplomatic_points_modifier = n
```
```
where n = 0.1 would be a 10% increase in diplomatic points.
```

#### education_efficiency_modifier *AHD ONLY*

Percentage change in the country's education efficiency.

Syntax: 
```
education_efficiency_modifier = n
```
```
where n = 0.1 would be a 10% increase in efficiency.
```

#### factory_cost

Percentage increase/decrease in the cost of factories for the country.

Syntax: 
```
factory_cost = n
```
```
where n = 0.1 is a 10% increase in factory cost.
```

#### factory_input

Percentage change in the input of all factories in the country.

Syntax: 
```
factory_input = n
```
```
where n = 0.1 is a 10% increase in input.
```

#### factory_output

Percentage change in the output of all factories in the country.

Syntax: 
```
factory_output = n
```
```
where n = 0.1 is a 10% increase in output.
```

#### factory_owner_cost

Percentage increase/decrease in the cost of factories for the country.

Syntax: 
```
factory_owner_cost = n
```
```
where n = 0.1 is a 10% increase in factory cost.
```

#### factory_throughput

Percentage change in the throughput of all factories in the country.

Syntax: 
```
factory_throughput = n
```
```
where n = 0.1 is a 10% increase in throughput.
```

#### global_assimilation_rate

Percentage change in the assimiliation rate of foreign culture pops in a country.

Syntax: 
```
global_assimilation_rate = n
```
```
where n = 0.1 would be a 10% increase.
```

#### global_immigrant_attract

Increases or decreases the attractiveness of the country to prospective immigrants.

Syntax: 
```
global_immigrant_attract = n
```
```
where n = 1 would be a 100% increase.
```

#### global_pop_(trait)_modifier

Monthly increase or decrease in (trait) for all pops (can be consciousness or militancy).

Syntax: 
```
global_pop_militancy_modifier = n
```
```
where n = 1 would add 1 MIL each month.
```

#### global_population_growth

Percentage increase or decrease in the natural growth of pops in the entire country.

Syntax: 
```
global_population_growth = n
```
```
where n = 0.1 would be a 10% increase in the growth rate.
```

#### import_cost

The amount in percentage that an extra cost is imposed on imported goods.

Syntax: 
```
import_cost = n
```
```
where n = 0.1 would make imported goods 10% more expensive.
```

#### influence_modifier

Percentage change in the base influence points the country generates.

Syntax: 
```
influence_modifier = n
```
```
where n = 0.1 would be a 10% increase in base influence gain.
```

#### issue_change_speed

Percentage increase in the rate at which pops change their issue interest.

Syntax: 
```
issue_change_speed = n
```
```
where n = 0.1 would be a 10% increase to the speed.
```

#### land_organisation

Percentage increase in the organization levels for a country's armies.

Syntax: 
```
land_organisation = n
```
```
where n = 0.1 would be a 10% increase to organization.
```

#### land_unit_start_experience

Fixed percentage point change in the starting experience of new land units.

Syntax: 
```
land_unit_start_experience = n
```
```
where n = 15 would start new land units with 15% (out of 100%) experience, <i>ceteris paribus</i>.
```

#### leadership_modifier

Percentage increase or decrease in the rate of Leadership generation.

Syntax: 
```
 leadership_modifier = n 
```
```
where n = 1 would double the production (+100%)
```

#### loan_interest

Change in the interest applied to foreign loans

Syntax: 
```
loan_interest = n
```
```
where n = 0.1 is an increase of 10% interest.
```
For more Information about interest click here.

#### max_loan_modifier

Percentage increase or decrease in the maximum loan the country can take.

Syntax: 
```
max_loan_modifier = n
```
```
where n = 0.1 is an increase of 10% in maximum loan size.
```

#### max_military_spending

Change in the maximum military spending threshold.

Syntax: 
```
max_military_spending = n
```
```
where n = 0.1 increases the maximum military spending threshold by 10%
```
Note: The max military spending you can limit a nation to is 1% (max_military_spending = 0.99). At 100% (max_military_spending = 1) this modifier doesn't work.

#### max_social_spending

Change in the maximum social spending threshold.

Syntax: 
```
max_social_spending = n
```
```
where n = 0.1 increases the maximum social spending threshold by 10%
```
Note: The max social spending you can limit a nation to is 1% (max_social_spending = 0.99). At 100% (max_social_spending = 1) this modifier doesn't work.

#### max_tariff

Change in the maximum permissible tariff.

Syntax: 
```
max_tariff = n
```
```
where n = 0.1 increases the maximum tariff threshold by 10%. 
```

#### max_tax

Change in themaximum permissible tax.

Syntax: 
```
max_tax = n
```
```
where n = 0.1 increases the maximum tax threshold by 10%
```

#### min_military_spending

Change in the minimum military spending threshold.

Syntax: 
```
min_military_spending = n
```
```
where n = 0.1 increases the minimum military spending threshold by 10%
```

#### min_social_spending

Change in the minimum social spending threshold.

Syntax: 
```
min_social_spending = n
```
```
where n = 0.1 increases the minimum social spending threshold by 10%
```

#### min_tariff

Change in the minimum permissible tariff.

Syntax: 
```
min_tariff = n
```
```
where n = 0.1 increases the minimum tariff threshold by a flat 10%.<br/>
```
Example: 
```
min_tariff = 0.25
```
```
will yield a minimum tariff rate of 25% if the base value was 0%.
```

#### min_tax

Change in themaximum permissible tax.

Syntax: 
```
min_tax = n
```
```
where n = 0.1 increases the min tax threshold by 10%
```
Example: 
```
min_tax = 0.25
```
```
will yield a minimum tax rate of 25% if the base value was 0%.
```

#### mobilisation_economy_impact

Increase/decrease in the economic impact of a country mobilizing its population.

Syntax: 
```
mobilisation_economy_impact = n
```
```
where n = -0.25 would indicate a reduction of this impact by 25%.
```

#### mobilization_impact

Increase/decrease of a country's mobilization impact, affecting how much a country can mobilize if it has a small military compared to its mobilizable population.

Syntax: 
```
mobilization_impact = n
```
```
where n = -0.25 would indicate a 25% reduction in this value.
```

#### mobilisation_size

Increase/decrease in the percentage amount of lower-class accepted POPs a country can mobilize.

Syntax: 
```
mobilisation_size = n
```
```
where n = 0.05 increases this percentage by 5.
```

#### naval_organisation

Percentage increase in the organization levels for a country's ships.

Syntax: 
```
naval_organisation = n
```
```
where n = 0.1 would be a 10% increase to organization.
```

#### naval_unit_start_experience

Percentage increase in the starting experience of new ships.

Syntax: 
```
naval_unit_start_experience = n
```
```
where n = 15 would start new ships with 15% (out of 100%) experience, <i>ceteris paribus</i>.
```

#### non_accepted_pop_consciousness_modifier

Monthly change in consciousness (CON) for all POPs of non-accepted cultures.

Syntax: 
```
non_accepted_pop_consciousness_modifier = n
```
```
where n = 2 would add 2 CON/month to POPs of non-accepted cultures.
```

#### non_accepted_pop_militancy_modifier

Monthly change in militancy (MIL) for all POPs of non-accepted cultures.

Syntax: 
```
non_accepted_pop_militancy_modifier = n
```
```
where n = 2 would add 2 MIL/month to POPs of non-accepted cultures.
```

#### org_regain

Percentage change of the rate of organization regeneration for a country's units.

Syntax: 
```
org_regain = n
```
```
where n = 0.1 is an increase of 10% organization/month.
```

#### political_reform_desire

Percentage change in the desire of all pops within the country for political reforms.

Syntax: 
```
political_reform_desire = n
```
```
where n = 0.1 is an increase of 10%.
```

#### prestige

Flat change in prestige per month

Syntax: 
```
prestige = n
```
```
where n = 0.02 yields +0.02 prestige/month.
```

#### research_points

Flat change in research points per day.

Syntax: 
```
research_points = n
```
```
where n = 0.01 is +0.01 research points per day.
```

#### research_points_modifier

Percentage change in the rate of research points (RP) generation. Applied <i>after</i> any research_points base modifier.

Syntax: 
```
research_points_modifier = n
```
```
where n = -0.5 would halve research point gain from any source, <i>ceteris paribus</i>.
```

#### research_points_on_conquer

Nominal modifier on the number of research points an uncivilized nation gains when they conquer lands.

Syntax: 
```
research_points_on_conquer = n
```
```
where n = 0.25 is intended to increase the number of research points gained via conquest by +25%.
```

In actuality, this modifier is broken, and functions as an on/off switch for whether a country will gain research points through conquest depending on whether or not the value is above 0.

#### rgo_output

Percentage change in the output of all the country's RGO's. Note the modifier name is case-insensitive (RGO_output and rgo_output both work).

Syntax: 
```
RGO_output = n
```
```
where n = 0.1 would be a 10% increase in output.
```

#### rgo_throughput

Percentage change in the throughput of all of a country's RGO's. Note the modifier name is case-insensitive (RGO_throughput and rgo_throughput both work).

Syntax: 
```
RGO_throughput = n
```
```
where n = 0.1 would be a 10% increase in throughput.
```

#### ruling_party_support

Percentage change in voter support for the current ruling party throughout the country.

Syntax: 
```
ruling_party_support = n
```
```
where n = 0.1 would be a 10% increase in voter support.
```

#### social_reform_desire

Percentage change in the desire of all pops within the country for social reforms.

Syntax: 
```
social_reform_desire = n
```
```
where n = 0.1 is an increase of 10%.
```

#### suppression_points_modifier

Percentage change in the gain of suppression points.

Syntax: 
```
suppression_points_modifier = n
```
```
where n = 0.1 is an increase of 10%.
```

#### supply_consumption

Percentage increase/decrease in the amount of resources needed to supply units.

Syntax: 
```
supply_consumption = n
```
```
where n = 0.1 would be an increase of 10%.
```

#### (strata)_vote

Percentage increase or decrease in the weighting of the strata's vote.

Syntax: 
```
poor_vote = 0.1
```
```
is a 10% increase in the weight of all poor pops' votes.
```

#### tax_efficiency

Percentage change in the efficiency of tax collection for the entire country

Syntax: 
```
tax_efficiency = n 
```
```
where n = 0.1 is an increase of 10%.
```

#### (category)_tech_research_bonus

Percentage cost change of the category's technologies.

Syntax: 
```
industry_tech_research_bonus = n
```
```
where n = 0.1 decreases the cost of industry technologies by 10%
```

#### unit_start_experience

Fixed percentage point change in the starting experience of all new units.

Syntax: 
```
unit_start_experience = n
```
```
where n = 15 would start new land units with 15% (out of 100%) experience, <i>ceteris paribus</i>.
```

#### war_exhaustion

Monthly change in a country's war exhaustion.

Syntax: 
```
war_exhaustion = n
```
```
where n = 1 would add 1 WE each month.
```

### Province Modifiers

#### assimilation_rate

Percentage change in the assimiliation rate of foreign culture pops in a province.

Syntax: 
```
assimilation_rate = n
```
```
where n = 0.1 would be a 10% increase.
```

#### immigrant_attract

Increases or decreases the attractiveness of a province to prospective immigrants.

Syntax: 
```
immigrant_attract = n
```
```
where n = 1 would be a 100% increase.
```

#### immigrant_push

Increases or decreases the amount emigrating from the province in scope.

Syntax: 
```
immigrant_push = n
```
```
where n = 1 would be a 100% increase. 
```

NB: While this does not increase the emigration rate, it does increase the emigration amount. Every month, the emigration chance tick hits, and if it hits a threshold (threshold percentage factors are in ..\common\pop_types.txt), this modifier will increase the amount that would emigrate from a certain pop. For example, if there is a non-accepted pop at 7 militancy and in a province that is not their core, they will most certainly hit the emigration threshold. Normally, only a few thousand at most per month would leave, however, if immigrant_push was set to, say, 100, it would increase the amount emigrating by a factor of 10,000. This would increase the emigration amount from the usual thousand or so, into the hundreds of thousands.

#### life_rating

Percentage change in the life rating of a province.

Syntax: 
```
life_rating = n
```
```
where n = 1 would be an increase of 100%.
```

#### local_artisan_output

Percentage change in the output of a province's artisans.

Syntax: 
```
local_artisan_output = n
```
```
where n = 0.1 would be a 10% increase in output.
```

#### local_factory_input

Percentage change of the input of factories in the province's state.

Syntax: 
```
local_factory_input = n
```
```
where n = 0.1 would be a (10% / number of provinces in the state) increase in input.
```

#### local_factory_output

Percentage change of the output of factories in the province's state.

Syntax: 
```
local_factory_output = n
```
```
where n = 0.1 would be a (10% / number of provinces in the state) increase in output.
```

#### local_factory_throughput

Percentage change of the throughput of factories in the province's state.

Syntax: 
```
local_factory_throughput = n
```
```
where n = 0.1 would be a (10% / number of provinces in the state) increase in throughput.
```

#### local_repair

Percentage change of the repair rate for ships in a province.

Syntax: 
```
local_repair = n
```
```
where n = 0.1 is an increase of 10% additional strength repaired per month.
```

#### local_RGO_output

Percentage change in the output of a province's RGO.

Syntax: 
```
local_RGO_output = n
```
```
where n = 0.1 would be a 10% increase in output.
```

#### local_RGO_throughput

Percentage change in the throughput of a province's RGO.

Syntax: 
```
local_RGO_throughput = n
```
```
where n = 0.1 would be a 10% increase in throughput.
```

#### local_ruling_party_support

Percentage change in voter support for the current ruling party in the province.

Syntax: 
```
local_ruling_party_support = n
```
```
where n = 0.1 would be a 10% increase in voter support.
```

#### local_ship_build

Percentage change of the time to build naval units in this province.

Syntax: 
```
local_ship_build = n
```
```
where n = 0.1 is a 10% increase.
```

#### pop_(trait)_modifier

Monthly increase or decrease in (trait; either consciousness or militancy) for all pops in a province.

Syntax: 
```
pop_consciousness_modifier = n 
```
```
where n = 1 would add 1 CON each month.
```

#### population_growth

Percentage increase or decrease in the natural growth of pops in a province.

Syntax: 
```
population_growth = n
```
```
where n = 0.1 would be a 10% increase in the growth rate.
```

#### (type)_rgo_eff

Percentage change in the efficiency of a province's RGO. The (type) can be farm or mine.

Syntax: 
```
farm_rgo_eff = n
```
```
where n = 0.1 would be a 10% increase in efficiency.
```

#### (type)_rgo_size

Percentage change in the size of a province's RGO. The (type) can be farm or mine.

Syntax: 
```
farm_rgo_size = n
```
```
where n = 0.1 would be a 10% increase in RGO size.
```

### Country & Province Modifiers

#### goods_demand

	 
Percentage increase or decrease in the demand for all goods of pops in the country or province specified.
	 
Syntax: 
```
goods_demand = n
```
```
where n = 0.1 would be a 10% increase in the demand.
```

#### (strata)_income_modifier

Percentage increase or decrease in the income of pops in the specified strata. 
This modifier appears not to be working, if you did manage to get the effect working, remove this text.

Syntax: 
```
 rich_income_modifier = n
```
, n = 0.1 is a 10% increase in income.

#### (strata)_(level)_needs

Strata can be poor, middle, or rich; level can be life, everyday, or luxury. After checks on the HoD v3.04 it appears that this modifier works for the social reforms listed in issues.txt but has no effect* when used in event_modifiers.txt.

- in event_modifiers.txt effects for middle strata and rich strata are swapped.

Syntax: 
```
 poor_life_needs = n
```
, -1 < n < 1. Not sure what the specific effect of the value of n is, might be percentage increase ex. n = 0.1 means that strata's life needs increase by 10%.

### Modifier Icons

In the event_modifiers.txt file, you'll see that every modifier has an icon it displays—for country modifiers, this is the icon that appears in the diplomacy screen (the one over which you hover to get the description and modifiers text). For province modifiers, this is the icon that appears in the province detail screen. The number of the icon corresponds to the "placement" of the modifier in the modifiers.dds file (in the gfx\interface folder). So you could, conceivably, go to that file and count along the strip to see the number of the icon you want.

The thing to note, however, is that province modifiers and country modifiers actually work a bit differently. The country modifiers "skip" the first two icons on the strip (the gavels—you can't get either to appear as country modifier icons) and "icon = 1" for a country modifier is actually the green pie chart icon (and thus you can only go up to 18 rather than 20). The picture below displays this (using the icons form vanilla), with the first row being province modifiers and the second row being country modifiers:

### See also

- [Modding overview](folder-file-overview.md)
- [Advanced events](event-modding.md)
- [Full list of commands](list-of-conditions.md)
- Full list of effects
- Full list of scopes
