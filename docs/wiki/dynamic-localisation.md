# Dynamic localisation

Source: https://vic2.paradoxwikis.com/Dynamic_localisation

[Localisation](localisation.md) for events and decisions is usually static, outside of some specific [localisation keys](localisation.md). However, through abuse of the `change_region_name` [effect](list-of-effects.md), one can write text with any arbitrary content that changes dependent on in-game dynamic conditions.

### Guide

Events and decisions can have effects that impact on regions, and these region names appear in the mouse over of the options to choose in an event or the tick to accept a decision. We can use the `change_region_name` effect to change the name of the region to anything we want it to be, based on whatever conditions we want, and then show the result back to the player.

Firstly, set up a region in region.txt. Note that provinces can be in multiple regions at the same time, there does not appear to be any limit - so long as your dynamic localisation region appears after the actual state you want the province to be in, there is no impact. You can also arbitrarily assign a sea province to a region.

```
dynamic_localisation_region = { 3248 }
```

Then in the effect scope of an event or decision you can summon the arbitary text to appear on mouseover by simply calling the region scope with nothing in it:

```
political_decisions = {
	show_dynamic_localisation = {
		potential = {
			...
		}
		effect = {
			dynamic_localisation_region = {}
		}
	}
}
```

To change the text being shown, in an effect block use the `change_region_name` effect. Note that you must secede the province to the country doing the changing of the region name - calling `secede_province` with an empty tag as demonstrated will revert to no owner, which is useful when using dynamic localisation on sea province regions. Note the region scope can also take a limit block, a form of [IF Emulation](if-emulation.md), meaning the text can be dynamically set based on conditions.

```
political_decisions = {
	change_dynamic_localisation = {
		potential = {
		    3248 = { secede_province = THIS }
		    dynamic_localisation_region = {
			    state_scope = { change_region_name = "My text is now this!" }
		    }
		    3248 = { secede_province = --- }
		}
		effect = {
			dynamic_localisation_region = {}
		}
	}
}
```

### See also

Dynamic localisation is similar to the concept of [metaregions](https://eu3.paradoxwikis.com/Metaregions).
