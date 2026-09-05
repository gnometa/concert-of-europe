# How to make a decision

Source: https://vic2.paradoxwikis.com/How_to_make_a_decision

Unlike [event](event.md)s, which are usually outside the player's control, [decision](decision.md)s can be taken directly by the player (and any AI country). They can have a variety of effects, from adding or removing modifiers for single provinces to unifying countries and changing international politics. This article is an introduction into the basics of decision modding.

### Basics

Before creating an event you should familiarize yourself with [scopes](list-of-scopes.md), [conditions](list-of-conditions.md) and [effects](list-of-effects.md).

A decision typically has these blocks:
- `potential`: The conditions for the decisions being visible.
- `allow`: The conditions for taking the decision.
- `effect`: What the decision does.
- `ai_will_do`: Instructions for the AI.

In each of these blocks scopes, conditions and effects are then used to define the decision.

### Example from the Game

<div class="mw-collapsible mw-collapsed">One of the most famous decisions in Victoria 2 is probably the German unification decision "Three Hurrahs For Germany!" (expand on the right):
<pre class="mw-collapsible-content">form_germany = {
	news = yes
	news_desc_long = "form_germany_NEWS_LONG"
	news_desc_medium = "form_germany_NEWS_MEDIUM"
	news_desc_short = "form_germany_NEWS_SHORT"
	potential = {
		is_culture_group = germanic
		NOT = {
			exists = GER
			tag = ISR
		}
	}
	allow = {
		is_greater_power = yes
		prestige = 45
		war = no
		GER = {
			all_core = {
				OR = {
					owned_by = THIS
					owner = {
						in_sphere = THIS
					}
				}
			}
		}
	}
	effect = {
		prestige = 20
		change_tag = GER
		add_accepted_culture = north_german
		add_accepted_culture = south_german
		any_country = {
			limit = {
				is_culture_group = germanic
				in_sphere = THIS
			}
			country_event = { id=11101 days=0 }
		}
	}
	ai_will_do = {
		factor = 1
	}
}</pre></div>

To better understand the decision, it can be broken down into smaller parts:

#### Start

```
form_germany = {
	news = yes
	news_desc_long = "form_germany_NEWS_LONG"
	news_desc_medium = "form_germany_NEWS_MEDIUM"
	news_desc_short = "form_germany_NEWS_SHORT"
```

This names the decision and in this case also gives information for generating a newspaper article, since this is an internationally important decision.

#### Potential

```
	potential = {
		is_culture_group = germanic
		NOT = {
			exists = GER
			tag = ISR
		}
	}
```

The decision is visible in the menu when:
- The country's primary culture is in the Germanic group (which includes North German, South German and Ashkenazi).
- Germany doesn't already exist, and the country isn't Israel (thus Ashkenazi is excluded).

#### Allow

```
	allow = {
		is_greater_power = yes
		prestige = 45
		war = no
		GER = {
			all_core = {
				OR = {
					owned_by = THIS
					owner = {
						in_sphere = THIS
					}
				}
			}
		}
	}
```

If the `potential` check is successful, a country can take the decision under the following conditions:
- It is a Great Power.
- It has at least 45 prestige.
- It isn't at war.
- For the country with tag `GER` (Germany):
  - All core provinces of `GER` are either
    - owned by the country taking the decision (`THIS`) **OR**
    - the owner is in the sphere of `THIS`

#### Effect

```
	effect = {
		prestige = 20
		change_tag = GER
		add_accepted_culture = north_german
		add_accepted_culture = south_german
		any_country = {
			limit = {
				is_culture_group = germanic
				in_sphere = THIS
			}
			country_event = { id=11101 days=0 }
		}
	}
```

If `THIS` now takes the decision the following happens:
- It gains 20 prestige.
- Its tag changes to Germany.
- North German and South German are added as accepted cultures.
- Any country that
  - the following conditions are true for:
    - The primary culture is in the Germanic group.
    - It is in the sphere of `THIS`.
  - instantly (0 days after the decision) gets the event with ID 11101, which gives a choice between being peacefully annexed by `THIS` and refusing annexation (AI countries will always choose annexation).

### Creating a Custom Decision

For this example we will make custom decision to annex Tibet as China.

First we should think about what this decision is about and how we could achieve that. It should
- annex Tibet
- give China cores on Tibet
- give China some Infamy
- give China a small amount of prestige
- anger any Tibetans in China

We should also consider the conditions for the decision:
- Visible when
  - The country is China
  - China is Westernized
  - Tibet still exists
