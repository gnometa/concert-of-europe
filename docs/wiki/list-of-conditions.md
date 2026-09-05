# List of conditions

Source: https://vic2.paradoxwikis.com/List_of_conditions

This is a **full list of conditions** usable in event and decision scripting. 

Conditions are pieces of script that ask simple logical questions, and return a yes/no answer. These are used in various situations, usually to determine whether or not the prerequisites are met for a certain action to occur. 

For example:

```
trigger = {
	is_greater_power = yes
}
```
 
This example displays a trigger for an event. Events can fire only when their trigger requirements are met. This hypothetical event has a very simple trigger, it asks only one thing: is the country in question a great power? If it returns true (i.e. the country is in fact a great power) then they trigger is satisfied and the event may fire. Using Boolean commands and some clever scripting, commands can be used to create very complex sets of requirements. They are used in several different parts of event and decision scripting.

Commands are used for: 
- The "potential" and "allow" sections of decision scripting to determine when they may be presented to the player as an option
- The "trigger" and "MTTH" (Mean Time to Happen) sections of event scripting to determine when they are eligible to fire and the chances of this happening
- The "limit" section of effect (within either events or decisions) scripting to determine what the limits of an effect's reach are

Not all commands are useful in all situations. Commands are usually relevant to specific situations.

For example, the command:

```
religion = protestant
```

This command is applicable only when a pop is in question, and it therefore non-functional when applied to province, state, national level scripts. Keep the limits of commands in mind when scripting.

The list below is a comprehensive collection of these commands. Enjoy, and get to modding!

### Boolean Operators

These are boolean operators. There are only three of them in Victoria 2, but they are extremely useful. Like any command, they can return true or false, but they are special in that they consist entirely of *other* commands. This makes them highly versatile. Expect to use these more than any other commands.

#### AND

This operator returns true only when every included statement returns true.

```
AND = {
	ai = no
	civilized = yes
}
```

This "and" operator will return true only if the country in question is not controlled by the ai (that is, it is player controlled), and it is civilized. 

#### OR

This operator returns true when any of the included commands returns true.

```
OR = {
	government = democracy
	prestige = 50
}
```

This "or" operator will return true if the country in question is either a democracy or has 50 (or more) prestige.

#### NOT

This command is a little more tricky. It will return true if the included variable is false.

```
NOT = {
	slavery = yes
}
```

This "not" operator will return true if the country in question does not allow slavery. This may seem useless, because the scripter could simply use "slavery = no" to achieve the same thing. However, not all commands are so cut and dry as the "slavery" command. Consider the following:

```
NOT = { 
	num_of_allies = 3
}
```

This "not" operator will be satisfied only if the country does not have 3 or more allies; or, in more plain terms, if the country has 2 allies or less. Thus we can see that the "not" command is very useful in combination with any numerically-based command.

NOTE: If you include multiple statements within the same NOT operator, it returns true if ALL of the statements evaluate to false, and it returns false if just ONE or more statements evaluates to true. It is essentially the same as an AND operator, only the logic works with false statements instead of true statements.

### Broad Commands

#### year

Syntax:	

```
year = x
```

Use:  

Returns true if x is the current year or a later year.

Range:  

This command is usable in any circumstance.

#### month

Syntax:	

```
month = x
```

Use:  

Returns true if x is the current month or an earlier month.

Range:  

This command is usable in any circumstance.

#### allow_multiple_instances

Syntax:

```
allow_multiple_instances = [yes/no]
```

Use:  

This will allow multiple instances of the same event to fire to one country.

Range:  

Usable for event triggers only.

#### fire_only_once

Syntax:

```
fire_only_once = [yes/no]
```

Use:  

The event will fire only once in a game. Normal events will fire whenever their conditions are met, this event will only fire once under any circumstance.

Range:  

Usable for event triggers only.

#### is_triggered_only

Syntax:

```
is_triggered_only = [yes/no]
```

Use:  

This prevents the event from being put into the event stack in the code and makes it so it may only be triggered by another trigger, decision, or through the game's programming.  
(NB: This also means you shouldn't include a trigger = { ... } parameter to your event, as it will be ignored. The only exception is with events triggered by the game's native-code, such as on-action election events.)

Range:  

Usable for event triggers only.

#### major

Syntax:

```
major = yes
```

Use:  

