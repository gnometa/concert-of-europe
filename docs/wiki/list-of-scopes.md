# List of scopes

Source: https://vic2.paradoxwikis.com/List_of_scopes

This is a **full list of scopes** for scripting event triggers, decision prerequisites, and limits.

Scopes are used to change what an event, decision, or limit is looking at. For example, if you have a provincial event, and wish to look at a population within that province, you use a scope.

### Country Scope: Triggers

#### all_core

Syntax:

```
all_core = { triggers... }
```

Scope:  

Switches scope to all core provinces of the current country in scope - the triggers must be true for all core provinces for this to return true.

#### any_core

Syntax:

```
any_core = { triggers... }
```

Scope:  

Switches scope to all core provinces of the current country in scope - the triggers must be true for one or more core provinces for this to return true.

#### any_greater_power

Syntax:

```
any_greater_power = { triggers... }
```

Scope:  

Switches scope to any country which is currently a greater power.

#### any_neighbor_country

Syntax:

```
any_neighbor_country = { triggers… }
```

Scope:  

Any country neighboring the current country.

#### any_owned_province

Syntax:	

```
any_owned_province = { triggers… }
```

Scope:  

Any owned province.

#### any_pop

Syntax:	

```
any_pop = { triggers… }
```

Scope:  

Any pop in the current country.

#### any_sphere_member

Syntax:

```
any_sphere_member = { triggers… }
```

Scope:  
 
Changes the current scope to any country in your sphere. Localisation is missing from vanilla.

#### any_state

Syntax:

```
any_state = { triggers… }
```

Scope:  
 
Changes the current scope to any owned region.

#### any_substate

Syntax:

```
any_substate = { triggers… }
```

Scope:  
 
Changes the current scope to any substate (not vassal).

#### capital_scope

Syntax:	

```
capital_scope = { triggers… }
```

Scope:  

Changes the current scope to the country’s capital (thus changing it to province scope).

#### [country tag]

Syntax:	

```
[tag] = { triggers… }
```

Scope:  

Changes the current scope to the specified country.

#### cultural_union

Syntax:	

```
cultural_union = { effects… }
```

Scope:  

Changes the current scope to the cultural union of the nation in the previous scope.

#### overlord

Syntax:

```
overlord = { triggers...}
```

Scope:  

Changes the scope for a vassal to its overlord country.

#### [region name]

Syntax:	

```
[region name] = { triggers… }
```

Scope:  

Changes the current scope to the specified region (the ones listed in map\regions.txt).

#### sphere_owner

Syntax:

```
sphere_owner = { triggers... }
```

Scope:  

Changes the current scope to the sphere owner of the country.

#### war_countries

Syntax:

```
war_countries = { triggers...}
```

Scope:  

Changes scope to all countries at war with the previously scoped country.

### Province Scope: Triggers

#### any_core

Syntax:

```
any_core = { triggers... }
```

Scope:  

Switches to the country scope of any cores inside the target province. So if the province has cores for Austria and Bohemia, then both those countries would now be in scope (whether they exist or not).

#### any_neighbor_province

Syntax:	

```
any_neighbor_province = { triggers… }
```

Scope:  

Any land province neighboring the current province. Note that this does not include empty provinces.

#### any_pop

Syntax:	

```
any_pop = { triggers… }
```

Scope:  

Any pop in the current province.

#### controller

Syntax:	

```
controller = { triggers … }
```

Scope:  

Changes the current scope to the province controller.

#### owner

Syntax:	

```
owner = { triggers … }
```

Scope:  

Changes the current scope to the owner of the province.

#### sea_zone

Syntax:

```
sea_zone = { triggers … }
```

Scope:  

Changes the current scope to every neighbouring sea proinces.

#### state_scope

Syntax:	

```
state_scope = { triggers … }
```

Scope:  

Changes the current scope to the state which the province is in.

### Pop Scope: Triggers

#### location

Syntax:	

```
location = { triggers … }
```

Scope:  

Changes the current scope to the province which the pop is in.

#### country

Syntax:	

```
country = { effects… }
```

Scope:  

Changes the current scope to the country this pop is part of.

#### cultural_union

Syntax:	

```
cultural_union = { effects… }
```

Scope:  

Changes the current scope to the cultural union of the nation in the previous scope.

### Country Scope: Effects

#### all_core

Syntax:

```
all_core = { effects... }
```

Scope:  

Changes the current scope to all provinces that are core to the current country (whether the country exists or not).

#### any_country

Syntax:	

