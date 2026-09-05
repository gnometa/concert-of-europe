# Crime Modding

Source: https://vic2.paradoxwikis.com/Crime_Modding

This page documents the how to edit to effects of crime effects and how to add new ones. The documents needed is *crimes.txt* found in the *Victoria 2 -> Common* folder.

### Editing and creating Crime modifiers

This part details how you create a new national type of crime or edit an existing one. 

The units in crime.txt document should look like this:

```
anarchic_bomb_throwers = {
	pop_consciousness_modifier = 0.05
	icon = 1	
	
	trigger = {
	}	
}

citizen_guard = {
	life_rating = -0.02
	local_rgo_output = -0.1
	icon = 2	
	
	trigger = {
	}		
}
```

This is an example of some of the existing types of crime modifiers. In total there should be 8 different types of crime modifiers. To create a new one, another at the bottom and put in the effects, you want.

### Icons

The icon mentioned in to a file in the GFX folder.