The event appears with a special window (with the country's flags by the title bar, and without a picture). This also means the event appears on the notifications, similar to how decisions do, with the prefix "Major Event".

Range:  

Usable for events only.

#### immediate

Syntax:	

```
immediate = { (effects) }
```

Use:  

Before the option section, it makes the specified effects in its section happen the moment the event is fired and independent of any option.

Range:  

Usable for events only.

#### check_variable

Syntax:	

```
check_variable = {
which = [name of variable]
value = x
}
```

Use:  

Returns true if the “variable name” has been set at an earlier stage and its value is greater than or equal to x. Note: Doesn't seem to work within the province scope.

#### has_global_flag

Syntax:

```
has_global_flag = [name of flag]
```

Use:  

Returns true if the game has the specified global flag defined.

#### is_canal_enabled

Syntax:

```
is_canal_enabled = [1,2,3]
```

Use:  

Returns true if the specified canal has been constructed. 1 = Kiel Canal, 2 = Suez Canal, 3 = Panama Canal.

### Country Scope

These commands are useful at the country scope. They are applicable whenever the script is referring to a country.

#### administration_spending

Syntax:	

```
administration_spending = x
```

Use:  

Returns true if the current country invest x% or more in administration. 

#### ai

Syntax:	

```
ai = [yes / no]
```

Use:  

Determines if the country in question is computer or human/player-controlled.

#### alliance_with

Syntax:	

```
alliance_with = [tag/THIS/FROM]
```

Use:  

Returns true if the country is allied with the specified country.

#### average_consciousness

Syntax:	

```
average_consciousness = X
```

Use:  

Returns true if the country overall has a consciousness average at or above X.

#### average_militancy

Syntax:	

```
average_militancy = X
```

Use:  

Returns true if the country overall has a militancy average at or above X.

#### badboy

Syntax:

```
badboy = X
```

Use:  

Returns true if the country has an infamy of X.
NOTE: Unlike with the effect, X in this case is not a straight integer. It's a percentage of 25 (the "infamy limit"). So 20 infamy is 0.8, and 50 infamy is 2.0.

#### big_producer (needs clarification)

Syntax:

```
big_producer = [name of trade good]
```

Use:  

Returns true if the country is a big producer of the specified trade good (may mean this good is in the top 3 exported for the nation or may mean the nation is a top exporter of this good vs all other nations).

#### blockade

Syntax:	

```
blockade = x
```

Use:  

Returns true if the blockade percentage is equal to x or more.

#### brigades_compare

Syntax:

```
brigades_compare = X
```

Use:  

Returns true if the current country has X or more in multiples of army brigades than the country in scope.
Example: "brigades_compare = 2" inside an "any_country" scope, would return true for any country that had double the brigades or more than the current country

#### can_build_factory_in_capital_state

Syntax:

```
can_build_factory_in_capital_state = [name of factory]
```

Use:  
 
Returns true if the capital state can build the specified factory. Real factory names can be found in common/buildings.txt (example: can_build_factory_in_capital_state = artillery_factory)

#### crime_higher_than_education

Syntax:

```
crime_higher_than_education = [yes/no]
```

Use:  

Returns true if the administration spending slider is higher than the education spending slider.

#### can_nationalize

Syntax:	

```
can_nationalize = [yes/no]
```

Use:  

Returns true if the current country can nationalize their industry.

#### can_create_vassals

Syntax:	

```
can_create_vassals = [yes/no]
```

Use:  

Returns true if the current country can create a puppet state.

#### capital

Syntax:	

```
capital = [province id]
```

Use:  

Returns true if the specified capital is the current country’s capital.

#### casus_belli

Syntax:

```
casus_belli = [tag/THIS/FROM]
```

Use:  

Returns true if the country in scope has any active casus belli against the target.

#### citizenship_policy

Syntax:	

```
citizenship_policy = [policy]
```

Use:  

Returns true if the country has the specified citizenship policy (from common\issues.txt) (example: "citizenship_policy = residency")

#### civilization_progress

Syntax:

```
civilization_progress = X
```

Use:  

Returns true if the uncivilized country has progressed to X% of civilization reforms, with X being expressed as a decimal (between 0 and 1).
NOTE: While this command displays on tooltips, the value of it does not. Be wary of using this in "allow" fields of decisions.

#### civilized

Syntax:	

```
civilized = [yes/no]
```

Use:  

Returns true if the current country is civilized.

#### colonial_nation

Syntax:	

```
colonial_nation = [yes/no]
```

Use:  

Returns true if the current country has colonies anywhere in the world.

#### constructing_cb_progress

Syntax:

```
constructing_cb_progress = X
```

Use:  

Returns true if the country CB construction has progressed to X% or more, with X being expressed as a decimal (between 0 and 1).

#### constructing_cb_type

Syntax:

```
constructing_cb_type = (name of CB)
```

Use:  

Returns true if the country is constructing the specified CB.

#### controls

Syntax:	

```
controls = [province id]
```

Use:  

Returns true if the current country controls the specified province.

#### crime_fighting

Syntax:	

```
crime_fighting = x
```

Use:  

Returns true if the current country invest x% or more in crime fighting.

#### crisis_exist *HOD ONLY*

Syntax:	

```
crisis_exist = [yes/no]
```

Use:  

Returns true if there is an active crisis somewhere in the world.

#### culture_has_union_tag

Syntax:	

```
culture_has_union_tag = [yes/no]
```

Use:  

Returns true if the scoped country's primary culture group has a defined cultural union tag/country.

#### diplomatic_influence

Syntax:	

```
diplomatic_influence = {
	who = [THIS/FROM/TAG]
	value = x
}
```

Use:  

Returns true if country has more than x diplomatic influence in the country in scope.

#### economic_policy

Syntax:	

```
economic_policy = [policy]
```

Use:  

Returns true if the country has the specified economic policy (from common\issues.txt) (example: "economic_policy = laissez_faire")

#### economic_reform

Syntax:	

```
economic_reform_name = level
See common/issues.txt for list of uncivilized economic reforms and their levels
Example : land_reform = yes_land_reform means the uncivilized country has researched the Land Reform reform
```

Use:  

Returns true if the country has a specific economic reform at a specific level

#### education_spending

Syntax:	

```
education_spending = x
```

Use:  

Returns true if the current country invest x% or more in education.

#### election

Syntax:	

```
election = [yes/no]
```

Use:  

Returns true if there is an ongoing election in the country.

#### exists

Syntax:	

```
exists = [tag]
```

Use:  

Returns true if the specified country exists. May also be used with [yes/no] to determine if the country in scope actually exists.

#### government

Syntax:	

```
government = [government type]
```

Use:  

Returns true if the country has the specified government type.

#### great_wars_enabled

Syntax:	

```
great_wars_enabled = [yes/no]
```

Use:  

Returns true if great wars are enabled.

#### have_core_in

Syntax:	

```
have_core_in = [country tag]
```

Use:  

Returns true if the country in scope has cores on any provinces of the specified nation.

#### has_country_flag

Syntax:	

```
has_country_flag = [name of flag]
```

Use:  

Returns true if the country in scope has the specified country flag.

#### has_country_modifier

Syntax:	

```
has_country_modifier = [name of modifer]
```

Use:  

Returns true if the current country has the specified modifier.

#### has_cultural_sphere *HOD ONLY*

Syntax:	

```
has_cultural_sphere = [yes/no]
```

Use:  

Returns true if the country in scope has any nations of our culture in their SOI.

#### has_leader

Syntax:	

```
has_leader = [name of leader]
```

Use:  

Returns true if the specified leader belongs to the current country.

#### has_recently_lost_war

Syntax:	

```
has_recently_lost_war = [yes/no]
```

Use:  

Returns true if the country in scope has recently lost a war within 5 years.

#### has_unclaimed_cores

Syntax:	

```
has_unclaimed_cores = [yes/no]
```

Use:  

Returns true if the country in scope has cores that are not owned by them.

#### [ideology]

Syntax:

```
[ideology] = x
```

Use:  

Returns true if at least x% of the country’s population follows the specified ideology.  

E.g. liberal = 10 will return true if *population*, NOT voter, support for liberal ideology is at least 10%. This is the same information as that displayed on the pop ideology pie charts in the politics and population screens.

#### ideology

Syntax:	

```
ideology = [ideology type]
```

Use:  

Returns true if the country’s ruling party belongs to the specified ideology.

#### industrial_score

Syntax:	

```
industrial_score = x
```

Use:  

Returns true if the country’s industrial score is equal to x or higher.

#### in_sphere

Syntax:

```
in_sphere = [tag/FROM/THIS]
```

Use:  

Returns true if the country in scope is in the sphere of the target.

#### in_default

Syntax:	

```
in_default = [yes/no]
```

Use:  

Returns true if the country in scope has defaulted on debts.

#### invention

Syntax:	

```
invention = [name of invention]
```

Use:  

Returns true if the country knows the specified invention.

#### involved_in_crisis *HOD ONLY*

Syntax:	

```
involved_in_crisis = [yes/no]
```

Use:  

Returns true if the country in scope is participating in the current crisis (being "on-the-fence" counts).

#### is_claim_crisis *HOD ONLY*

Syntax:	

```
is_claim_crisis = [yes/no]
```

Use:  

Returns true if the current crisis is over claims on territory.

#### is_colonial_crisis

Syntax:	

```
is_colonial_crisis = [yes/no]
```

Use:  

Returns true if the current crisis is over uncolonized land. 

#### is_core

Syntax:	

```
is_core = [province id]
```

Use:  

Returns true if the specified province is a core of the current country.

#### is_cultural_union

Syntax:	

```
is_cultural_union = [tag/FROM/THIS]
```

Or

```
is_cultural_union = [yes/no]
```

Use:  

Returns true if the country in scope is a cultural union country, like Germany, Romania and Italy.

#### is_culture_group

Syntax:	

```
is_culture_group = [culture/tag/FROM/THIS]
```

Use:  

Returns true if the country in scope has a primary culture of the specified culture group, or if a country is provided, equal to the culture group of the primary culture of that country.

#### is_disarmed

Syntax:

```
is_disarmed = [yes/no]
```

Use:  

Returns true if the current country has been disarmed (via the Cut Down to Size casus belli).

#### is_greater_power

Syntax:	

```
is_greater_power = [yes/no]
```

Use:  

Returns true if the current country is a greater power.

#### is_ideology_enabled

Syntax:	

```
is_ideology_enabled = ideology
Example : is_ideology_enabled = socialism means socialism is active in the country
```

Use:  

Returns true if the ideology is active in the nation

#### is_independant

Syntax:	

```
is_independant = [yes/no]
```

Use:  

Determines whether the country is puppet or not. Difference to is_vassal is unknown. Independent is supposed to be spelled wrong: independent

#### is_liberation_crisis *HOD ONLY*

Syntax:	

```
is_liberation_crisis = [yes/no]
```

Use:  

Returns true if the current crisis a liberation crisis to liberate an entire nation.

#### is_mobilised

Syntax:

```
is_mobilised = [yes/no]
```

Use:  

Determines whether the country has mobilised or not.

#### is_next_reform

Syntax:	

```
is_next_reform = [reform type]
```

Use:  

Returns true if the next reform is the specified reform (if healthcare is no healthcare, then the next reform would be trinket healthcare).

#### is_our_vassal

Syntax:

```
is_our_vassal = [tag/THIS/FROM]
```

Use:  

Returns true if the specified country is a vassal of the country in scope.

#### is_possible_vassal

Syntax:	

```
is_possible_vassal = (tag)
```

Use:  

Returns true if the specified country can be released as a puppet state (meaning do they own the target's capital?).

#### is_secondary_power

Syntax:	

```
is_secondary_power = [yes/no]
```

Use:  

Returns true if the current country is a secondary power.

#### is_sphere_leader_of

Syntax:

```
is_sphere_leader_of = [tag/FROM/THIS]
```

Returns true if the country in scope is the sphere owner of the target.

#### is_vassal

Syntax:	

```
is_vassal = [yes/no]
```

Use:  

Returns true if the current country is a puppet.

#### is_substate

Syntax:	

```
is_substate = [yes/no]
```

Use:  

Returns true if the current country is a substate.

#### literacy

Syntax:	

```
literacy = x
```

Use:  

Returns true if the average literacy of the country is greater than or equal to the specified amount.

#### lost_national

Syntax:	

```
lost_national = x
```

Use:  

Returns true if the number of core provinces that a country has lost is equal to x or more.

#### middle_strata_everyday_needs

Syntax:

```
middle_strata_everyday_needs = X
```

Use:  

Returns true if the country's middle strata are getting X% of their everyday needs, with X being a value between 0 and 1.

#### middle_strata_life_needs

Syntax:

```
middle_strata_life_needs = X
```

Use:  

Returns true if the country's middle strata are getting X% of their life needs, with X being a value between 0 and 1.

#### middle_strata_luxury_needs

Syntax:

```
middle_strata_luxury_needs = X
```

Use:  

Returns true if the country's middle strata are getting X% of their luxury needs, with X being a value between 0 and 1.

#### middle_tax

Syntax:	

```
middle_tax = x
```

Use:  

Returns true if percentage of tax paid by the middle strata is equal to x% or more.

#### military_access

Syntax:	

```
military_access = [tag/THIS/FROM]
```

Use:  

Returns true if the target country has military access to the scoped country.

#### military_reform

Syntax:	

```
military_reform_name = level
See common/issues.txt for list of uncivilized military reforms and their levels
Example : foreign_training = yes_foreign_training means the uncivilized country has researched the Foreign Training reform
```

Use:  

Returns true if the country has a specific military reform at a specific level

#### military_score

Syntax:	

```
military_score = x
```

OR

```
military_score = [tag/THIS/FROM]
```

Use:  

Returns true if the country’s military score is equal to x or higher.

#### military_spending

Syntax:	

```
military_spending = x
```

Use:  

Returns true if the current country invest x% or more in the military.

#### money

Syntax:	

```
money = x
```

Use:  

Returns true if the amount of money a country has in their treasury is equal to x or more.

#### nationalvalue

Syntax:	

```
nationalvalue = [national value]
```

Use:  

Returns true if the current country’s national value is equal to the national value specified (using the value in the nationalvalues.txt file... so Liberty would be "nv_liberty".

#### national_provinces_occupied

Syntax:	

```
national_provinces_occupied = x
```

Use:  

Returns true if a foreign power occupies x% or more of the current country’s provinces.

#### neighbour

Syntax:	

```
neighbour = [tag/FROM/THIS]
```

Use:  

Returns true if the current country is a neighbour to the specified country.

#### num_of_allies

Syntax:	

```
num_of_allies = x
```

Use:  

Returns true if the country has x or more allies.

#### num_of_cities

Syntax:	

```
num_of_cities = x
```

Use:  

Returns true if the country has x or more cities (aka provinces – inherited from EU3).

#### num_of_ports

Syntax:	

```
num_of_ports = x
```

Use:  

Returns true if the country has x or more ports.

#### num_of_revolts

Syntax:	

```
num_of_revolts = x
```

Use:  

Returns true if there are x or more revolts in the country (x being the number of states under rebel control).

#### number_of_states

Syntax:	

```
number_of_states = x
```

Use:  

Returns true if the number of states a country has is equal to x or more.

#### num_of_substates

Syntax:	

```
num_of_substates = x
```

Use:  

Returns true if the number of substates a country has is equal to x or more.

#### num_of_vassals

Syntax:	

```
num_of_vassals = x
```

Use:  

Returns true if the number of puppets a country has is equal to x or more.

#### num_of_vassals_no_substates

Syntax:	

```
num_of_vassals_no_substates = x
```

Use:  

Returns true if the number of puppets that are not substates a country has is equal to x or more.

#### owns

Syntax:	

```
owns = [province id]
```

Use:  

Returns true if the country owns the specified province.

#### part_of_sphere

Syntax:

```
part_of_sphere = [yes/no]
```

Use:  

Determines whether the country in scope is part of ANY great power's sphere.

#### [party_issue]

Syntax:

```
[party_issue] = x
```

Use:  

Returns true if total population support for the party issue is at least x%.   

(E.g. moralism = 10 will return true if *population*, NOT voter, support for moralism is at least 10%).

#### political_movement_strength

Syntax:	

```
political_movement_strength = x
```

Use:  

Checks if there is any political movement with x or more support.
The support is calculated by dividing the supporters by the total amount of POPs and then multiplying by MOVEMENT_SUPPRT_UH_FACTOR in defines.lua (default is 3).
So for a country with 150000 POPs and a political movement with 5000 supporters, the political_movement_strength would be 3 * 5000 / 150000 = 10% (0.10).

#### political_reform

Syntax:	

```
political_reform_name = level
See common/issues.txt for list of social reforms and their levels
Example : vote_franchise = wealth_weighted_voting means the country currently has its voting rights set at weighted wealth voting
```

Use:  

Returns true if the country has a specific political reform at a specific level

#### political_reform_want

Syntax:	

```
political_reform_want = 0.xx
```

Use:  

Returns true if x% or more of the population wants a social reform, x being a value between 0.00 and 1.00

#### poor_strata_everyday_needs

Syntax:

```
poor_strata_everyday_needs = X
```

Use:  

Returns true if the country's poor strata are getting X% of their everyday needs, with X being a value between 0 and 1.

#### poor_strata_life_needs

Syntax:

```
poor_strata_life_needs = X
```

Use:  

Returns true if the country's poor strata are getting X% of their life needs, with X being a value between 0 and 1.

#### poor_strata_luxury_needs

Syntax:

```
poor_strata_luxury_needs = X
```

Use:  

Returns true if the country's poor strata are getting X% of their luxury needs, with X being a value between 0 and 1.

#### poor_tax

Syntax:	

```
poor_tax = x
```

Use:  

Returns true if percentage of tax paid by the poor strata is equal to x% or more.

#### pop_majority_culture

Syntax:	

```
pop_majority_culture = (culture)
```

Use:  

Returns true if the majority of a nation's population is of the specified culture.

#### pop_majority_ideology

Syntax:	

```
pop_majority_ideology = (ideology)
```

Use:  

Returns true if the majority of a nation's population has the specified ideology.

#### pop_majority_religion

Syntax:	

```
pop_majority_religion = (religion)
```

Use:  

Returns true if the majority of a nation's population has the specified religion.

#### pop_militancy

Syntax:	

```
pop_militancy = x
```

Use:  

Returns true if any pop in the province has a militancy value equal to x or higher.

#### [poptype]

Syntax:

```
[poptype] = x
```

Use:
Returns true if the specified poptype has x% of the total population in the country (x expressed as a value between 0 and 1).
Example: "soldiers = 0.05" would return true if soldiers made up 5% or more of the country's population.

#### prestige

Syntax:	

```
prestige = x
```

Use:  

Returns true if the country has a prestige value equal to x or higher.

#### primary_culture

Syntax:	

```
primary_culture = [culture]
```

Use:  

Returns true if the country has the specified culture as its primary culture.

#### accepted_culture

Syntax:	

```
accepted_culture = [culture]
```

Use:  

Returns true if the country has the specified culture as its accepted culture.

#### plurality

Syntax:	

```
plurality = x
```

Use:  

Returns true if the country has plurality value equal to x or higher.

#### produces

Syntax:	

```
produces = nameofgood
```

Use:  

Returns true if the country produces the specified industrial or RGO good

#### rank

Syntax:

```
rank = x
```

Use:  

Returns true if the country's rank is equal to x or greater

#### rebel_power_fraction

Syntax:	

```
rebel_power_fraction = x
```

Use:  

Returns true if any rebel has a power (muscle flexing icon, not revolt risk, which has the rebel flag) of at least x%. Would not recommend going too high as pops tend to rebel before their power gets high (revolt risk tends to climb faster than power).

#### recruited_percentage

Syntax:	

```
recruited_percentage = x
```

Use:  

Returns true if the percentage of recruited regiments is at least x%.

#### relation

Syntax:	

```
relation = { who = [tag/this/from] value = x }
```

Use:  

Returns true if the specified country has a relation value equal to x or higher with the specified country.

#### religious_policy

Syntax:	

```
religious_policy = [policy]
```

Use:  

Returns true if the country has the specified religious policy (from common\issues.txt) (example: "religious_policy = moralism")

#### revolt_percentage

Syntax:	

```
revolt_percentage = x
```

Use:  

Returns true if the percentage of revolts in the country is equal to x or higher.

#### rich_strata_everyday_needs

Syntax:

```
rich_strata_everyday_needs = X
```

Use:  

Returns true if the country's rich strata are getting X% of their everyday needs, with X being a value between 0 and 1.

#### rich_strata_life_needs

Syntax:

```
rich_strata_life_needs = X
```

Use:  

Returns true if the country's rich strata are getting X% of their life needs, with X being a value between 0 and 1.

#### rich_strata_luxury_needs

Syntax:

```
rich_strata_luxury_needs = X
```

Use:  

Returns true if the country's rich strata are getting X% of their luxury needs, with X being a value between 0 and 1.

#### rich_tax

Syntax:	

```
rich_tax = x
```

Use:  

Returns true if percentage of tax paid by the rich strata is equal to x% or more.

#### rich_tax_above_poor

Syntax:	

```
rich_tax_above_poor = [yes/no]
```

Use:  

Returns true if percentage of tax paid by the rich strata is greater than the percentage of tax paid by the poor strata.

#### ruling_party

Syntax:	

```
ruling_party = [tag]
```

Use:  

Returns true if the ruling party is equal to tag.

#### ruling_party_ideology

Syntax:	

```
ruling_party_ideology = [ideology]
```

Use:  

Returns true if the ruling party of the current country belongs to the specified ideology.
This is not a valid condition for ideologies.txt.

#### slavery

Syntax:	

```
slavery = yes_slavery/no_slavery
```

Use:  

Returns true if the current country allows slavery or not.

#### social_movement_strength

Syntax:	

```
social_movement_strength= 0.xx
```

Use:  

See [political_movement_strength](list-of-conditions.md)

#### social_reform

Syntax:	

```
social_reform_name = level
See common/issues.txt for list of social reforms and their levels
Example : wage_reform = trinket_wage means the country currently has its wage level set at trikets
```

Use:  

Returns true if the country has a specific social reform at a specific level

#### social_reform_want

Syntax:	

```
social_reform_want = 0.xx
```

Use:  

Returns true if x% or more of the population wants a social reform, x being a value between 0.00 and 1.00

#### social_spending

Syntax:	

```
social_spending = x
```

Use:  

Returns true if the current country is investing x% or more in social issues.

#### stronger_army_than

Syntax:	

```
stronger_army_than = [tag/this/from]
```

Use:  

Returns true if the current country has a stronger army than the specified country.

#### substate_of

Syntax:	

```
substate_of = [tag/this/from]
```

Use:  

Returns true if the current country is a substate of the specified country.

#### tag

Syntax:	

```
tag = [country tag]
```

Use:  

Returns true if the current country has a country tag that matches the specified tag.

#### [technology]

Syntax:	

```
[technology name] = 1
```

Use:  

Is a boolean that returns true if the country has researched the specified technology (example: "state_n_government = 1")

#### this_culture_union *HOD ONLY*

Syntax:	

```
this_culture_union = [country tag] / THIS / FROM / this_union
```

Use:  

Returns true if the nation specified has the same cultural union as the country in scope.

#### total_amount_of_divisions

Syntax:	

```
total_amount_of_divisions = x
```

Use:  

Returns true if the number of divisions belonging to a country is equal to x or more. Note: An army needs at least 2 brigades to count as a division.

#### total_amount_of_ships

Syntax:	

```
total_amount_of_ships = x
```

Use:  

Returns true if the number of ships belonging to a country is equal to x or more.

#### total_defensives

Syntax:	

```
total_defensives = x
```

Use:  

Returns true if the current country is currently involved in x or more defensive battles.

#### total_num_of_ports

Syntax:	

```
total_num_of_ports = x
```

Use:  

Returns true if the current country controls x or more ports.

#### total_offensives

Syntax:	

```
total_offensives = x
```

Use:  

Returns true if the current country is currently involved in x or more offensive battles.

#### total_of_ours_sunk

Syntax:	

```
total_of_ours_sunk = x
```

Use:  

Returns true if the number of sunken ships belonging to the current country is equal to x or more.

#### total_pops

syntax:

```
TAG = { total_pops = N }
```

use:  

Returns true if the tag has equal or more pops than N.

#### total_sea_battles

Syntax:	

```
total_sea_battles = x
```

Use:  

Returns true if the number of sea battles currently undertaken is equal to x or more.

#### total_sunk_by_us

Syntax:	

```
total_sunk_by_us = x
```

Use:  

Returns true if the total number of ships sunk by the current country is equal to x or more.

#### trade_policy

Syntax:	

```
trade_policy = [policy]
```

Use:  

Returns true if the country has the specified trade policy (from common\issues.txt) (example: "trade_policy = free_trade")

#### truce_with

Syntax:	

```
truce_with = [tag/this/from]
```

Use:  

Returns true if the current country has a truce with the specified country.

#### unemployment

Syntax:	

```
unemployment = x
```

Use:  

Returns true if the unemployment percentage is equal to x or higher.

#### unit_has_leader

Syntax:	

```
unit_has_leader = [yes/no]
```

Use:  

Returns true if any unit in the current country has a leader.

#### unit_in_battle

Syntax:	

```
unit_in_battle = [yes/no]
```

Use:  

Returns true if the country has any unit that is fighting a battle.

#### upper_house

Syntax:	

```
upper_house = {
                                          ideology = name
                                          value = 0.x  
			}
where value is a fraction 0.0 to 1.0, so value 0.4 = 40% has that ideology
```

Use:  

Returns true if the country's upper house has the required characteristics

#### vassal_of

Syntax:	

```
vassal_of = [tag/this/from]
```

Use:  

Returns true if the current country is a puppet state to the specified country.

#### war

Syntax:	

```
war = [yes/no]
```

Use:  

Returns true if the current country is at war.

#### war_exhaustion

Syntax:	

```
war_exhaustion = x
```

Use:  

Returns true if the country’s war exhaustion is equal to x or above.

#### war_policy

Syntax:	

```
war_policy = [policy]
```

Use:  

Returns true if the country has the specified war policy. E.g. Pacifism.

#### war_score

Syntax:	

```
war_score = x
```

Use:  

Returns true if any war score a country is involved in is at least x%.

#### war_with

Syntax:	

```
war_with = [tag/FROM/THIS]
```

Use:  

Returns true if the current country is at war with the specified country.

### Province Scope

#### average_consciousness

Syntax:	

```
average_consciousness = X
```

Use:  

Returns true if the province has a consciousness average at or above X.

#### average_militancy

Syntax:	

```
average_militancy = X
```

Use:  

Returns true if the province has a militancy average at or above X.

#### can_build_factory

Syntax:	

```
can_build_factory = [yes/no]
```

Use:  

Returns true if the province in scope can construct a factory if the owner has the capability to do so.  

(The tooltip displays "can *not* build factory". This is probably a mistake in the text.csv localization file.)

#### continent

Syntax:	

```
continent = [name of continent]
```

Use:  

Returns true if the current province belongs to the specified continent.

#### controlled_by

Syntax:	

```
controlled_by = [tag/FROM/THIS]
```

Use:  

Returns true if the specified country controls the current province.

#### controlled_by_rebels

Syntax:

```
controlled_by_rebels = [yes/no]
```

Use:  

Determines whether the province is currently under rebel control (you may also use "controlled_by = REB").

#### country_units_in_province

Syntax:	

```
country_units_in_province = [tag/FROM/THIS]
```

Use:  

Returns true if the specified country has any units in the current province.

#### country_units_in_state

Syntax:	

```
country_units_in_state = [tag/FROM/THIS]
```

Use:  

Returns true if the specified country has any units in the current state. Localisation for the state may be broken.

#### crime_fighting

Syntax:	

```
crime_fighting = x
```

Use:  

Returns true if the current country invest x% or more in crime fighting.

#### education_spending

Syntax:	

```
education_spending = x
```

Use:  

Returns true if the current country invest x% or more in education.

#### empty

Syntax:

```
empty = [yes/no]
```

Use:  

Returns true if the current province is empty (uncolonized).

#### flashpoint_tension *HOD ONLY*

Syntax:	

```
flashpoint_tension = x
```

Use:  

Returns true if the flashpoint tension in the province is greater than or equal to the specified amount.

#### has_building

Syntax:	

```
has_building = [building type]
```

Use:  

Returns true if the current province has the specified building.

#### has_crime

Syntax:	

```
has_crime = [crime type]
```

Use:  

Returns true if the province has the specified crime.

#### has_culture_core (needs clarification)

Syntax:	

```
has_culture_core = [yes/no]
```

Use:  

Returns true if the pop in scope has the same culture as one of the core nations in the province.  IE Mexican culture in California will receive a -20 factor to assimilation in American owned California until USA removes the Mexican cores.

#### has_empty_adjacent_province

Syntax:	

```
has_empty_adjacent_province = [yes/no]
```

Use:  

Returns true if the current province has an empty adjacent province.

#### has_empty_adjacent_state

Syntax:	

```
has_empty_adjacent_state = [yes/no]
```

Use:  

Returns true if the current province has an empty adjacent state.

#### has_factories

Syntax:	

```
has_factories = [yes/no]
```

Use:  

Returns true if the province in scope has any factories.

#### has_flashpoint

Syntax:	

```
has_flashpoint = [yes/no]
```

Use:  

Returns true if the province has flashpoint tension.

#### has_national_minority

Syntax:	

```
has_national_minority = [yes/no]
```

Use:  

Returns true if there are pops of different cultures in the province.

#### has_pop_type

Syntax:	

```
has_pop_type = [pop type]
```

Use:  

Returns true if the current province has any pops of the specified type.

#### has_province_flag

Syntax:	

```
has_province_flag = [name of flag]
```

Use:  

Returns true if the province in scope has the specified province flag. Note: Doesn't seem to work correctly, usually returning true even if the province doesn't have the flag.

#### has_province_modifier

Syntax:	

```
has_province_modifier = [name of modifier]
```

Use:  

Returns true if the current province has the specified modifier.
This is not a valid condition for the POP files.

#### has_recent_imigration

Syntax:	

```
has_recent_imigration = X 
```

Use:  

Returns true if the current province has received any immigrants in the past X days.

#### [ideology]

Syntax:

```
[ideology] = x
```

Use:  

Returns true if at least x% of the province’s population follows the specified ideology.  

E.g. liberal = 10 will return true if *population*, NOT voter, support for liberal ideology is at least 10%. This is the same information as that displayed on the pop ideology pie chart in the population screen for that province.

#### is_accepted_culture

Syntax:

```
is_accepted_culture = [yes/no]
```

Use:  

Returns true if the province's majority culture is the same as the owning country's accepted culture(s).
  

NB: You can also specify a country tag to the command (including THIS/FROM) and it will return true if the majority culture is the same as the specified country's accepted culture(s).

#### is_blockaded

Syntax:	

```
is_blockaded = [yes/no]
```

Use:  

Returns true if the province is blockaded.

#### is_capital

Syntax:	

```
is_capital = [yes/no]
```

Use:  

Returns true if the current province is a capital.

#### is_coastal

Syntax:

```
is_coastal = [yes/no]
```

Use:  

Determines whether the province is on a coast (note this means any body of water, even an inland lake—if you want to determine if it's a province that could build a port, use the port command).

#### is_colonial

Syntax:	

```
is_colonial = [yes/no]
```

Use:  

Returns true if the current province is a colonial province or not

#### is_core

Syntax:

```
is_core = [tag/THIS/FROM]
```

Use:  

Returns true is the current province is has a core belonging to the specified country.

#### is_ideology_enabled

Syntax:	

```
is_ideology_enabled = [ideology type]
```

Use:  

Returns true if the specified ideology has been enabled.

#### is_overseas

Syntax:

```
is_overseas = [yes/no]
```

Use:  

Returns true if the specified province is overseas (defined by the game as being on a different continent and not contiguous with the country's non-overseas provinces).

#### is_primary_culture

Syntax:

```
is_primary_culture = [yes/no]
```

Use:  

Returns true if the province's majority culture is the same as the owning country's primary culture.
  

NB: You can also specify a country tag to the command (including THIS/FROM) and it will return true if the majority culture is the same as the specified country's primary culture.

#### is_state_capital

Syntax:	

```
is_state_capital = [yes/no]
```

Use:  

Returns true if the province in is the state (the region) capital.

#### is_state_religion (needs clarification)

Syntax:

```
is_state_religion = [yes/no]
```

Use:  

Likely returns true if the state which the province resides has a religious majority of the primary religion of the nation that owns it.

#### life_rating

Syntax:

```
life_rating = x
```

Use:  

Returns true if the life rating in the province is greater than or equal to the specified amount.

#### literacy

Syntax:

```
literacy = x
```

Use:  

Returns true if the average literacy in the province is greater than or equal to the specified amount.

#### military_spending

Syntax:	

```
military_spending = x
```

Use:  

Returns true if the current country are investing x% or more in the military.

#### minorities

Syntax:	

```
minorities = [yes/no]
```

Use:  

Returns true if there are pops of a non-accepted culture in the province.

#### owned_by

Syntax:	

```
owned_by = [tag/FROM/THIS]
```

Use:  

Returns true if the specified country owns the current province.

#### pop_militancy

Syntax:	

```
pop_militancy = x
```

Use:  

Returns true if any pop in the province has a militancy value equal to x or higher.

#### port

Syntax:	

```
port = [yes/no]
```

Use:  

Returns true if the current province has a port (even if it's level 0). Note that the main use for this, as opposed to is_coastal, is that it specifically returns true for provinces that COULD build a port, as opposed to provinces that border a body of water even if it's an inland lake.

#### province_control_days

Syntax:

```
province_control_days = X
```

Use:  

Returns true if the province has been controlled for X number of days by someone other than the owner.

#### province_id

Syntax:	

```
province_id = [province id]
```

Use:  

Returns true if current province has the specified ID.

#### region

Syntax:	

```
region = [name of region]
```

Use:  

Returns true if the province belongs to the specified region.
Note: In regions.txt provinces can be assigned to multiple regions, which can be used here. Only the first assigned region will be used for normal ingame activites. A region is more commonly referred to as a state.

#### state_id

Syntax:	

```
state_id = [province id]
```

Use:  

Returns true if the specified province belongs to the same state as the province in the current scope.

#### terrain

Syntax:

```
terrain = [terrain type]
```

Use:  

Returns true if the province in scope has the specified terrain type (from map\terrain.txt).

#### trade_goods

Syntax:	

```
trade_goods= [type]
```

Use:  

Returns true if the trade good in the province matches “type”.

#### total_pops

syntax:

```
total_pops = [number]
```

use:  

Returns true if the total pops in provinces match the specified number.

#### unemployment

Syntax:	

```
unemployment = 0.xx 
```

Use:  

Returns true if there is x% or more unemployment in the province, valued between 0.00 and 1.00

#### unemployment_by_type

Syntax:

```
unemployment_by_type = {
	type = [poptype]
	value = x
}
```

Use:  

Returns true if there is x% unemployment for pops of that poptype (with x between 0 and 1).

Example:

```
unemployment_by_type = {
	type = farmers
	value = 0.5 
}
```

This would return true if farmers in the province were more than 50% unemployed.

#### units_in_province

Syntax:	

```
units_in_province = x
```

Use:  

Returns true if there are x or more units in the current province.

#### work_available

Syntax:	

```
work_available = {
			worker = [type]
}
```

Use:  

Returns true if there is any work available for the specified pop type—meaning specifically is it possible for that pop type to be employed, not whether they would actually find work there or whether there's any unemployment in the province. If a province has factories, this command will always return true for craftsmen and clerks. If the province produces coal, this command will always return true for labourers and false for farmers.

### Pop Scope

#### agree_with_ruling_party

Syntax:	

```
agree_with_ruling_party = X
```

Use:  

Returns true if the POP agrees with at least X percentage (a range of 0.0 to 1.0) of their ruling party's platform issues.

#### cash_reserves

Syntax:	

```
cash_reserves = x
```

Use:  

Returns true if any pop in the province has a cash reserve equal to the cost of x percentage of their daily needs.

#### consciousness

Syntax:	

```
consciousness = x
```

Use:  

Returns true if the consciousness value is equal to x or higher.

#### culture

Syntax:	

```
culture = [culture name]
```

Use:  

Province Scope Effects: Returns true if there is a majority of the specified culture in the specified province.  

POP Scope Effects: **Warning!** Only returns true if there is a majority of the specified culture in the POP's province. To check if the POP itself has the culture, use "has_pop_culture" instead.

#### everyday_needs

Syntax:	

```
everyday_needs = x
```

Use:  

Returns true if any pop in the province has everyday needs equal to x or more.

#### has_pop_culture

syntax:

```
has_pop_culture = [culture] [THIS]
```

Use:  

Returns true if any pop in scope has the specified culture.

#### has_pop_religion

Syntax:	

```
has_pop_religion = [religion] [THIS]
```

Use:  

Returns true if any pop in scope has the specified religion.

#### is_primary_culture

Syntax:

```
is_primary_culture = [yes/no]
```

Use:  

Returns true if culture of the pop in scope is the same as the primary culture of the nation they reside in.
  

NB: You can also specify a country tag to the command (including THIS/FROM) and it will return true if the culture of the pop in scope matches the primary culture of the country specified.

#### is_accepted_culture

Syntax:

```
is_accepted_culture = [yes/no]
```

Use:  

Returns true if culture of the pop in scope is the same as the accepted culture(s) of the nation they reside in.
  

NB: You can also specify a country tag to the command (including THIS/FROM) and it will return true if the culture of the pop in scope matches the accepted culture(s) of the country specified.

#### is_culture_group

Syntax:

```
is_culture_group = [culture/tag/FROM/THIS]
```

Use:  

Returns true if the pop in scope is of the specified culture group, or if a country is specified, equal to the culture group of the primary culture of that country.

#### is_state_religion

Syntax:

```
is_state_religion = [yes/no]
```

Use:  

Returns true if the pop in question has the same religion as the state religion.

#### life_needs

Syntax:	

```
life_needs = x
```

Use:  

Returns true if any pop in the province life needs equal to x or more.

#### literacy

Syntax:	

```
literacy = x
```

Use:  

Returns true if the literacy value is equal to x or higher.

#### luxury_needs

Syntax:	

```
luxury_needs = x
```

Use:  

Returns true if any pop in the province has a luxury need equal to x or more.

#### militancy

Syntax:	

```
militancy = x
```

Use:  

Returns true if the militancy value is equal to x or higher.

#### money

Syntax:	

```
money = x
```

Use:  

Returns true if any pop in the province has a cash reserve equal to x or higher. Note: Though this condition displays properly in tooltips, it doesn't seem to actually work.

#### political_movement

Syntax:	

```
political_movement= [yes/no]
```

Use:  

Returns true if the pop is currently part of any political movement.

#### political_reform_want

Syntax:	

```
political_reform_want = x
```

Use:  

Returns true if the pop in scope has a political reform want percentage greater than or equal to the specified amount.

#### pop_majority_culture

Syntax:	

```
pop_majority_culture = (culture)
```

Use:  

Returns true if the majority of the pop(s) are of the specified culture.

#### pop_majority_ideology

Syntax:	

```
pop_majority_ideology = (ideology)
```

Use:  

Returns true if the majority of the pop(s) have the specified ideology.

#### pop_majority_issue

Syntax:	

```
pop_majority_issue = (issue type)
```

Use:  

Returns true if the majority of a nation's population/if the majority of the pop(s) have the specified majority issue.

#### pop_majority_religion

Syntax:	

```
pop_majority_religion = (religion)
```

Use:  

Haven't tested, but presumably returns true if the majority of the pop(s) have the specified religion.

#### religion

Syntax:	

```
religion = [religion name]
```

Use:  

Returns true if the pop's cultural government has the specified state religion.  See cultural union in common\cultures.txt

#### social_movement

Syntax:	

```
social_movement = [yes/no]
```

Use:  

Returns true if the pop is currently part of any social movement.

#### social_reform_want

Syntax:

```
social_reform_want = x
```

Use:  

Returns true if the pop in scope has a social reform want percentage greater than or equal to the specified amount.

#### strata

Syntax:

```
strata = [poor/middle/rich]
```

Use:  

Returns true if the pop is of the specified strata.

#### type

Syntax:	

```
type= [type]
```

Use:  

Returns true if there are any pop types of the specified “type”.

#### unemployment

Syntax:	

```
unemployment = x
```

Use:  

Returns true if the unemployment percentage is equal to x or higher.

### See also

- [Modding overview](folder-file-overview.md)
- [Advanced events](event-modding.md)
- Full list of effects
- Full list of scopes
- [Modifier effects](modifier-effects.md)