```
any_country = { effects… }
```

Scope:  

Changes the current scope to all the currently available countries.

NOTE: This scope works differently in decisions and events. In decisions, it automatically refers to any existing countries (in fact, it cannot be used to target non-existing countries) and does not target the current country in scope. In events, it automatically refers to all country tags whether they currently exist or not (and would need a limit to specify otherwise), as well as the current country in scope.

#### any_greater_power

Syntax:

```
any_greater_power = { effects... }
```

Scope:  

Changes the current scope to all countries which are currently greater powers.

NOTE: For the tooltip, this handily does not display the text of the scope and its conditions but rather lists every greater power individually which would be affected. So, rather than printing "Any greater power that is... NOT.. etc. etc." it would list "Russia: {effect}", "Austria: {effect}" and so forth, whoever is covered by the scope. If you'd prefer to have the tooltip display all the conditions, you should use any_country instead and just include "is_greater_power = yes" in the triggers.

#### any_owned

Syntax:	

```
any_owned = { effects… }
```

Scope:  

Changes the current scope to every owned province.

#### any_neighbor_country

Syntax:	

```
any_neighbor_country = { effects… }
```

Scope:  

Changes the current scope to all the neighboring countries.

NOTE: For the tooltip, this handily does not display the text of the scope and its conditions but rather lists every country that would be affected. So, rather than printing "Any neighbor country that is... NOT.. etc. etc." it would list "Russia: {effect}", "Austria: {effect}" and so forth, whoever is covered by the scope. If you'd prefer to have the tooltip display all the conditions, you should use any_country instead and just include "neighbour = THIS" in the triggers.

#### any_state

Syntax:	

```
any_state = { effects… }
```

Scope:  

Changes the current scope to every owned state.

#### capital_scope

Syntax:	

```
capital_scope = { effects… }
```

Scope:  

Changes the current scope to the country’s capital.

#### [country tag]

Syntax:	

```
[tag] = { effects… }
```

Scope:  

Changes the current scope to the specified country.

#### cultural_union

Syntax:	

```
cultural_union = { effects… }
```

Scope:  

Changes the current scope to the cultural union of the nation in the previous scope.

#### from

Syntax:	

```
from = { effects… }
```

Scope:  

Changes the scope to the country that triggered the current event.

#### overlord

Syntax:

```
overlord = { triggers...}
```

Scope:  

Changes the scope for a vassal to its overlord country.

#### random_country

Syntax:

```
random_country = { effects... }
```

Scope:  

Changes the current scope to a random existing country.

#### random_owned

Syntax:	

```
random_owned = { effects… }
```

Scope:  

Changes the current scope to a random owned province.

#### random_pop

Syntax:	

```
random_pop = { triggers … }
```

Scope:  

Changes the current scope to a random pop in the country. Can be limited by location.

#### [region name]

Syntax:	

```
[region name] = { effects… }
```

Scope:  

Changes the current scope to the specified region.

#### sphere_owner

Syntax:

```
sphere_owner = { triggers... }
```

Scope:  

Changes the current scope to the sphere owner of the country.

### Province Scope: Effects

#### any_neighbor_province

Syntax:	

```
any_neighbor_province = { effects… }
```

Scope:  

Changes the current scope to every neighbouring land province.

#### country

Syntax:	

```
country = { effects… }
```

Scope:  

Changes the current scope to the country to which this province belongs.

#### cultural_union

Syntax:	

```
cultural_union = { effects… }
```

Scope:  

Changes the current scope to the cultural union of the nation in the previous scope.

#### owner

Syntax:	

```
owner = { effects… }
```

Scope:  

Changes the current scope to the country to which this province belongs. Same as *country* scope from a province but more consistent with its corresponding trigger.

#### [province ID]

Syntax:	

```
[province id] = { effects… }
```

Scope:  

Changes the current scope to the specified province.

#### random_neighbor_province

Syntax:	

```
random_neighbor_province = { effects… }
```

Scope:  

Changes the current scope to a random neighbour province.

#### random_empty_neighbor_province

Syntax:	

```
random_empty_neighbor_province = { effects… }
```

Scope:  

Changes the current scope to random, empty neighbour province.

#### sea_zone

Syntax:

```
sea_zone = { effects … }
```

Scope:  

Changes the current scope to every neighbouring sea proinces.

### See also

- [Modding overview](folder-file-overview.md)
- [Advanced events](event-modding.md)
- [List of conditions](list-of-conditions.md)
- Full list of effects
- [Modifier effects](modifier-effects.md)
