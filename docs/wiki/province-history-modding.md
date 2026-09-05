# Province history modding

Source: https://vic2.paradoxwikis.com/Province_history_modding

This page documents the formatting and creation of province history files.

### What does a province history file look like?

Province history files are found within history\provinces. From there they divided into various regions. Each province in the game has a seperate file named province number - province name. Example: 256 - Belfast.

##### Required info

At the bare minimum, most provinces files will look like this:

```
owner = TAG           #Tag of owner country
controller = TAG      #Tag of controller country
add_core = TAG        #Tag of core country
add_core = TAG        #A second core country's tag. 
trade_goods = (good)  #Resource in province
life_rating = x       #Life rating of province
```

The controller of a province determines if it is occupied at the start of the game. Unless we are talking about rebels (which is a tag; REB), this is really only used if the country starts at war. If owner and controller is the same tag, the province is unoccupied. Otherwise it is occupied.
There can only be one controller and one owner, but there is no limit to the number of cores a province can have.

##### Additional info

Many provinces will have much more in their history files. Since all values defaults to either 0 (for numeric values) or no (for boolean values), if something is not wanted, there does not need to be any code.

example of London, from vanilla:

```
owner = ENG
controller = ENG
add_core = ENG
trade_goods = grain
life_rating = 45
fort = 1
party_loyalty = {
	ideology = liberal
	loyalty_value = 10.5
}
state_building = {
	level = 1
	building = furniture_factory
	upgrade = yes
}
state_building = {
	level = 1
	building = paper_mill
	upgrade = yes
}
state_building = {
	level = 1
	building = ammunition_factory
	upgrade = yes
}
state_building = {
	level = 1
	building = small_arms_factory
	upgrade = yes
}
state_building = {
	level = 2
	building = clipper_shipyard
	upgrade = yes
}
1861.1.1 = {
	state_building = {
		level = 1
		building = luxury_clothes_factory
		upgrade = yes
	}
	state_building = {
		level = 1
		building = luxury_furniture_factory
		upgrade = yes
	}
}
1861.1.1 = { railroad = 3 }
```

There is a lot to break down here, but let's start small.

```
owner = ENG
controller = ENG
add_core = ENG
trade_goods = grain
life_rating = 45
```

This says that London is owned, controlled, and cored by the ENG tag, or the United Kingdom. It's resource is grain, and the life rating is high at 45. 

Now, for the new stuff:

```
fort = 1
```

London also has a level 1 fort present.

party_loyalty = {
	ideology = liberal
	loyalty_value = 10.5
}

This says that London has a significant loyalty towards the liberal ideology.

```
state_building = {
	level = 1
	building = furniture_factory
	upgrade = yes
}
state_building = {
	level = 1
	building = paper_mill
	upgrade = yes
}
```

This says that the state London is in owns two level one factories, a furniture factory and a paper mill.

```
1861.1.1 = {
	state_building = {
		level = 1
		building = luxury_clothes_factory
		upgrade = yes
	}
	state_building = {
		level = 1
		building = luxury_furniture_factory
		upgrade = yes
	}
}
1861.1.1 = { railroad = 3 }
```

This says that in the 1861 bookmark, London owns these two new factories and a level three railroad.

### Editing province history files

#### Party loyalty

```
party_loyalty = {
	ideology = (ideology)    #same as in [[ideologies.txt]]
	loyalty_value = x
}
```

#### Buildings

##### Factories

```
state_building = {
	level = x
	building = (building)    #same as in [[buildings.txt]]
	upgrade = yes
}
```

##### Forts and railroads

```
fort = x
railroad = x
```

X here of course refers to the level of each building. It goes from 0 to 6. If you leave it out, it will default to 0 (no building).

#### Different bookmarks

Any of the above entries can be enclosed in date brackets so that they do not appear until later bookmarks.

```
1861.1.1 = { 
owner = PRU
controller = PRU
add_core = PRU
remove_core = AUS
}
```

This will make it so that in the ACW bookmark, the province will change hands from Austria to Prussia. 

### Bugfixing

If a certain province looks to have a core with the rebel flag, it is likely because you have added a core to a country that does not exist (meaning they have not been defined in the common/countries.txt file). It is likely because you have written the three letter acronym wrong.
