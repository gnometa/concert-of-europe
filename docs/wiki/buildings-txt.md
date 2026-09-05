# Buildings.txt

Source: https://vic2.paradoxwikis.com/Buildings.txt

**Buildings** (forts, naval bases, railroads and factories) are defined in this file. Factories act fundamentally different than the three others, since they are build at state level, while the other is build on province level.<ref>While Naval bases can only be build once pr state, they are still build in one specific province and have province specific effects, which makes them a province building.</ref>

### Syntax

```
fort = {      
	type = fort
	goods_cost =
	{
		lumber = 100
		cement = 100
		explosives = 50
		small_arms = 50
		artillery = 40
	}
	time = 1080 
	visibility = yes
	onmap = yes
	max_level = 6
	province = yes
	fort_level = 1
}
naval_base = {    
	type = naval_base
	cost = 15000
	goods_cost =
	{
		timber = 50
		lumber = 50
		cement = 100
		steel = 100
		machine_parts = 1
	}
	time = 1080
	naval_capacity = 1
	capital = yes
	onmap = yes
	port = yes
	visibility = yes
	max_level = 6
	colonial_points = { 30 50 70 90 110 130 } #points at levels 1-6
	province = yes
	one_per_state = yes
	colonial_range = 50
	local_ship_build = -0.10
}
```

#### Cost and goods cost

The `goods_cost` field determines what goods the state must buy to build this building. These values are static. The `cost` field for buildings defines an extra money cost that will be applied on top of the money cost calculated based on the goods the building costs. Interestingly, this extra cost scales with level so if cost = 1500, level 1 will cost 1500, level 2 will cost 3000 and so on. In the base game, only the naval base makes use of this field.

#### Time

Time defines how long it takes to build said building.

#### Pop build factory

The `Pop_build_factory = (yes/no)` determines if capitalists can build said building via investment.

#### Max level

Max level determines how many levels of a building can be build. The default is 6 for province buildings and 99 for factories. These can be changed by the modder easily, as the effects and costs would just scale.

#### Specific for Province buildings

The `province = (yes/no)` defines if the building can be build once per state (like naval bases) or once pr province. 

Province buildings can generally have any modifier effect that an event modifier can possess, but there is a significant limitation: for most of them, the building may only have one (the last defined one being the one that counts). Another issue is that although the modifier effects do work for the province buildings, and they do show up properly in the tooltips of the province itself, they do not show up in other tooltips where they should. 

#### Specific for factories

The actual goods the factory produces is defined by the `production_type = (production_type)` Production types are defined in production_types.txt, which defines production formulae for both factories and artisans.

```
fabric_factory = {
	type = factory
	on_completion = factory
	completion_size = 0.2
	max_level = 99
	goods_cost =
	{
		machine_parts = 20
		iron = 200
		cement = 200
	}
	time = 365
	visibility = yes
	onmap = no

	production_type = fabric_factory
	pop_build_factory = yes
}
```

### Limitations and requirements

#### not_if_x_exists

The `not_if_x_exists` field determines which other buildings impede this one from being constructed. It has been confirmed to work for province buildings, but it is unknown if it works for factories. It is not actually used in the base game.

Syntax: 
```
not_if_x_exists = { n }
```
```
where n is the name of the province building to be incompatible with this one
```

Note that although this works correctly, the interface tooltip will have an issue. It will display the name of the building to be constructed itself, rather than the one blocking it. It is possible to alter the localisation tag (BUILDING_BLOCKED_BY) to refer to a particular building, however.

#### prerequisites

The `prerequisites` field is almost the mirror opposite to `not_if_x_exists`. It defines which other buildings any necessary in the province before this one can be constructed. The field has been tested and confirmed to work for province buildings; whether it works for factories is unknown. It is not actually used in the base game.

Syntax: 
```
prerequisites = { n }
```
```
where n is the name of the province building to be required
```

Note that although the requirement works correctly, the displayed text does not. For example, if you create a university building and make it require a school, the displayed text will nevertheless be "Must have University", rather than "Must have School". No way is currently known to fix this, as in the relevant localisation tag (BUILDING_MUST_HAVE), the "$OTHER$" is interpreted by the game as referring to the name of the building to be constructed itself, rather than the prerequisite. It is possible to change that localisation tag to directly refer to the name of a particular building, however.

### Misc

It is possible to create new types province buildings in addition to the three in the game, but it is trickier than modding the existing three. This is because it also requires modding the interface. Otherwise the game would crash when you click on a province. 

Another issue is that the AI will not build new province buildings by itself, so you will need to create special events or decisions for it to construct the new buildings.

### Notes

<references />
