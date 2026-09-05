# Creating a country

Source: https://vic2.paradoxwikis.com/Creating_a_country

This guide will direct you through the process of creating a new country. The guide assumes that the culture of said nation already exists. If you want to create a whole new culture, check out [culture modding](culture-modding.md). The guide contains information for both countries that will be on the map upon starting a new game and countries who can be released by their current owner or formed through another country waging war on the owner with the wargoal "Free ____ in ____" This guide will make Byelorus a playable nation as an example.

### Finding the Files

The first step is to find the files you will be editing. They are in the Victoria 2 folder. Go to My Computer and access your C: Drive. Open up program files (or program files x86) If the game is bought on steam, it is under Steam --> steamapps --> Common --> Victoria 2 if you downloaded the game off of Steam, but if not it will be under the Paradox Interactive folder. It is strongly recommended that you make a back-up somewhere on you computer. Let's choose to edit the files in the Victoria 2 folder in program files. Rename the one on your desktop something that will let you know it is a backup. Open up the folder in the Paradox Interactive/Steamapps folder and begin.

### Summary

Minimum required to add country and ensure no crashes when loading the game:
- Victoria 2\common\countries.txt --#list of country tags to load into game
- Victoria 2\common\countries\country name.txt --#country parties and common names
- Victoria 2\history\countries\TAG - Country Name.txt --#country culture, govt, policies, techs
- Victoria 2\gfx\flags\TAG.tga --#don't forget TAG_monarchy, TAG_fascist, TAG_communist, and TAG_republic versions of your flag
- Victoria 2\history\provinces --#edit province txt files you want to own, console command "provid" can show province ID in game or [Provinces](provinces.md)

Additional changes:
- Victoria 2\history\units\TAG_oob.txt --#starting units
- Victoria 2\gfx\flags\flagfiles.txt --#also edit flagfiles_monarchy.txt, flagfiles_fascist.txt, flagfiles_communist.txt, and flagfiles_republic.txt
- Victoria 2\localisation\text.csv #localization file, use notepad to edit; if you use open office or notepad++, make sure you open and save it in ANSI encoding (also called Windows-1252)

### Creating the Country

#### Defining the tag

The country tag is a three letter acronym that the game uses to refer to a specific country. It is used in everything from national events to cores to the starting location of units. The convention is to use an acronym to easily remember it, but it can technically be anything.

In the Victoria 2 folder, find the folder named "common" and open it. First open the .txt file (NOT THE FOLDER) named "countries". It is advised to either find the category that the country you are trying to make best fits into or to create an entire new category just for your own nations. The placement of the line does not make a difference for the game files. It is only for your sake.

For Byelorus, let's go with # Eastern Europe. Create a new line somewhere in the block and type a three letter tag. The tag must be three upper case letters. It cannot be taken by another country (For example "Belarus" can't use BEL as that is already taken by [Belgium]).<ref>A tag can also not be a special word used in the game's code base, for example: `AND`, `LOG`, `NOT`, `GUI`, etc.</ref> Ctrl-F and type in the tag you chose to verify that your tag is not already taken. The tag "BYE" is not. Then hit the tab key twice and type following the format of the lines above: = "countries/Byelorus.txt" Save and close this document.
This makes the game now that the information of the tag BYE is defined is the byelorus.txt file.

#### The country file

Now go back and find the folder named countries. Inside will be .txt files of every playable country in the game. It is possible to create the file from the bottom but for your first attempt it is suggested to simply copy the country most similar to the one you aim to make and work from there. For Byelorus - let's go with Russia. 

##### The colour

The first line is the country's color - what shows up on the political map. 

```
color = { 47 91 18 }
```

It's in RGB format, if you are familiar with it. If not, the first number is red, the second green, and the third blue. The numbers are a scale of 0 to 255; 0 being devoid of that color, 255 being the highest amount. Play around until you find what you want, or copy the numbers from a "custom color selection" in MS Paint. 

##### Graphical culture

