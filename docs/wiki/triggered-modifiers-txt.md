# Triggered modifiers.txt

Source: https://vic2.paradoxwikis.com/Triggered_modifiers.txt

The **Triggered modifiers.txt** can be found in the Victoria2/common folder and is meant to contain various constant modifiers. By default this file contains only comments, but you can put country level [modifiers](modifier-effects.md) that are applied under certain [conditions](list-of-conditions.md) here. The conditions are checked once per month. For example:

```
populationsize_30k  = {
	trigger = {
		total_pops = 7500
		NOT = {
			total_pops = 25000
		}
	}
	research_points = -1
	global_population_growth = 0.003
	icon = 11
}
```

The trigger part contains the conditions, the icon is one from the [modifier icons](modifier-effects.md) and the rest of the triggered modifier contains the country scope modifier effects that have to be applied.
