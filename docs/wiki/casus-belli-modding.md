# Casus belli modding

Source: https://vic2.paradoxwikis.com/Casus_belli_modding

This page documents the how to edit casus belli and how to add new ones. The documents needed is *cb_types.txt* found in the *Victoria 2 -> Common* folder.

### The file structure

The code for a casus belli should look like this:

```
conquest = {
	sprite_index = 2
	is_triggered_only = yes
	months = 12
	crisis = no
	
	can_use = {
		NOT = { is_our_vassal = THIS }
		# only one state or unciv
		NOT = { number_of_states = 5 }
		OR = {
			AND = {
				civilized = yes
				NOT = { number_of_states = 2 }
			}
			AND = {
				civilized = no
				THIS = { civilized = no }
				NOT = { number_of_states = 2 }
			}
			AND = {
				civilized = no
				number_of_states = 2
				THIS = {
					OR = {
						NOT = { is_greater_power = yes }
						NOT = { nationalism_n_imperialism = 1 }
					}
				}
			}
		}
		is_independant = yes
	}

	badboy_factor = 2.2
	prestige_factor = 5
	peace_cost_factor = 1
	penalty_factor = 1
	
	break_truce_prestige_factor = 5
	break_truce_infamy_factor = 2
	break_truce_militancy_factor = 2
	truce_months = 0
	
	good_relation_prestige_factor = 1
	good_relation_infamy_factor = 1
	good_relation_militancy_factor = 1
	
	construction_speed = 0.5
	
	on_add = {
		move_issue_percentage = { 
			from = jingoism 
			to = pro_military
			value = 0.25
		}
	}
	
	po_annex = yes
	
	war_name = WAR_CONQUEST_NAME
}
```

Sprite index refers to the icon. The number refers to a certain file in the gfx folder.

#### Common effects

Is_triggered_only and constructing_cb accepts the values yes and no. Together they define if the casus belli can be fabricated or not. Yes in is_triggered only and No in constructing_cb indicates that it only can be created by event. They default to yes

Months define the time this CB will be valid. Only works for triggered CBs. The default is 12 months.

The content in Can_use defines who the CB can be used against.

The badboy_factor defines the infamy cost of fabricating the casus belli. The infamy cost will be ten times the value so 2.2 in the example above means it costs 22 infamy.

the prestige_factor defines the amount of prestige earned by succesfully pressing this war goal.

peace_cost_factor defines the cost of the peace options in the peace treaty.

Construction speed defines how fast it is to fabricate said casus belli. It defaults to 1, which is the base construction speed. 0.5 means the constuction takes twice as long time, while 1.5 means it is 50% faster.

On_add defines the effect on the attacking country, when the casus belli is added as a secondary war goal.

War_name defines what the war will be called, when used for the first casus belli. if WAR_NAME is used, it means that this CB is only used as a second objective and thus cannot define the war name.

The po_XXX defines what the war goal actually is about. There is a set list of possible options. They are:
1. po_annex
1. po_demand_state
1. po_add_to_sphere
1. po_disarmament
1. po_reparations
1. po_transfer_provinces
1. po_remove_prestige
1. po_make_puppet
1. po_release_puppet
1. po_status_quo
1. po_install_communist_gov_type
1. po_uninstall_communist_gov_type
1. po_remove_cores
1. po_colony

#### Uncommon effects

Here is a list of effects that are only used in certain circumstances:
1. great_war_obligatory - cb is always added to the peace offer/demand in great wars.
1. po_remove_cores - Removes the cores from a province taken, mostly used in independence wars. may be used only with: po_transfer_provinces, po_demand_state, po_annex
1. crisis - accepts yes and no. Yes means that the CB can be offered as a wargoal in a crisis.
1. mutual - The CB effects will also be used by the defender in peace treaties. Mostly used in civil wars where both countries completely annex the other.

### Infamy / Badboy

It is possible to change the limit of infamy it takes for the great powers to get a *cut down to size* casus belli in the [defines.lua](defines-lua.md) file (default is 25).
