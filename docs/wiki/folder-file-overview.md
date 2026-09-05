# Folder/File overview

Source: https://vic2.paradoxwikis.com/Folder/File_overview

### Overview

This is a list of what the files and folders inside the main Victoria 2 folder mean, knowing what files go where, and where to make changes is the most important part of modding, as something in the wrong place can easily lead to a fatal crash.

Note that Victoria II's files need to be saved with ANSI encoding in order to work properly in the game. Additionally, some files seem to be encoded in a weird manner (such as some of the province history files), resulting in the game reading their contents as a single line. This can be fixed by creating a new .txt file with ANSI encoding with Notepad++ and copying the contents of the old file to it, deleting the old one and replacing it with the new.

### The Files

| File/Folder | What it contains |
|---|---|
| Victoria II\battleplans | Settings for battle plan editor |
| Victoria II\common\ | General information |
|  *[bookmarks.txt](bookmark-modding.md) *[buildings.txt](buildings-txt.md) *cb_types.txt *[countries.txt](creating-a-country.md) *country_colors.txt *[crime.txt](crime-modding.md) *[cultures.txt](culture-modding.md) *[defines.lua](defines-lua.md) *[event_modifiers.txt](event-modding.md) *goods.txt *[governments.txt](governments-txt.md) *ideologies.txt *issues.txt *[national_focus.txt](national-focus-modding.md) *[nationalvalues.txt](national-value-modding.md) *on_actions.txt *pop_types.txt *production_types.txt *rebel_types.txt *[religion.txt](religion-modding.md) *static_modifiers.txt *technology.txt *traits.txt *[triggered_modifiers.txt](triggered-modifiers-txt.md) *country\<country name>.txt |  *Defines scenarios/start dates *Building statistics *Casus belli attributes and types *Which tag is linked to which <country name>.txt in common\countries *RGB code for each country *All crimes and effects *Culture groups, names and colors along with cultural unions *POP, general, diplomatic, economic and military variables *All [event](event.md) and province modifiers and their effects *All goods with their starting price and color *All government types with their ideology and effects *All ideologies and their views on reforms *All reforms (political, social and civilizing) and party issues and their effects *All national focusses and their effects *All national values and the effects *Specially triggered effects *Mean Time To Happen (MTTH) for POP actions (promotion, assimilation etc.) *Production statistics *All rebel types, their goals and chances for rebelling *All religions, their icons and colors *All difficulty, rank and standard modifiers *Technology data *Traits of leaders and their effects *Empty by default *Color, political parties and ship names |
| Victoria II\decision\ | Decisions folder, all decisions are stored here |
| Victoria II\events\ | Events folder, all event files are kept here |
| Victoria II\gfx\ | Graphics |
| Victoria II\history\ | Data on each province, diplomatic relations, country, units and POPs |
| Victoria II\interface\ | Interface Graphics |
| Victoria II\inventions\ | All inventions together with requirements, invention chances and effects |
| Victoria II\launcher\ | Launcher graphics and configuration |
| Victoria II\localisation\ | All text data for things like country names and event description, [has options for other languages](localisation.md) |
| Victoria II\map\ | Map settings, province shapes, continents, regions etc. |
| Victoria II\mod\ | Folder for storing mods and [.mod file](mod-file.md)s |
| Victoria II\movies\ | Game intro movie |
| Victoria II\music\ | Music used by the game |
| Victoria II\news\ | All news stories |
| Victoria II\poptypes\ | All POP data for each specific POP type |
| Victoria II\script\ | All scripts |
| Victoria II\sound\ | All sounds except music |
| Victoria II\technologies\ | Technologies with their effects and attributes |
| Victoria II\tutorial\ | Tutorial configuration |
| Victoria II\units\ | All military unit attributes, for each specific unit |

Pop files note: Issue and Ideology modifiers are multipliers, all other seem to be additions.

### See also

- [Advanced events](event-modding.md)
- [Full list of commands](list-of-conditions.md)
- Full list of effects
- Full list of scopes
- [Modifier effects](modifier-effects.md)