The second line is the Graphic culture. This defines the pictures and troops models used. 

```
graphical_culture = RussianGC
```

##### Political parties

The third section defines the political parties which will exist in the country. If they are not listed here, they will not exist.

```
party = {
	name = "RUS_conservative"
	start_date = 1830.1.1
	end_date = 1905.1.1

	ideology = conservative

	economic_policy = interventionism
	trade_policy = protectionism
	religious_policy = moralism
	citizenship_policy = residency
	war_policy = jingoism
}
```

The name refers to a line in the [localisation](localisation.md) files. The name can be changed alternatively be changed by editing the names directly in the countries.txt file. 

```
name = "Belarussian Nationalist Party"
```

Lastly it is actually also possible to refer to the name of another country's party by choosing a tag and adobt that nations parties. E.g. one can adopt Chiles parties if one makes a Spanish nation. This only adopts the name, they are still two separate entities.

If you want more parties with the same ideology they are commonly called "RUS_liberal_2"

#### The country's history file

Now go into the "history" folder and find the files named TAG - Name e.g. RUS - Russia. These files deals with the conditions for the country at the start of the game. By default they are used for the 1836 scenario. If you want a specific thing to be different in the 1861 scenario, this has to be specified. When not specifiec, the conditions are inherited from the 1836 scenario. Again you can build your own or copy of another one and rename it to BYE - Byelorus. 

##### Capital

The first line defines the capital.

```
capital = 994
```

The number refers to a file in the history - provinces map. The information on any province can be found in the victoria2/history/province folder. Each province is saved as a file under the corresponding province number.

Look up the province number for the province you want to be the capital of your country. For Byelorus we can use Minsk, which is 718.

##### Cultures

```
primary_culture = russian
culture = byelorussian
culture = ukrainian
```

Next section defines the primary and secondary cultures. The words are always lowercase and refers to the entities in the [cultures.txt](culture-modding.md) file. There must be one and only one primary culture, but you can have as many or as few accepted cultures as your want. If you want no additional accepted cultures, the line can be omitted. One can also add by writing culture = [name]. Let's go with byelorussian as primary and Russian as secondary.

##### Religion

```
religion = orthodox
```

This defines the national religion. The text must be lower case. It refers to one of the 14 religions defined in the [religion.txt](religion-modding.md) document.

##### Government form

- *See Also: [Governments.txt](governments-txt.md)*

```
government = absolute_monarchy
```

This defines the starting government form. This has little to no effect, if the country doesn't start the game as independent.

##### Plurality

```
plurality = 25
```

This defines the starting plurality of the country. The scale goes from 0 to 100.

##### National Value

- *See also: [National value modding](national-value-modding.md)*

```
nationalvalue = nv_order
```

This defines which of the three national values the country will have; Liberty, Order or Equality as they are defined in the [nationalvalues.txt](national-value-modding.md) file. Simply put in the one you find most fitting.

##### Literacy

Under national value you will find literacy.

```
literacy = 0.10
non_state_culture_literacy = 0.03
```

This is a scale from 0.01 to 1.0 interpreted as a percentage. It can be a little tricky to mess with, because it overlaps with information from the provinces files as well as other countries.
Non state culture literacy refers to the literacy of non-accepted Pops. It is not required, if you do not want it to be different from the main culture.

##### Rank, prestige and status

There can potentially be a line defining status and/or if the country is civilized or not. 

```
civilized = yes
```

If omitted it will default to no.

```
prestige = 80
```

This defines the starting prestige of the country. There are no upper limit, and it has no effect if the country doesn't exist at the start of the game.
If you are in doubt about which value to put, you can compare with a similar country.
For Belarus we can match Denmark as an example and go with 5.

##### Reforms

###### Political and Social Reforms

The next block defines the starting reforms of the country. This also has effect when the country is released peacefully. If ommitted it will default to the most regressive type of reform.

