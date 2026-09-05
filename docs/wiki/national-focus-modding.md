# National focus modding

Source: https://vic2.paradoxwikis.com/National_focus_modding

This page documents the how to edit to effects of the  various National focus, how to add new ones. The documents needed are *national_focus.txt* found in the *Victoria 2 -> Common* folder and the icon files found in *Victoria 2 -> History -> GFX*. Lastly you will need the [localisation](localisation.md) files to edit the name and description of the national focus.

### Editing and creating National Values

This part details how you edit the effects of an existing national focus. 

The national_focus.txt document should look like this:

```
rail_focus =
{
	encourage_rail = 
	{
		railroads = 0.5 #Capitalists 50% more likeley to choose railroads
		icon = 2
	}
}

immigration_focus = 
{
	immigration =
	{
		immigrant_attract = 0.2 #increases attactiveness to immigrants by 20 %
		icon = 3
		limit = { 
			#OR = { 
				#continent = north_america
				#continent = south_america
				#is_overseas = yes
			#}  
		}
	}
}

diplomatic_focus =
{
	increase_tension =
	{
		icon = 4
		has_flashpoint = yes
		own_provinces = no

		flashpoint_tension = 0.15

		limit = {
			is_core = THIS
			THIS = {
				is_greater_power = no
			}
		}
	}
}

promotion_focus =
{
	promote_aristocrats =
	{
		aristocrats = 0.20 #20% more likeley to become artisans
		icon = 5
		outliner_show_as_percent = yes
	}

	promote_artisans =
	{
		artisans = 0.20 #20% more likeley to become this type
		icon = 6
		outliner_show_as_percent = yes
	}

	promote_bureaucrats =
	{
		bureaucrats = 0.20 #20% more likeley to become this type
		icon = 7
		outliner_show_as_percent = yes
	}

	promote_capitalists =
	{
		capitalists = 0.20 #20% more likeley to become this type
		icon = 8
		outliner_show_as_percent = yes
		limit = { 
			civilized = yes
		}

	}
	
	promote_clergymen =
	{
		clergymen = 0.20 #20% more likeley to become this type
		icon = 9
		outliner_show_as_percent = yes
	}

	promote_clerks =
	{
		clerks = 0.20 #20% more likeley to become this type
		icon = 10
		outliner_show_as_percent = yes
		limit = { 
			civilized = yes
		}
	}

	promote_craftsmen =
	{
		craftsmen = 0.20 #20% more likeley to become this type
		icon = 11
		outliner_show_as_percent = yes
		limit = { 
			civilized = yes
		}
	}

	promote_farmers =
	{
		farmers = 0.20 #20% more likeley to become this type
		icon = 12
		outliner_show_as_percent = yes
	}
	
	promote_labourers =
	{
		labourers = 0.20 #20% more likeley to become this type
		icon = 13
		outliner_show_as_percent = yes
	}

	promote_officers =
	{
		officers = 0.20 #20% more likeley to become this type
		icon = 14
		outliner_show_as_percent = yes
	}

	promote_soldiers =
	{
		soldiers = 0.20 #20% more likeley to become this type
		icon = 15
		outliner_show_as_percent = yes
	}
}

production_focus =
{
	automation_focus =
	{
		aeroplanes = 18.3
		barrels = 18.3
		automobiles = 18.3
		icon = 16
		limit = { year = 1880 }
	}

	electrical_focus =
	{
		radio = 18.3
		telephones = 18.3
		electric_gear = 18.3
		icon = 17
		limit = { year = 1880 }
	}

	chemical_focus =
	{
		fuel = 18.3
		oil = 18.3
		icon = 18
		limit = { year = 1880 }
	}

	shipping_focus =
	{
		steamer_convoy = 18.3
		clipper_convoy = 18.3
		icon = 19
		limit = { 
			#civilized = yes
			state_scope = { any_owned_province = { port = yes } }
		}
	}

	textile_focus =
	{
		luxury_clothes = 18.3
		regular_clothes = 18.3
		fabric = 0.3
		dye = 0.3
		icon = 20
		#limit = { 
		#	civilized = yes
		#}
	}

	wood_focus = 
	{
		paper = 18.3
		luxury_furniture = 18.3
		furniture = 18.3
		lumber = 18.3
		icon = 21
		#limit = { 
		#	civilized = yes
		#}
	}

	basic_industry_focus =
	{
		steel = 18.3
		machine_parts = 25.3
		cement = 18.3
		icon = 22
		#limit = { 
		#	civilized = yes
		#}
	}

	armaments_focus = 
	{
		artillery = 18.3
		small_arms = 18.3
		ammunition = 18.3
		canned_food = 18.3  
		explosives = 18.3
		fertilizer = 18.3
		icon = 23
		#limit = { 
		#	civilized = yes
		#}
	}

	consumer_focus = 
	{
		liquor = 18.3
		wine = 18.3
		glass = 18.3
		icon = 24
		#limit = { 
		#	civilized = yes
		#}
	}
}

party_loyalty_focus =
{
	fascist_focus =
	{
		ideology = fascist
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 25
	}
	
	reactionary_focus =
	{
		ideology = reactionary
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 26
	}
	
	conservative_focus =
	{
		ideology = conservative
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 27
	}
	
	socialist_focus =
	{
		ideology = socialist
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 28
	}
	
	communist_focus =
	{
		ideology = communist
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 29
	}
	
	liberal_focus =
	{
		ideology = liberal
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 30
	}
	
	anarcho_liberal_focus =
	{
		ideology = anarcho_liberal
		loyalty_value = 0.001 # By that much pops will be more loyal
		icon = 31
	}
}
```

#### Explanation

**Overall category:**
*Coming Soon*

**Limit**:
Here you can change when the national focus should be usable. The ones in use are status, in-game year, ownership status and cores. But it could potentially also be certain technologies, wether the country is at war or not or any other condition.

**Values**
The values of the effects are assumed to be percentages. They are confusingly listed in two different formats. So "regular_clothes = 18.3; fabric = 0.3" means that the capitalists' tendency to build said factory/building is increased by 18.3% and 30% respectively. 

**Icon**
The icon number refers to a file in the GFX folder. When simply changing the effects of an already existing national focus, you don't need to do anything about this.
*Coming soon*

**Encourage industries**
The name of the scope references an instance in the [buildings.txt](buildings-txt.md) file.

**Party Loyalty**
The name refers to an ideology in the ideologies.txt file.

### The defines.lua file

How the amount of primary culture population relates to the amount of NFs is defined in `Victoria II/common/defines.lua`. Inside the file there is NATIONAL_FOCUS_DIVIDER, which is 400000.0 in an unmodded game.

### Creating a new national focus

Creating a new type of national foxus is a little more elaborate than simply editing an already existing one.
First and foremost you will need to add a new icon that can be refered.