- Can be taken when
  - China is a Great Power
  - China isn't at war
  - Tibet is a vassal of China

#### Start

The decision should have a unique name, ideally with some sort of ID in it to prevent confusion with other mods or the base game:

```
XZ_annex_tibet = {
```

More experienced modders can also add news information here, but that is optional.

#### potential

The above conditions put into code:

```
	potential = {
		tag = CHI				#The tag of the taker is CHI.
		civilized = yes				#The taker has westernized/is a civilized nation.
		exists = TIB				#The country with the tag TIB exists.
	}
```

#### allow

```
	allow = {
		is_greater_power = yes			#The taker is a Great Power.
		war = no				#The taker isn't at war.
		TIB = { vassal_of = THIS }		#The country with the tag TIB is a vassal of the taker.
	}
```

#### effect

```
	effect = {
		badboy = 4				#The taker gains 4 infamy.
		prestige = 10				#The taker gains 10 prestige.
		inherit = TIB				#The taker annexes Tibet.
		any_owned = {				#Any province owned by the taker
			limit = {			#for which the follwoing is true:
				is_core = TIB		#It is a core of Tibet
				NOT = { is_core = CHI }	#It isn't a core of China
			}
			add_core = CHI			#China gains a core on.
		}
		any_pop = {				#Any pop living within the takers borders
			limit = { culture = tibetan }	#Which is Tibetan
			militancy = 7			#Add seven Militancy
			consciousness = 3		#Add 3 Consciousness
		}
		set_country_flag = XZ_annexed_tibet	#Give the taker a country flag (if a check for this decision being taken later needs to be done)
	}
```

#### AI instructions

```
	ai_will_do = {					#Adding this block means that the AI will take this decision as soon as all conditions are met.
		factor = 1
	}
}							#Close the entire decision block.
```

#### Implementation

Finally the decision needs to be put into the game. For that three things are necessary:
1. The file containing it has to be in the appropriate folder.
1. It has to be localized, otherwise it will appear in the game as `XZ_annex_tibet_title` with the description `XZ_annex_tibet_desc`.
1. A mod file needs to be created so the engine can properly read the files.

##### File & Folder

<div class="mw-collapsible mw-collapsed">First the decision needs to be enclosed in a `political_decisions` block so the engine knows it is a decision. Expand the final file on the right:
<pre class="mw-collapsible-content">political_decisions = {
	XZ_annex_tibet = {
		potential = {
			tag = CHI
			civilized = yes
			exists = TIB
		}
		allow = {
			is_greater_power = yes
			war = no
			TIB = { vassal_of = THIS }
		}
		effect = {
			badboy = 4
			prestige = 10
			inherit = TIB
			any_owned = {
				limit = {
					is_core = TIB
					NOT = { is_core = CHI }
				}
				add_core = CHI
			}
			any_pop = {
				limit = { culture = tibetan }
				militancy = 7
				consciousness = 3
			}
			set_country_flag = XZ_annexed_tibet
		}
		ai_will_do = {
			factor = 1
		}
	}
}</pre></div>
This is now saved as a normal .TXT file in the new mod's decision folder, for example: `C:\Program Files\Steam\SteamApps\common\Victoria 2\mod\AnnexTibet\decisions`.

##### Localization

Localizing decisions in Victoria 2 is quite simple, the necessary file has the following structure:

```
decision_id_title;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portugese;Russian;Finnish;
decision_id_desc;English;French;German;Polish;Spanish;Italian;Swedish;Czech;Hungarian;Dutch;Portugese;Russian;Finnish;
```

In case of the Tibetan annexation the localization could look something like this:

```
XZ_annex_tibet_title;Annex Tibet;;;;;;;;;;;;;
XZ_annex_tibet_desc;Tibet has been part of the Empire in all but name since 1720, now it will be officially annexed.;;;;;;;;;;;;;
```

In this case there are only English localizations.

This file is now saved as a .CSV file in the `localisation` folder of the mod, for example: `C:\Program Files\Steam\SteamApps\common\Victoria 2\mod\AnnexTibet\localisation`.

##### Mod File

A mod file for such a small mod only neeeds two lines: `name` for the name that will be displayed in the launcher, and `path` to tell the engine which files to load.

```
name = "Annex Tibet"
path = "mod/AnnexTibet"
```

This is saved as a .MOD file in e.g. `C:\Program Files\Steam\SteamApps\common\Victoria 2\mod`

If all these steps are done the mod is complete and should be available for selection in the game launcher.
