# List of effects

Source: https://vic2.paradoxwikis.com/List_of_effects

This article lists all possible event effects. Add any that are missing.

### Syntax and terminology

Many event options are of the form 

```
X = {
	limit = {
		A = B
	}
	Y = Z
}
```

What this means is that when the event triggers, and this outcome is selected, then for all X such that A = B, Y = Z happens to X. X is the *target* of the command, and may be a group of pops, a group of provinces or states, a country, or other things; A = B is the *condition*, and may be limiting the pops to only those of certain cultures, limiting the states to only those that are slave states, or other things; Y is the *effect*, and Z is the *argument* that tells the effect what to do. This is a general pattern, and may not hold for specific examples.

These may also be nested; for instance, 

```
any_state = {
	limit = {
		is_slave = yes
	}
	any_pop = {
		limit = {
			has_pop_culture = dixie
		}
		consciousness = 0.5
	}
}
```

says that in all states (any_state) that are slave states (limit = {is_slave = yes}), all pops (any_pop) that are of the Dixie culture will have a CON increase of 0.5

### Targets

#### Pops

An effect that applies to pops can target pops in these classes:

| target | what it means |
|---|---|
| any_pop | targets all pops |
|  *aristocrats *artisans *bureaucrats *capitalists *clergymen *clerks *craftsmen *farmers *labourers *officers *slaves *soldiers | the type of pop specified |
|  *poor_strata *middle_strata *rich_strata | all pops in a certain wealth level |

This target can be limited by:
- has_pop_culture = (culture)
- has_pop_religion = (religion)
- is_state_religion = (yes/no)
- type (type = slaves or NOT = { type = slaves}, for example)
- is_primary_culture = (yes/no)
- is_accepted_culture = (yes/no)
- consciousness = n (all pops where CON is at least n)
- militancy = n

#### Province

An effect that targets provinces can target these classes:

| target | what it means |
|---|---|
| any_owned | all provinces; can be nested within a state or country target to give all provinces within the state, states, or country selected. |
| (a province ID) | the province referenced by the ID |
| capital_scope | for a country event, this targets the country's capital province. |

For a province event, if no target is given the effect will target the province for which the event fired.

This target can be limited by:
- is_core = (tag) (to specify provinces that have certain cores on them)
- province_id = n (to exclude specific provinces from a larger group)
- has_province_modifier = (modifier)
- has_province_flag = (flag name) (only provinces that have that flag will be targeted)
- (ideology) = n (only provinces where (ideology) has more than n% representation)
- average_militancy = n (all provinces with average MIL over n)
- average_consciousness = n

#### State

An effect that targets states can target these classes:

| target | what it means |
|---|---|
| random_state | any one state, randomly chosen |
| (a state name, e.g. USA_1) | the state referenced by that name |
| state_scope | For a province event, state_scope is the state containing the province |

This target can be limited by:
- is_slave = (yes/no)
- is_colonial = (yes/no)
- average_militancy = n (all states with average MIL over n)
- average_consciousness = n
- has_pop_type = (type)
- (issue) = n (all states where (issue) is the primary issue for n% of the population)

#### Country

An effect that targets a country as a whole can use these targets

| target | what it means |
|---|---|
| no target given | For a country event, the default target is the country that fired the event |
| (a tag) | the country referenced by the tag |
| any_country | all countries (the current country not included) |
| any_greater_power | randomly choose one of the eight great powers |
| FROM | for a triggered event, FROM is the country that fired the triggering event. |
| THIS | the country that fires a country-scope event. |
| owner | for a province event, owner is the country that owns the province that fired the event |
| sphere_owner | If the country that fired an event is in a sphere, sphere_owner is the nation controlling that sphere |

