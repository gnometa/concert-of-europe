# Event modding

Source: https://vic2.paradoxwikis.com/Event_modding

This page will show how to create more advanced events, it is recommend to learn the [basics](how-to-make-an-event.md) first.

### Using [Boolean](list-of-conditions.md) Combinations

Boolean commands are at their finest when combined with other Boolean commands. Consider the following:

```
OR = {
	tag = GER
	AND = {
		culture = north_german
		NOT = {
			continent = europe
		}
	}
}
```

This complex-looking string is actually quite simple. 
- We begin with the "or" command, which is the root command, stating that it will be satisfied if any one of the listed commands in its tier are satisfied.
- We then have a simple "tag = " command, which simply checks if the country in question matches its own.
- Now we have an "and" command, which demands that all of the commands listed in its tier be satisfied before it returns true.
- Contained within this "and" command is a "culture = " command, this time demanding the primary culture of the country in question be North German.
- Then, we have a "not" command, which demands that the country in question not be in Europe; that is, it must be on some other continent.

From all of this information, we can derive the meaning of this command. The command will return true if:
- The country in question is Germany
 OR
- The country in question has North German as its primary culture and resides outside of the European continent

Using these Boolean commands, one could create immensely complex sets of requirements for events, decisions, and limits. Enjoy them, but be wary of creating scenarios so specific they will never be satisfied!

### Using Flags

Flags can be used to select certain countries, but can also be used to say whether something has happened.
A flag has no direct effect on the game, however it can have indirect effects, through other events.
The following commands can be used for flags.

**The flag effects:**

```
set_country_flag = (name)
```

Sets country flag (name).  

```
set_global_flag = (name)
```

Sets global flag (name).  

```
clr_country_flag = (name)
```

Removes country flag (name).  

```
clr_global_flag = (name)
```

Removes global flag (name).

**The flag triggers:**

```
has_country_flag = (name)
```

Returns true if the country has (name).  

```
has_global_flag = (name)
```

Returns true if (name) is a global flag.

### Using Scopes

Scopes are a way to switch the target between:
- countries
- [Provinces](provinces.md)
- POPs

They can be used for example if a province event depends (partly or entirely) on the country that owns the province.
Or if a POP is affected by a country event.

### Using Variables

Variables are simple numbers that work like flags, so they do not directly influence the game, but through other events.

**The variables effects:**

```
set_variable = { 
	which = (name)
	value = n
}
```

Sets (name) to n.  

```
change_variable = {
	which = (name)
	value = n
}
```

Adds n to (name).

**The variables triggers:**

```
check_variable = {
	which = "name"
	value = n
}
```

Returns true if (name) is more than n.  

```
NOT = {
	check_variable = {
		which = "name"
		value = n
	}
}
```

Returns true if (name) is less than n.  

The code above works fine for values that are above or below n, but to trigger when (name) ≈ n both codes are needed (see below).  

```
check_variable = {
	which = "name"
	value = (n-0.01)
}
NOT = {
	check_variable = {
		which = "(name)"
		value = (n+0.01)
	}
}
```

Returns true if (name) ≈ n.

### Mean Time To Happen

#### How to make an event fire randomly

If you want to make events happen randomly, you'll have to remove the line called 
```
 is_triggered_only = yes 
```
```
From now on the event will be happening randomly, instead of having to be fired using on_actions, decisions or other events. 
```

First, an event that can only be triggered by decisions:

```
country_event = {
	id = (id)

	trigger = {
		(trigger)
	}

	title = (title)
	desc = (desc)
	picture = (picture)

        is_triggered_only = yes

	option = {
		name = (name)
		(effect)
	}
}
```

And here is one that can happen randomly, note that the only_if_triggered line is gone:

```
country_event = {
	id = (id)

	trigger = {
		(trigger)
	}

	title = (title)
	desc = (desc)
	picture = (picture)

	option = {
		name = (name)
		(effect)
	}
}
```

#### Mean Time To Happen

This also brings a problem, because now the event will fire once every month, which is not what you want. To fix this problem you should use 'Mean Time To Happen'. This basically says over what time period the event will have a 50% chance of firing. If you want the event to only fire in a average of around every ten years, you can use this line of code:

```
mean_time_to_happen =  {
	months = 60
}
```

After the line is implemented (make sure the location you put it isn't inside the space of the trigger or one of the options).

This one will work:

```
country_event = {
	id = (id)

	trigger = {
		(trigger)
	}

        mean_time_to_happen  {
	        months = 12
        }

	title = (title)
	desc = (desc)
	picture = (picture)

	option = {
		name = (name)
		(effect)
	}
}
```

This one won't work, note that the line is put inside the option instead of directly in the event:

```
country_event = {
	id = (id)

	trigger = {
		(trigger)
	}

	title = (title)
	desc = (desc)
	picture = (picture)

	option = {
                mean_time_to_happen  {
	                months = 12
                }
		name = (name)
		(effect)
	}
}
```

This one will fire every month because there isn't a mean time to happen and there it isn't triggered:

```
country_event = {
	id = (id)

	trigger = {
		(trigger)
	}

	title = (title)
	desc = (desc)
	picture = (picture)

	option = {
		name = (name)
		(effect)
	}
}
```

### Using a series of events

For large scaled events involving multiple countries it may be necessary to create a [series of events](event.md).
In such a serie one event will trigger other events either directly (triggered_only = yes and country_event = <event id>) or indirectly (using variables, flags or modifiers).
The Rock-Paper-Scissors is an example of an event serie.

### Examples

#### Flag/Event Serie example: Rock-Paper-Scissors (RPS)

This example will show how flags can be used in an event serie to play RPS.  

It is not a single event, but an event serie, each linked to another (see picture).  

It requires a starting event (1) which has no trigger, so it must be triggered by another event or manually.  

The game requires 2 players:
- player 1=ORGIN
- player 2=TAG
TAG is the country that receives event 1 (the start).  

ORGIN is the country chosen in event 1, either a country with flag ORGIN or a random country.  

<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">
**RPS events**
<div class="mw-collapsible-content">

```
country_event = {
	id = 1
	title = "Rock Paper Scissors"
	desc = "Ready to play?"
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Yes, against ORGIN."
		any_country = {
			limit = { has_country_flag = orgin }
			country_event = 2
		}
	}
	option = {
		name = "Yes, against a random country."
		random_country = {
			country_event = 2
		}
	}
	option = {
		name = "Set Flag ORGIN"
		any_country = {
			limit = { has_country_flag = orgin }
			clr_country_flag = orgin
		}
		set_country_flag = orgin
	}
	option = {
		name = "Remove Flag"
		any_country = {
			limit = { has_country_flag = orgin }
			clr_country_flag = orgin
		}
	}
	option = {
		name = "No"
		ai_chance = { factor = 100 }
	}
}
country_event = { #ORGIN player 1
	id = 2
	title = "$COUNTRY$ vs $FROMCOUNTRY$ (ORGIN)"
	desc = "$COUNTRY$ is playing. Make your choice. The first option is Rock, the second is Paper and the third is Scissors"
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "An Option"
		set_country_flag = rock_1
		FROM = {
			country_event = 3
			set_country_flag = rock_1
		}
		ai_chance = { factor = 34 }
	}
	option = {
		name = "An Option"
		set_country_flag = paper_1
		FROM = {
			country_event = 3
			set_country_flag = paper_1
		}
		ai_chance = { factor = 33 }
	}
	option = {
		name = "An Option"
		set_country_flag = scissors_1
		FROM = {
			country_event = 3
			set_country_flag = scissors_1
		}
		ai_chance = { factor = 33 }
	}
}
country_event = { #TAG player 2
	id = 3
	title = "$COUNTRY$ vs $FROMCOUNTRY$"
	desc = "$COUNTRY$ is playing. Make your choice. The first option is Rock, the second is Paper and the third is Scissors"
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "An Option"
		set_country_flag = rock_2
		FROM = {
			country_event = 4
			set_country_flag = rock_2
		}
		ai_chance = { factor = 34 }
	}
	option = {
		name = "An Option"
		set_country_flag = paper_2
		FROM = {
			country_event = 4
			set_country_flag = paper_2
		}
		ai_chance = { factor = 33 }
	}
	option = {
		name = "An Option"
		set_country_flag = scissors_2
		FROM = {
			country_event = 4
			set_country_flag = scissors_2
		}
		ai_chance = { factor = 33 }
	}
}
country_event = { #ORGIN player 1
	id = 4
	title = "$COUNTRY$ vs $FROMCOUNTRY$"
	desc = "Both $COUNTRY$ and $FROMCOUNTRY$ have made their choice now its time for the outcome."
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Tell our opponent."
		any_country = { #TAG player 2
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_2
						has_country_flag = paper_1
					}
					AND = {
						has_country_flag = paper_2
						has_country_flag = scissors_1
					}
					AND = {
						has_country_flag = scissors_2
						has_country_flag = rock_1
					}
				}
			}
			country_event = 5
			country_event = 6 #Lost
		}
		any_country = {
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_2
						has_country_flag = scissors_1
					}
					AND = {
						has_country_flag = paper_2
						has_country_flag = rock_1
					}
					AND = {
						has_country_flag = scissors_2
						has_country_flag = paper_1
					}
				}
			}
			country_event = 5
			country_event = 7 #Won
		}
		any_country = {
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_1
						has_country_flag = rock_2
					}
					AND = {
						has_country_flag = paper_1
						has_country_flag = paper_2
					}
					AND = {
						has_country_flag = scissors_1
						has_country_flag = scissors_2
					}
				}
			}
			country_event = 5
			country_event = 8 #Tie
		}
	}
}
country_event = { #TAG player 2
	id = 5
	title = "$COUNTRY$ vs $FROMCOUNTRY$"
	desc = "Both $COUNTRY$ and $FROMCOUNTRY$ have made their choice now its time for the outcome."
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Tell our opponent."
		any_country = { #ORGIN player 1
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_2
						has_country_flag = scissors_1
					}
					AND = {
						has_country_flag = paper_2
						has_country_flag = rock_1
					}
					AND = {
						has_country_flag = scissors_2
						has_country_flag = paper_1
					}
				}
			}
			country_event = 6 #Lost
		}
		any_country = {
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_2
						has_country_flag = paper_1
					}
					AND = {
						has_country_flag = paper_2
						has_country_flag = scissors_1
					}
					AND = {
						has_country_flag = scissors_2
						has_country_flag = rock_1
					}
				}
			}
			country_event = 7 #Won
		}
		any_country = {
			limit = { 
				OR = {
					AND = {
						has_country_flag = rock_1
						has_country_flag = rock_2
					}
					AND = {
						has_country_flag = paper_1
						has_country_flag = paper_2
					}
					AND = {
						has_country_flag = scissors_1
						has_country_flag = scissors_2
					}
				}
			}
			country_event = 8 #Tie
		}
	}
}
country_event = {
	id = 6
	title = "$COUNTRY$ Lost from $FROMCOUNTRY$"
	desc = "Better luck next time."
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Ah"
		clr_country_flag = rock_1
		clr_country_flag = rock_2
		clr_country_flag = paper_1
		clr_country_flag = paper_2
		clr_country_flag = scissors_1
		clr_country_flag = scissors_2
		money = -500 #price money
	}
}
country_event = {
	id = 7
	title = "$COUNTRY$ Won of $FROMCOUNTRY$"
	desc = "Well done."
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Yeah"
		clr_country_flag = rock_1
		clr_country_flag = rock_2
		clr_country_flag = paper_1
		clr_country_flag = paper_2
		clr_country_flag = scissors_1
		clr_country_flag = scissors_2
		money = 500 #price money
	}
}
country_event = {
	id = 8
	title = "Tie!"
	desc = "No winner, no loser."
	picture = "meeting3"

	is_triggered_only = yes

	option = {
		name = "Fine"
		clr_country_flag = rock_1
		clr_country_flag = rock_2
		clr_country_flag = paper_1
		clr_country_flag = paper_2
		clr_country_flag = scissors_1
		clr_country_flag = scissors_2
	}
}
```
</div></div>

### See also

- [Modding overview](folder-file-overview.md)
- [Full list of conditions](list-of-conditions.md)
- Full list of effects
- [Modifier effects](modifier-effects.md)
