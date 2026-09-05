# How to make an event

Source: https://vic2.paradoxwikis.com/How_to_make_an_event

Events are in game messages that effect gameplay, by giving bonuses, penalties or change POP ideology.  

For all effects look see the full list of effects.
For all triggers look see the [full list of commands](list-of-conditions.md).
For all scopes look see the full list of scopes.

When making new events it is recommended to use a new file, for example "my events.txt" put it in the events map.  

When making an event it is very important to check the { and } this can be done through the C/C++ mode (see below).  

Notepad ++ and Ultraedit can show the text file in C/C++, this will show which { and } correspond.  

If you want to include notes for modding do it by a # (see step by step guides for usage).

### How does an event look?

```
(country/province)_event = {
	id = (event id)
	title = "(event title)"
	desc = "(event text)"
	picture = "(picture name)"

        #the four lines below are only needed if they are yes
	 
	is_triggered_only = (yes/no)        #only fired by another event or manually
	major = (yes/no)                    #major event has no picture example: great wars enabled
	fire_only_once = (yes/no)           #can only be fired once through triggers
	allow_multiple_instances = (yes/no) #Allows to fire several at once?

	trigger = { #what triggers the event
		(triggers)
	}
	
	mean_time_to_happen = {
		months = (months)
		
		modifier = {
			factor = (factor)
			(trigger)
		}
	}
	
	option = {
		name = "(option name)"
		(effect)
	}
}
```

example:

```
....
	option = {
		name = "(option name)"
		any_country = {
			limit = { money = 1000 }
			country_event = 1
		}
	}
....
country_event = {
	id = 1
....
	allow_multiple_instances = yes
....
	option = {
		name = "(option name)"
		money = -50
	}
}
```

If allow_multiple_instances = no only one country will get event 1, now that allow_multiple_instances = yes every country that has 1000 or more cash will get event 1.

If this is a bit overwhelming it may be handy to follow the guide below to make a new event.

### Step by step instruction

1. Think what you want as event, in this example I wanted to enslave non-accepted cultures.  

2. Open "my events.txt" (or whatever you name it)   

3. Copy a sample event, in this case the above.  

4. Country or province event? (country)

```
country_event = {
```

The following steps do not have to be done in this order.
5. Make the description. (long descriptions require a reference to localisation files)  

```
	id = 1 #make sure it is unused
	title = "Enslave Foreigners"
	desc = "Shall we enslave foreigners in our country?."
	picture = "NavioNegreiro" #slave picture
```

6. Make the triggers (see below).  

```
	fire_only_once = yes

	trigger = {
		slavery = yes_slavery
	}

	mean_time_to_happen = {
		months = 36 
	}
```

7. Make the effects.  

```
	option = {
		name = "Good Idea"
		any_pop = { #any POP in our country
			limit = { #which meets these conditions:
				is_primary_culture = no #not our own culture
				is_accepted_culture = no #not accepted culture
			}
			pop_type = slaves #become slaves
		}
		
	}
	option = {
		name = "No they remain free people!" #no effect
	}
```

8. (Very Important) Check the { and }. We are missing one } at the bottom, add it and the event will work. The event will look like this:  

```
country_event = {
	id = 1 #make sure it is unused
	title = "Enslave Foreigners"
	desc = "Shall we enslave foreigners in our country?."
	picture = "NavioNegreiro" #slave picture
	fire_only_once = yes

	trigger = {
		slavery = yes_slavery
	}

	mean_time_to_happen = {
		months = 36 
	}
	option = {
		name = "Good Idea"
		any_pop = { #any POP in our country
			limit = { #which meets these conditions:
				is_primary_culture = no #not our own culture
				is_accepted_culture = no #not accepted culture
			}
			pop_type = slaves #become slaves
		}
		
	}
	option = {
		name = "No they remain free people!" #no effect
	}
}
```