This target can be limited by:
- has_country_flag = (flag name) (only countries that have that flag will be targeted)
- civilized = (yes/no)
- in_culture_group = (group)
- (reform_class) = (reform_level) (only countries that have a certain level of political or social reform, ex. press_rights = free_press)
- prestige = n (limits to countries with n prestige or more)
- tag = (tag) or, more importantly, NOT = {tag = (tag)} (limits to the country with (or the countries without) the given tag

### Population Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `assimilate` | Province |  ``` assimilate = yes/no ```  | Changes every pop whose province is currently in scope to the country's primary culture. | Only works in the province scope. Example: ``` any_owned = { assimilate = yes } ``` Changes all pops in the country to the primary culture. |
|  `consciousness` | POPs |  ``` consciousness = n ```  | Change the CON of the targeted pop or pops by the given value | Example: ``` poor_strata = { consciousness = 1.5 } ```  |
|  `militancy` | POPs |  ``` militancy = n ```  | Change the MIL of the targeted pop or pops by the given value. | Similar in all aspects to consciousness, as described above. |
|  `dominant_issue` | POPs |  ``` dominant_issue = { value = (issue) factor = n } ```  | Changes the dominant issue of a portion of the targeted pop to the given issue. | Works the same way as [upper_house](list-of-effects.md). |
|  `ideology` | POPs |  ``` ideology = { factor = n value = (name) } ```  | Change the proportion of the targeted pop that follows the specified ideology. | Works the same way as [upper_house](list-of-effects.md). |
|  `literacy` | POPs |  ``` literacy = n ```  | Changes the literacy of the targeted pop by the specified amount. | Example: ``` any_pop = { literacy = -0.10 } ``` Reduces literacy by 10%. |
|  `money` | POPs |  ``` money = n ```  | Changes the target pop's savings by the specified amount. |  |
|  `move_issue_percentage` | POPs |  ``` move_issue_percentage = { from = (issue) to = (issue) value = n } ```  | Makes a certain percentage of people supporting issue A, switch to issue B. This effect is used in the adding of CB, where people switch from jingoism to pro military. |  |
|  `move_pop` | POPs |  ``` move_pop = (province ID) ```  | Moves the targeted pop to the specified province. | When a pop moves to a province where another pop of the same type and religion already exists, he will get merged with the latter regardless of culture - sometimes even if another pop of the same type, religion and culture also exists. What culture a POP turns into when they are moved appears to be based on the order POPs are placed in within the game files. Use with caution. |
|  `pop_type` | POPs |  ``` pop_type = (type) ```  | Changes the type of the targeted pop. |  |
|  `reduce_pop` | POPs |  ``` reduce_pop = n ```  | Changes the targeted pop to the given proportion of its current value. Increases POP size if n>1. | Example: ``` any_pop = { reduce_pop = 0.95 } ``` Reduces every pop by 5%. |
|  `scaled_consciousness` | POPs | Example: ``` scaled_consciousness = { factor = n ideology or issue = (name) } ```  | Changes the consciousness of the targeted pops by the given value multiplied by the proportion of the pop that is of the given ideology or issue. | E.g. if a pop has 40% support for pro-military, and n = 0.5, then the CON increase would be 0.4 * 0.5 = 0.2. |
|  `scaled_militancy` | POPs |  | see `scaled_consciousness` |  |

### Provincial Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `add_core` | Province |  ``` add_core = [TAG/THIS/FROM] ```  | Adds a core of the given country to the targeted province |  |
|  `add_province_modifier` | Province |  ``` add_province_modifier = { name = (modifiername) duration = n } ```  | Adds the specified modifier to the targeted province. *n* in days. |  |
|  `change_controller` | Province |  ``` change_controller = [TAG] ```  | Changes the controller (not owner) of the target province. |  |
|  `change_province_name` |  |  ``` change_province_name = "name" ```  | Changes the province's name to the one specified. |  |
|  `change_region_name` | State |  ``` change_region_name = "name" ```  | Changes the region (state) name to the one specified. | Example: ``` 1 = { state_scope = { change_region_name = "name" } } ``` Don't include ANY other effects in the same province scope as this one, else the event will cause a crash. |
|  `flashpoint_tension` | State |  ``` flashpoint_tension = n ```  | Increases the flashpoint tension of the state by *n*. | HoD only. Example: ``` state_scope = { flashpoint_tension = 10 } ```  |
|  `fort` | Province |  ``` fort = n ```  | Changes the target province's fortification level by *n*. |  |
|  `infrastructure` | Province |  ``` infrastructure  = n ```  | Changes the target province's infrastructure level by *n*. |  |
|  `life_rating` | Province |  ``` life_rating = n ```  | Changes the target province's life rating by *n*. |  |
|  `naval_base` | Province |  ``` naval_base = n ```  | Changes the target province's naval base level by *n*. |  |
|  `remove_core` | Province |  ``` remove_core = [TAG/THIS] ```  | Removes a core of the given country to the targeted province. | FROM does not work. |
|  `remove_province_modifier` | Province |  ``` remove_province_modifier = [modifier name] ```  | Removes the specified modifier from the targeted province. | If the modifier does not currently exist in the province, this command won't appear in the tooltip. |
|  `secede_province` | Province |  ``` secede_province = [tag/THIS/FROM] ```  | Transfers the province in scope from the targeted nation to another. |  |
|  `sub_unit` | Province or Country |  ``` sub_unit = { type = [unit type] value = [province] } ```  | Spawns a unit. | If a province is targeted, and the `value` parameter is not `current`, a ghost unit will be spawned which vanishes upon reloading. Units spawned via this command will spawn with zero experience and will be unable to move until either they are merged with another unit or the game is reloaded. Land units will additionally spawn with 100k strength and without an attached soldier POP. |
|  `trade_goods` | Province |  ``` trade_goods = [type] ```  | Changes the good produced by the target province to the one specified. |  |

### National Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `activate_technology` | Country |  ``` activate_technology = [technology] ```  | Adds the specified technology to the country, whether it is the next level or not. | AHD only |
|  `add_accepted_culture` | Country |  ``` add_accepted_culture = [culture] ```  | Makes the specified culture accepted by the targeted country. |  |
|  `remove_accepted_culture` | Country |  ``` remove_accepted_culture = (culture) ```  | Removes the specified culture as accepted by the targeted country. |  |
|  `add_country_modifier` | Country |  ``` add_country_modifier = { name = [modifier] duration = n } ```  | Adds the specified modifier to the targeted country. *n* is in days. | Won't replace or extend an already existing modifier. |
|  `add_crisis_interest` | Country |  ``` add_crisis_interest = [yes/no] ```  | Involves the country in scope to the current crisis. | HoD only |
|  `add_crisis_temperature` |  |  ``` add_crisis_temperature = n ```  | Increases the temperature of the current crisis by *n*. |  |
|  `badboy` | Country |  ``` badboy = n ```  | Change the target country's infamy by *n*. |  |
|  `build_factory_in_capital_state` | Country |  ``` build_factory_in_capital_state = [factory type] ```  | Starts construction of the given factory type in the capital state of the country. | Works as with the westernization reform. Tested in HoD v3.04 |
|  `capital` | Country |  ``` capital = [province] ```  | Change the capital of the country to the specified province id. |  |
|  `civilized` | Country |  ``` civilized = [yes/no] ```  | Changes the civilized/uncivilized status of the country. |  |
|  `kill_leader` |  |  ``` kill_leader = [ID] ```  | Kills the specified army/navy leader. | The ID can be found in the save file. Unclear if the ID is always the same for leaders created using define_general. |
| `define_admiral` |  |  ``` define_admiral = { name = [name] personality = [trait] background = [trait] } ```  | Creates a new admiral with the specified parameters. | name: see `kill_leader`\|name: see `kill_leader` |
| `define_general` |  |  ``` define_general = { name = [name] personality = [trait] background = [trait] } ```  | Creates a new general with the specified parameters. | name: see `kill_leader` |
|  `nationalvalue` | Country |  ``` nationalvalue = [value] ```  | Changes the national value of the current country to the value specified. | *value* from common\nationalvalues.txt |
|  `plurality` | Country |  ``` plurality = n ```  | Change the plurality of the targeted country by *n*. |  |
|  `prestige` | Country |  ``` prestige = n ```  | Change the prestige of the targeted country by *n*. |  |
|  `prestige_factor` | Country |  ``` prestige_factor = n ```  | Changes the prestige of the targeted country by the current prestige multiplied with *n*. Change cannot be less than ±1. |  |
|  `primary_culture` | Country |  ``` primary_culture = [culture]/[TAG/THIS/FROM] ```  | Changes the target country's primary culture. | This may be used on non-existing countries. |
|  `religion` | Country |  ``` religion = (religion) ```  | Changes the scoped country's state religion to the specified one. | State religion is only visible in save files. |
|   `remove_country_modifier` |  |  ``` remove_country_modifier = [modifier] ```  | Removes a country modifier. | If the country modifier does not exist, the command won't appear in the tooltip. |
|  `research_points` | Country |  ``` research_points = n ```  | Grants *n* RPs to the target country's current research project. |  |
|  `war_exhaustion` | Country |  ``` war_exhaustion = n ```  | Changes the target country's war exhaustion by *n*. |  |
|  `years_of_research` | Country |  ``` years_of_research = n ```  | Grants a number of RP that would have been accumulated over *n* years. |  |
|  `nationalize` | Country |  ``` nationalize = [yes/no] ```  | Turns all factories invested by foreign powers your own. |  |

### Political Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `economic_reform` | Country |  ``` economic_reform = [reform] ```  | Adds the specified economic reform to the uncivilized nation. | AHD only |
|  `election` | Country |  ``` election = yes ```  | Starts the election process ahead of schedule. |  |
|  `enable_ideology` |  |  ``` enable_ideology = [ideology] ```  | Globally enables the specified ideology. |  |
|  `government` | Country |  ``` government = [government] ```  | Changes the target country's government to the specified type. | Does not change any of the country's reforms. |
|  `is_slave` | State |  ``` is_slave = (yes/no) ```  | Sets the slave state / free state status of a state. | Appears in a triggered-only event, syntax doesn't fit the normal model. |
|  `military_reform` | Country |  ``` military_reform = [reform] ```  | Adds the specified military reform to the uncivilized nation. | AHD only |
|  `political_reform` | Country |  ``` political_reform = [reform] ```  | Changes the target country to the specified political reform. |  |
|  `ruling_party_ideology` | Country |  ``` ruling_party_ideology = [ideology] ```  | Changes the current ideology of the country's ruling party. | If there is more than one party for that ideology, the first party listed in the country file is chosen. |
|  `social_reform` | Country |  ``` social_reform = [reform] ```  | Changes the target country to the specified social reform. |  |
|  ===== `upper_house` ===== | Country |  ``` upper_house = { ideology = [ideology] value = [n] } ```  | Changes the proportion of the upper house that follows the specified ideology. | The amount gained (U) is calculated by the following formula: U=1-1/(1+N)  The other values will be multiplied by 1-U.  Example:  Upperhouse starts with 10% (0.1) liberals and 90% (0.9) conservatives.   U=1-1/(1+N)=1-1/(1+0.25)=1-0.8=0.2  1-U=0.8  liberals = 0.1*0.8+.2 = 0.28 = 28%  conservatives = 0.9*0.8 = 0.72 = 72%  N = -1-1/(U-1) |

<!--UNCOMMENT LATER
There are few values that don't result in an endless fraction, below is a list.

Syntax 

```
upper_house = {
	ideology = (name)
	value = N
} 
```

| U (%) | N |
|---|---|
| -100 | -0.5 |
| -28 | -0.21875 |
| 20 | 0.25 |
| 36 | 0.5625 |
| 50 | 1 |
| 60 | 1.5 |
| 68 | 2.125 |
| 75 | 3 |
| 80 | 4 |
| 84 | 5.25 |
| 90 | 9 |
| 92 | 11.5 |
| 95 | 15 |
| 96 | 24 |
| 98 | 99 |

### Diplomatic Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `add_casus_belli` | Country |  ``` add_casus_belli = { target = [TAG/FROM/THIS] type = [casus belli] months = n } ```  | Gives the target a casus belli against the country in scope for *n* months. Optional fields include `state_province_id` for when the casus belli targets a specific state, such as with acquire state, and `country` for when the casus belli targets another country tag, such as with free peoples. |  |
|  `annex_to` | Country |  ``` annex_to = [TAG/THIS/FROM] ```  | Annexes the targeted country to the country in the current scope. |  |
|  <code id="casus belli">casus_belli</code> | Country |  ``` casus_belli = { target = [TAG/FROM/THIS] type = [casus belli] months = n } ```  | Grants the scoped country a casus belli against the target country for *n* months. Optional fields include `state_province_id` for when the casus belli targets a specific state, such as with acquire state, and `country` for when the casus belli targets another country tag, such as with free peoples. |  |
|  `create_alliance` | Country |  ``` create_alliance = [TAG] ```  | Creates an alliance between target country and the scoped country. |  |
|  `create_vassal` | Country |  ``` create_vassal = [TAG] ```  | Makes the specified country a vassal of the scoped country, even if they are already a vassal. |  |
|  `diplomatic_influence` | Country |  ``` diplomatic_influence = { who = [TAG/FROM/THIS] value = n } ```  | Changes the influence that the targeted country has on the specified country by *n*. |  |
|  `end_military_access` | Country |  ``` end_military_access = [TAG/THIS/FROM] ```  | Ends the military access granted by the specified country to the current country. |  |
|  `end_war` | Country |  ``` end_war = [TAG] ```  | Ends any war between the target country and the specified country. | Does not create a truce, and there are no penalties for the cancelled CBs. Will not cancel the war with allies or vassals. |
|  `inherit` | Country |  ``` inherit = [TAG/FROM/THIS] ```  | Adds all provinces of the specified country to the targeted country. |  |
|  `leave_alliance` | Country |  ``` leave_alliance = [TAG/FROM/THIS] ```  | Remove the current country from an alliance with the specified country. |  |
|  `military_access` | Country |  ``` military_access = [TAG/THIS/FROM] ```  | Gives the target country military access to the specified country. |  |
|  `neutrality` | Country |  ``` neutrality = [yes/no] ```  | Dissolves all alliances a nation has and set all satellites free. |  |
|  `relation` | Country |  ``` relation = { who = [TAG/FROM/THIS] value = n } ```  | Changes the relation between the targeted country and the specified country by *n*. |  |
|  `release` | Country |  ``` release = [TAG] ```  | Allows the target country to release the specified country and thereby create a new independent nation. |  |
|  `release_vassal` | Country |  ``` release_vassal = [TAG/FROM/THIS] ```  | If this targets a vassal nation (or substate), the vassal is freed. If this targets a non-existing nation, it is released as a vassal of the current country. | If the capital of the released country is not owned, the country is simply freed outright and not as a vassal (check with `is_possible_vassal`). |
|  `war` | Country |  ``` war = [TAG] ```   ``` war = { target = [TAG] attacker_goal = { casus_belli = [casus belli] } defender_goal = { casus_belli = [casus belli] } call_ally = [yes/no] } ```  | Starts a war between the country for whom the event fired and the given country. | See [[#casus belli\|casus belli]] for info on its options. |

<!--UNCOMMENT LATER
eligible types of casus_belli are status_quo, conquest, civil_war, add_to_sphere, take_from_sphere, acquire_core_state, annex_core_country, acquire_state, place_in_the_sun, cut_down_to_size, free_peoples, release_puppet, humiliate, demand_concession_casus_belli, establish_protectorate_casus_belli, unification_humiliate_cb, unification_casus_belli, unification_annex_casus_belli, or rude_boy.

"call_ally = yes" is optional to include, and when used causes the country to automatically call in all allies (who will elect to join or not join as the AI dictates).

To use a casus_belli that requires an identified country (such as release puppet) use "country":

```
war = {
	target = (tag)
	attacker_goal = {
		casus_belli = release_puppet
                country = (tag)
	}
}
```

To use a casus_belli that requires an identified state (such as acquire_state) use "state_province_id":

```
war = {
	target = (tag)
	attacker_goal = {
		casus_belli = acquire_state
                state_province_id = (province ID# of any province within the state)
	}
}
```

Note that for a free_peoples casus_belli, both "country" and "state_province_id" are required.

There is a trick to calling allies in existing wars: If "target" is not specified, but "call_ally = yes" is present, then your country declares war on a null tag (which is REB), and finishes the war the next day. If your allied nations honored your alliance, then once the null war ends, they will participate in any existing wars your country is in.

```
war = {	
	attacker_goal = {
		casus_belli = (type)
	}	
        call_ally = yes
}
```

Something like this would work, but "attacker_goal" probably is unnecessary here.-->

### Economic Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `add_tax_relative_income` | Country |  ``` add_tax_relative_income = n ```  | Used to remove or add money relative to country's income with maximum taxation. | E.g. if n=0.1, 10% of what income would be if all taxes were maxed out is added. |
|  `[resource name]` | Country |  ``` [resource name] = n ```  | Changes the national stockpile of the resource named by *n*. |  |
|  `treasury` | Country |  ``` treasury = n ```  | Change the amount of cash in the treasury by *n*. | The maximum amount of money you can add to a country's treasury through this effect is 2147483, or 2^31/100. Values greater than this will overflow. |

### Function Effects

| Name |  |  |  |  |
|---|---|---|---|---|
| Target | Syntax | Effect | Notes |  |
|  `change_tag` | Country |  ``` change_tag = [TAG] ```  | Switches the nation in scope to the specified country tag. No cores will change. | `change_tag = culture` changes to the union tag for the currently scope country. The previous example has no effect on cultures with no union tag. |
|  `change_tag_no_core_switch` |  |  ``` change_tag_no_core_switch = [TAG] ```  | Switches the player nation from the current one to the specified one. |  |
|  `change_variable` |  |  ``` change_variable = { which = [variable] value = n } ```  | Increases or decreases the value of an existing variable. |  |
|  `clr_province_flag` | Province |  ``` clr_province_flag = [flag] ```  | Removes the specified province flag. |  |
|  `clr_country_flag` | Country |  ``` clr_country_flag = [flag] ```  | Removes the specified country flag. |  |
|  `clr_global_flag` | Global |  ``` clr_global_flag = [flag] ```  | Removes the specified global flag. |  |
|  `country_event` |  |  ``` country_event = [event] ```   ``` country_event = { id = [event] days = n } ```  | Fires the specified country event for the targeted country. | Second syntax is AHD only. |
|  `province_event` |  |  ``` province_event = { id = [event] } ```  | Fires the specified province event for the targeted province. | Event can only fire for the owner of the province, and does not work on empty provinces. It will however work if you secede_province at the same time. |
|   `random` |  |  ``` random = { chance = n [effects] } ```  | Specifies the probability *n* that the effects specified will occur. |  |
|  `random_list` |  |  ``` random_list = { E1 = { [effect1] } E2 = { [effect2] } ... En = { [effectn] } } ```  | Causes one of two or more possible effects to happen and specifies the probability for each. Probability of any effect Ex occurring is Ex/(E1+E2+...+En). | The actual randomness of this effect varies. If this is a top-level effect, its RNG will be seemingly random for an event, and seeded based on the in-game date (month and year) for a decision. If this is *not* a top-level effect, its output for any given event or decision will be the same every time. |
|  `set_province_flag` | Province |  ``` set_province_flag = [flag] ```  | Sets the specified flag for the current province. |  |
|  `set_country_flag` | Country |  ``` set_country_flag = [flag] ```  | Sets the specified flag on the current country. |  |
|  `set_global_flag` | Global |  ``` set_global_flag = [flag] ```  | Sets the specified flag globally (meaning every tag, existing or not, gets the flag) |  |
|  `set_variable` |  |  ``` set_variable = { which = [name] value = n } ```  | Creates a new variable and assigns it the value *n*. If the variable exists, its value will be set to *n*. |  |

### See also

- List of commands
- [List of scopes](list-of-scopes.md)
- [Modifier effects](modifier-effects.md)
- [Modding overview](folder-file-overview.md)
- [Event modding](event-modding.md)