```
# Political reforms
slavery = no_slavery
upper_house_composition = appointed
vote_franschise = none_voting
public_meetings = yes_meeting
press_rights = state_press
trade_unions = no_trade_unions
voting_system = first_past_the_post
political_parties = underground_parties

# Social Reforms
wage_reform = no_minimum_wage
work_hours = no_work_hour_limit
safety_regulations = no_safety
health_care = no_health_care
unemployment_subsidies = no_subsidies
pensions = no_pensions 
school_reforms = no_schools
```

It is important to get the spelling and underscores absolutely correct. 
If you want to change it, it is advised to copy a line or two from another country which has the reforms, you want.
The titles '# political reforms' and '# social reforms' are only comments and does not strictly have an effect. It is suggested to keep them though for your own overview's sake.

###### Westernization reforms

Westernization reforms can also be added for uncivilized nations.

```
foreign_training = yes_foreign_training
foreign_weapons = yes_foreign_weapons
land_reform = yes_land_reform
```

As it defaults to no reform, if you do not want your country to start with a certain reform, you do not have to add anything. For already westernized countries these lines will have no effect.

##### Starting political situation

```
ruling_party = RUS_conservative
upper_house = {
	fascist = 0
	liberal = 19
	conservative = 60
	reactionary = 21
	anarcho_liberal = 0
	socialist = 0
	communist = 0
}
```

The first line defines which party is in power at the start of the game. It refers to the parties, you have already created in the country file.

The second line sets the starting upper house. The scale is a percentage from 0.0 to 100. Make sure to only use integers (numbers without decimals) and that it adds up to 100.

##### Technologies and inventions

The next block can look overwhelming, but it actually fairly simple.

```
# Technologies
post_napoleonic_thought = 1
flintlock_rifles = 1
bronze_muzzle_loaded_artillery = 1
military_staff_system = 1
army_command_principle = 1
post_nelsonian_thought = 1
clipper_design = 1
naval_design_bureaus = 1
alphabetic_flag_signaling = 1
the_command_principle = 1
classicism_n_early_romanticism = 1
late_enlightenment_philosophy = 1
malthusian_thought = 1
enlightenment_thought = 1
introspectionism = 1
private_banks = 1
no_standard = 1
early_classical_theory_and_critique = 1
guild_based_production = 1
water_wheel_power = 1
publishing_industry = 1
mechanized_mining = 1
basic_chemistry = 1

#Inventions
#corvettes = yes
commerce_raiders = yes
```

