# Governments.txt

Source: https://vic2.paradoxwikis.com/Governments.txt

This file contains the list of all possible government types. For each government, it lists allowed parties, if there are elections, if appointing ruling parties is allowed and the flag type. For example:

```
prussian_constitutionalism = {
	liberal = yes
	socialist = yes
	conservative = yes
	reactionary = yes
	
	election = yes
	duration = 48
	appoint_ruling_party = yes
	flagType = monarchy
}
```

```
	[ideology] = yes 
```

Lists the ideologies of the parties that are allowed to be appointed to power, if the government form allows appointment. **It has no effect in elections.**
'''

```
	elections = (yes/no)
```

Defines if the government form allows elections elections. Elections can happen by player action, the election effect, or regular elections, as follows. 

```
	duration = X
```

If set the duration is the number of months between the end of an election and the beginning of the next electoral campaign. Keep in mind that the election campaign itself takes 6 months.

```
	appoint_ruling_party = (yes/no)
```

This defines if the player (the AI never uses this) can change the ruling party manually.

```
	flagType = (monarchy/republic/fascist/communist/other)
```

Chooses the flag type for the government. If none is selected then the TAG.tga flag in gfx/flags is used. The other default flags are TAG_monarchy.tga, TAG_republic.tga, TAG_fascist.tga, TAG_communist.tga, but any can be added, as long as all countries have a TAG_other.tga file. Note that the flag choice here can be overridden by the country file in history/countries.

The starting government of each country can be set in the country history files.

### See Also

- Government types
- [How to make a country](creating-a-country.md)
