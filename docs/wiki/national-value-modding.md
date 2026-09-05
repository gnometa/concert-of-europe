# National value modding

Source: https://vic2.paradoxwikis.com/National_value_modding

This page documents the how to edit to effects of National values, how to add new ones, and how the change the national value of each specific country. The documents needed are *nationalvalues.txt* found in the *Victoria 2 -> Common* folder and country files found in *Victoria 2 -> History -> Countries* 

### Editing and creating National Values

This part details how you create a new national value or edit an existing one. 

The nationalvalues.txt document should look like this:

```
nv_order = {
	mobilisation_size = 0.04
	mobilisation_economy_impact = 1.0
}

nv_liberty = {
	mobilisation_size = 0.02
	mobilisation_economy_impact = 0.75
}

nv_equality = {
	mobilisation_size = 0.06
	mobilisation_economy_impact = 1.25
}
```

It mentions the existing national values; Order, Liberty and Equality and there effects on mobilization. To create a new one, simply at a fourth and put in the effects, you want. Only [country modifiers](modifier-effects.md) are used. Note that in addition to the effects found in this file, national values affect other things, for example POPs' ideologies.

### Setting the national value of a specific country

To actually use a national value, you have to go to *Victoria 2 -> History -> Countries* and find the country, you want to edit the national value of.

Each country is called its three letter acronym and its name. For example 'BAD - Baden.txt'.

In this file you find the line *nationalvalue = nv_order*. It should be in line 6. Simply change the nv_order part to the one you want.

### See also

- National Value
- [How to make a country](creating-a-country.md)