Both inventions and technologies is a [boolean value](https://en.wikipedia.org/wiki/Boolean_data_type). Meaning it has to be either 0 or 1 and yes or no. You can simply see '1' as a yes and '0' as a no.
Each line refer to either a technology or an invention. If the value is either 1 or yes, the country will start with said tech/invention. If you don't want a certain tech to be researched you don't have to put anything, as the boolean value defaults to 0/no.

This does not have any effect, if the country doesn't exists at game start.<ref>If you look at e.g. Irelands file, you will notice the information simply isn't there</ref>

##### Consciousness

```
# Starting Consciousness
consciousness = 3
nonstate_consciousness = 1
```

This defines the starting consciousness. First line is in all integrated states and the second line is in colonies.

##### Tech School

```
schools = culture_tech_school
```

This defines the starting tech school. If the country is not independent at the start of the game, it has no effect and can be omitted.

##### OOB

The OOB (Order of Battle) defines the placement of troops, relations, influence among other things. The actual values we will get to later. Here we will simply refer to the correct file.

```
oob = "RUS_oob.txt"
1861.1.1 = {
	oob = "/1861/RUS_oob.txt"
```

There are one for each of the two start dates in the game. If the country is not independent at the start of the game, it has no effect and can be omitted.
Change the RUS to BYE. If you don't Byelorus will start with the same amount of troops in the same places as Russia! Save and close this document.

### Bringing your Country into Existence

Now comes the fun part. Making your country exist! Go into the history folder again and open up the province folder. Find the category your country falls in, Byelorus would be in Soviet. The search bar works well if you want a specific province e.g. Minsk. It is recommended that you keep a list of Province ID's nearby for this. A complete list can be found here: [Provinces](provinces.md).

#### The provinces files

- *Main article: [province history modding](province-history-modding.md)*
Find any province that you want Byelorus to control at the start of the game or potentially own upon being released by Russia or have cores for. (Byelorus' modern day borders are 936 to 939 - but you can modify them however you like. Let's go with 936 - Grodno.

```
owner = RUS
controller = RUS
add_core = RUS
add_core = POL
add_core = PLC
add_core = BYE
```
 
Owner defines who owns the province at the start of the game. Controller defines who has occupied it. If the two tags are the same, the province will start unoccupied. This is only really relevant if you want to start with your country at war or fighting rebels.
The "add_core =" adds the specified tag as a core.
For Belarus we can add "add_core = BYE". Byelorus now has a core in Grodno. If you want Byelorus to be simply releasable by Russia, this is enough. If you want it to exist on the starting map of the grand campaign, then change the owner and controller from RUS to BYE. Save and close the document and move to the next one. Repeat. Congrats, using this information you should now be able to modify borders at the game start and add cores to provinces! Woo!

The controller, owner and cores can be set completely independently of each other - you can own a province you don't have a core on and vice versa.

Unfortunately each province is stored as a separate file, so for especially large countries this can take a while. Luckily, provinces that border each other tend to have numbers next to each other. So a good bet is that all the provinces you are looking for are the same place.

Like with the country history file, if you want the cores or ownership to be different in the 1861 scenario, this has to be specified. When not specified, the conditions are inherited from the 1836 scenario.

#### OOB

##### Sphere of Influence and relations

- *Main article: [Sphere modding](sphere-modding.md)*
If you want your country to start with certain relations with another nations, a level of influence or in a sphere it has to be editted in the OOB-file. Liek previously mentioned, you have in the country - history file created the link to a certain file, you will have to create.

```
SWE = {

	value = 125
	level = 3 	
	influence_value = 40
```

<sup>This example is Russias starting relations with Sweden</sup>

The TAG is of course the country being sphered (the sphere leader is defined by the file it self).
Value refers to the relation. It can be set to any value between -200 and 200.
Level refers to the 6 different levels of influence (In Sphere, Friendly, Cordial, Neutral, Opposed, Hostile). 5 is in a sphere while 0 is hostile.
Influence_value refers to any additional influence. It goes on a scale from 0 to 100.
If you do not put any values for a country it will default to 0 relation, 0 influence and neutral influence level.

If you want your new country to start in the sphere of influence of another country, you will have to found their particular oob.file.
Maybe you find it realistic, that Byelorus is in the sphere of influence of Russia at the start of the game. To do this, go in the history folder again and then in the folder units. Find the file named RUS_oob.txt. In this file you can find all starting influence of a country.

##### Leaders

The next section defines which/if the country starts with any leaders. Each seperate block is a single leader

```
leader = {
	name = "Prince Vasilchikov"
	date = 1801.1.1
	type = land
	personality = competent
	background = powerful_friends
	prestige = 0.4
}
```

type (land/sea) defines the leader as a general or admiral.
Personality and background refers to the values defined in the traits.txt document.

If you want your country to start without any leaders, simply do not have this section.

##### Starting troops

If you want, you also can create starting troops for Byelorus. To create them, copy the RUS_oob.txt file and rename it to BYE_oob.txt. 

```
regiment = {
		name= "2.1-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 946
	}

	regiment = {
		name= "3.1-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 1006
	}

	regiment = {
		name= "1.2-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 1008
	}

	regiment = {
		name= "2.2-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 343
	}

	regiment = {
		name= "3.2-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = artillery
		home = 718
	}

	regiment = {
		name= "1.3-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 360
	}

	regiment = {
		name= "2.3-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 994
	}

	regiment = {
		name= "3.3-ya Gvardeiskaya Pekhotnaya Diviziya"
		type = infantry
		home = 1012
	}

}
```

"army" (or "navy") means, that the following troops form an army. Any army have a name and a starting location.<ref>Navies do not have home as they are not recruited from Soldier Pops</ref> 
Then follow a lot of regiments (every regiment means a troop) with a name, a type and a home. Home is which province the soldiers has been recruited from(remember: To recruite a unit, you need soldiers POPs).

### Getting a Flag

- *Main article: [Flag modding](flag-modding.md)*
Flags are in the folder "flags" which is in the "gfx" folder. The maximum flag dimensions that the Victoria 2 engine can cache and render is 128x64. The flag must also be saved in .tga format. You need a program to do this, I recommend paint.net. Install the program and create a new document with the dimensions above. Now pick out a flag for Byelorus, I went with the white red white horizontal tricolor. Find an image on the internet and copy paste it into the program. Resize the image so it entirely fits in the canvas, do not resize the canvas to match the image. Now save it as a .tga with the name BYE. If you want to make different flags for different government types, you can! For the communist Byelorus, why not pick out the flag of the Byelorussian SSR and use that? Simply save it as BYE_communist with the correct dimensions and format! Move the .tga files to the flags folder and just leave them there.

One has to make one BYE, one BYE_communist, one BYE_fascist, one BYE_republic and one BYE_monarchy. No more no less. If one forgets one, the game will fail to load.

### Making your Country... Presentable

- *See also: [Localisation](localisation.md)*
If you were to load up Victoria 2 right now, your country would be fully accessible. However, the name of your country would be whatever you made the tag. If it was releasable, you do have the option to release Byelorus, however the name will be BYE. Also, look at the region of Brest or Lida. Because it is split between Russian Brest and BYE_ADJ Brest. 

#### Localisation

Search the localisation folder for a file named "text.csv" and open it. It's comma delimited so make sure to maintain all formatting. 

Ctrl-F and type in any tag you know to find the section where country names are defined. Insert a new line and copy/paste another so you don't have to meticulously type in semicolon formatting. The format (in Notepad) is as follows:

`tag;name(English);name(French);name(German);;name(Spanish);;;;;;;;;x;`

Let's enter in:

`BYE;Byelorus;Byelorussie;Weissrusland;;Bielorrusia;;;;;;;;;x;`

If you are lazy and know that you will not ever use the game in French, German or Spanish one can just let the names stay, from the country you copied from. You don't have to get the foreign names correct. 

Now Ctrl-F again to find where you see the list of countries names with _ADJ following them. This is where the adjective for countries shows up. Follow the instructions listed above to modify a line for Byelorussian. And once you save this file, the game is completely playable without looking ugly. There is more you can do, but that is beyond this guide.
`tag_ADJ;name(English);name(French);name(German);;name(Spanish);;;;;;;;;x;`

#### Flavour

Now the country is actually finished. Congratulations.
There can still be added flavour with either [event modding](event-modding.md) or [decision modding](how-to-make-a-decision.md). Or various diplomatic pacts could be added in the history files.

### Bug-fixing

#### If your game fails to load

Pay attention to when to game stops loading and the error message.

If the game stops while loading flags, you are missing a flag file. Every single country needs exactly 5 flag files: one [TAG], one [TAG]_communist, one [TAG]_fascist, one [TAG]_republic and one [TAG]_monarchy. No more no less. If just one of them for any country is missing, the game will fail to load.

If the game stop loading and gives an error box saying "failed to load line 528 "common/countries/[name ... ... ENG" you have made a mistake in the countries.txt file. Usually one of the " " marks is missing and the game files thinks the next country's tag is a part of the name. Example:

```
ENG		= "countries/United Kingdom.txt
```

#### If the in-game text is messed up

If the in-game text is wrongly placed, you may have made a misclick in the [localisation](localisation.md) files (the one with all the country names and country adjectives). Find a backup and replace with the original. It is way faster than looking for your mistake, as the file is huge.

If the game becomes unplayable, and there is not an easy fix or backup, you can always reinstall the game.

### Notes

<references />
