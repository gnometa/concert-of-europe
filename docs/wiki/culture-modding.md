# Culture modding

Source: https://vic2.paradoxwikis.com/Culture_modding

This guide will direct you through the process of creating a new culture or to edit an already existing culture.

### Finding the Files

The first step is to find the files you will be editing. They are in the Victoria 2 folder. Go to My Computer and access your C: Drive. Open up program files (or program files x86) If the game is bought on steam, it is under Steam --> steamapps --> Common --> Victoria 2 --> Common if you downloaded the game off of Steam, but if not it will be under the Paradox Interactive folder. It is strongly recommended that you make a back-up somewhere on you computer. Let's choose to edit the files in the Victoria 2 folder in program files. Rename the one on your desktop something that will let you know it is a backup. Open up the folder in the Paradox Interactive/Steamapps folder and begin.

Here you need the cultures.txt file.

### The cultures.txt file

Each culture is arranged in culture groups. For example North German, South German and Aszhkenazi is in the Germanic group. They have a few things in common like the nation formed by decisions and some graphical features.
Example:

```
germanic = {
	leader = european
	unit = EuropeanGC
    union = GER
```

The two first lines determine the pictures used for leaders and the units sprites on the map. Union defines which formable country is the correct if applicable. This is mainly used when a country is formed by rebels.<ref>The union line is typically placed under each of the individual culture blocks, but it is still part of the culture group statements</ref>

Here is the default list of possible leader portraits:
- european
- southamerican
- russian
- arab
- asian
- indian
- african
- polar_bear<ref>only used by Jan Mayen and considered an Easter Egg</ref>

Here is the default list of possible unit models:
- EuropeanGC
- BritishGC
- ItalianGC
- SpanishGC
- FrenchGC
- AustriaHungaryGC
- RussianGC
- MiddleEasternGC
- IndianGC
- AsianGC
- ChineseGC
- AfricanGC
- ZuluGC

Within each culture group there are blocks for each separate culture. Example:

```
north_german = { 
		color = { 90 60 60 }
		first_names = { Adelbert Adolf Albrecht Alexander Alfred August Bernhard Burkhard Dieter }
		
		last_names = { Behncke Brommy Cordemann Dreyer Droste Groener "Herwarth von Bittenfeld" Heppendorf Hoffmann Krohn }
	}
```

<ref>Most names have been removed for ease of reading</ref>

The color determines which colour is used in pie charts and such. It is in RGB format, if you are familiar with it. If not, the first number is red, the second green, and the third blue. The numbers are a scale of 0 to 255; 0 being devoid of that color, 255 being the highest amount. Play around until you find what you want, or copy the numbers from a "custom color selection" in MS Paint. 

First names and last names determines the names that leaders can take. There has to be at least 1 example in each, but there can be as many as you like. Most cultures have around 50 first names and 50 last names.

### Finishing steps

- *Main article: [Population modding](population-modding.md)*
This is strictly speaking all that is needed to create a culture. To create a nation for your new culture look at [Creating a country](creating-a-country.md). To add your culture to the map go to the folder Victoria2 --> history --> Pops. Here is defined the sizes and types of each POP at the start of the game.
Each file is a country and it can be a little tricky to find exactly which province is in which file.

The files look like this:

```
1470 = {
	aristocrats = {
		culture = beifaren
		religion = mahayana
		size = 22000
	}

	bureaucrats = {
		culture = beifaren
		religion = mahayana
		size = 10750
	}
```
<ref>most POPs has been removed for ease of reading</ref>

1470 determines the province, Anqing in this example. For each province, the pops are aranged by pop types. Size is the amount of Pops. Culture determines the culture, and it is here you should put your new culture. Religion of course determines the religion of said pop. 

Here you have to add all the POPs you want to have with your new culture. If you are doing this for the first time, it might be a good idea to find a comparable example to have an idea of an appropriate scale.

Remember to also edit the 1861 bookmark, if you ever want use it. 

### Notes

<references />
