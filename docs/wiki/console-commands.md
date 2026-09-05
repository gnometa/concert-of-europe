# Console commands

Source: https://vic2.paradoxwikis.com/Console_commands

This page lists the codes which may be input into the Console Window, a special debugging window which may be accessed by pressing the ` key (button may vary on non-American keyboards). Press the up or down arrow keys to traverse through previously executed commands. Many codes can be turned off by repeating the command, but sometimes reloading the save or exiting the game is necessary.

They are often considered cheating to use.

### List of Commands

| Expansion or patch required | Command | Effect | Example | Comments |
|---|---|---|---|---|
|  | money [amount] | Adds the desired amount of money to the player's nation's cash reserves. | money 15000 |  |
| patch 1.2 | prestige [amount] | Gives a specified amount of prestige to the player. | prestige 100 | Prestige change is affected by technologies. |
|  | leadership [amount] | Adds the desired amount of leadership to the player's nation's leadership reserves. | leadership 3 |  |
|  | goods [amount] | Gives the player the amount specified of all the goods in the game plus the same amount of money. Default is 10000. | goods 5000 | Warning: creating a large amount of goods with this code will probably lead to economic problems. |
|  | plurality [number] | Set the player plurality to the number given. | plurality 75 |  |
|  | revolt [province id] | Rise all the valid rebels of the country that controls [province id] | revolt 1 | Use twice for it to take effect |
|  | instantconstruction | Buildings finish in one day. | instantconstruction | Affects human and AI players. |
|  | inc | Buildings finish in one day. | inc | Affects only human players, not the AI. |
|  | instantresearch | Research finishes in one day. | instantresearch | Affects human and AI players. |
|  | inr | Research finishes in one day. | inr | Affects only human players, not the AI. |
|  | yesmen | The AI accepts any deal with the player or other AI players. | yesmen | This was changed to "debug yesmen" in the initial release of HoD. |
| HoD | debug yesmen | The AI accepts any deal with the player or other AI players. | debug yesmen |  |
|  | tag [TAG] | Change the player country to the one specified. | tag USA | The tag must be capitalized. More than 1 change "sleeps" the AI of the affected country until reload. |
|  | event [event id] [province id] | Trigger province [event](event.md)s, regardless of the event requirements. | event 5162 1 | This command applies to province events only. If the province ID is not specified, the event is triggered in the capital province of the player's country. |
|  | event [id] [TAG] | Trigger country [event](event.md)s, regardless of the event requirements. | event 2001 USA | This command applies to country events only. If the country tag is not specified, the event is triggered in the player's country. |
|  | changeowner [TAG] [province id] | Change the current owner of [province id] to the TAG specified. | changeowner USA 1 |  |
|  | changecontroller [TAG] [province id] | Change the current controller of [province id] to the TAG specified. | changecontroller USA 1 | Unless there is a war between the original owner and the specified country the province will return to the original owner. |
|  | conquerall [TAG] | Set all enemy provinces under the current country's control. | conquerall USA | Unless there is a war between the specified country and the current country the provinces will return to the original owner. |
|  | showprovinceid | Shows the id of the provinces. | showprovinceid |  |
|  | provid | Shows the id of the provinces. | provid | A shortened version of the previous command. |
|  | spawnunit [unit] [province id] | A [unit] appears in the province specified at 0 organization and full strength. | spawnunit hussar 206 | In case of a land unit, the soldiers will come from a random province. |
|  | reload <filename> | Allows some files, such as the interface files, to be reloaded. | reload interface.gfx | No-one is sure which files can be reloaded and which cannot. |
|  | reloadfx <effectname> | Reloads the specified shaders. | reloadfx map |  |
|  | reloadtexture <name> | Reloads the specified texture. | reloadtexture grass.png |  |
|  | break | Enforces rebel/movement demands. | break | The top-level rebels available in the movement window are the ones that have their demands met. |
|  | upperhouse | Trigger a reelection of the upper house. | upperhouse |  |
|  | election | Starts common elections. | election |  |
|  | militancy [level] | Changes militancy of all pops by the specified amount. | militancy 1 | Both positive and negative values work. |
|  | date | Changes the date. | date 1862.5.13 |  |
|  | fow | Turns on\of fog of war. | fow |  |
| HoD | debug fow | Turns on\of fog of war. | debug fow |  |
|  | debug invent [invention] | Discover specified invention. | debug invent gas_attack | The names of all inventions are in the *inventions* folder. The "debug" part of this command may not be required. |
|  | debug market | Turns on/off a log of price changes. | debug market | The log is located at which is located in My documents/Paradox Interactive/Victoria 2/Logs/game.log, and has a format described at [1]. |
|  | debug minzoom | Controls maximum and minimum camera zoom. | minzoom |  |
|  | debug cb_use <cb_type> <TAG> <TAG> | Show all the requirements for a certain Casus Belli, marking which ones are currently valid or invalid. The first TAG is the country trying to use the CB; the second TAG is the country against the CB is evaluated. | debug cb_use conquest_cb USA MEX | The list can be too long to be completely displayed. |
|  | wireframe | Switches units' 3D models to wireframe mode. | wireframe |  |
|  | blockade <provinceid> | Blockades the specified province. | blockade 1 |  |
|  | reorg <provinceid> | All units in the specified province get 100% organization and full strength. | reorg 12 |  |
|  | fullscreen | Changes screen to fullscreen mode. | fullscreen |  |
|  | debug allmoney | Shows info for money transfers. | debug allmoney |  |
|  | debug alwaysdiplo | Makes diplomats endless. | debug alwaysdiplo |  |
|  | debug alwaysaddwargoal | Removes limitations for adding wargoals. | debug alwaysaddwargoal |  |
|  | researchpoints [number] | Grants the specified number of research points. | researchpoints 9001 |  |
|  | debug alwaysreform | Eliminates the 1-month wait between reforms. | debug alwaysreform | It's unknown if it this affects the AI. |
|  | debug influence | Makes every Great Power's influence on every country fixed at 100. When deactivated, all influence levels return to normal. | debug influence | Also affects the AI. It doesn't show any message on console when activated or deactivated. |
| HoD | debug assert | Events won't pause the game. | debug assert | This is a regular game option that you can switch on and off in some newer Paradox games. |
|  | suppress | Set suppression points to 100. | suppress |  |
| HoD | showrails(rails) | Toggles the railroads visibility mode | showrails(rails) |  |
| HoD | Citysize [on/off] [<size 0-100>(if on)] | Overrides the cities size. | Citysize [off] |  |
| HoD | newsfakegenerateall(fakenewsall) [<stylename>] [<randomseed>] | Generates fake news for each possible fake defined. | newsfakegenerateall(fakenewsall) [<stylename>] [<randomseed>] |  |
| HoD | newsfakegenerate(fakenews) [articlename] [<stylename>] [<randomseed>] | Generates fake news for specified article name. | newsfakegenerate(fakenews) [articlename] [<stylename>] [<randomseed>] |  |
| HoD | reloadnewsdatabase(reloadnews) [articlename] [<stylename>] [<randomseed>] | Reloads the news databases and styles. | reloadnewsdatabase(reloadnews) |  |
| HoD | newsgeneratefrompath(newsfrom) [path] [<stylename>] [<randomseed>] | Generates news from specified folder. | newsgeneratefrompath(newsfrom) [path] [<stylename>] [<randomseed>] |  |
| HoD | newsgenerate(news) [filename] [<stylename>] [<randomseed>] | Generates news from file. | newsgenerate(news) [filename] [<stylename>] [<randomseed>] |  |
| HoD | addresearch(addr) [techname] | Adds research at specified name. | addresearch(addr) [techname] | Typing an invalid technology name crashes the game, so use with caution. Technology names can be found in inventions.txt in the game files. |
| HoD | leaderprestige(lprestige) [province] [value] | Adds prestige to leaders attached to units at specified location. | leaderprestige(lprestige) [1456] [10] |  |
| HoD | togglepopupdate(popupdate) | Toggles ON/OFF updating pops. | togglepopupdate(popupdate) |  |
| HoD | popstat | Prints out amount of active pops. | popstat |  |
| HoD | breakalliances(breakally) [<tag>] | Breaks all alliances for you or for specific country. | breakalliances(breakally) [ENG] |  |
| HoD | lua [luacode] | Executes lua code typed instead of arguments. | lua [luacode] |  |
| HoD | technologylist(techs) | Prints out all technologies | technologylist(techs) |  |
| HoD | morehumans(humans) [num] | Adds more humans | morehumans(humans) [2] |  |
| HoD | window(wnd) [Arguments: open/close] [window gui name] | Opens or closes the specified window | window(wnd) [Arguments: open/close] [window gui name] |  |
| HoD | randomlog | Toggles random logging | randomlog |  |
| HoD | reload [file name] | Reloads the gui or lua file | reload [file name] |  |
| HoD | reloadinterface | Reloads the entire interface | reloadinterface |  |
| HoD | reloadfx [Arguments: map or *.fx filename] | Reloads the shader | reloadfx [Arguments: map or *.fx filename] |  |
| HoD | reloadtexture [texture file name] | Reloads the specified texture | reloadtexture [texture file name] |  |
| HoD | paint | Switch to map painting mode. | paint |  |
| HoD | rpaint | Switch to region painting mode. | rpaint |  |
| HoD | cpaint | Switch to continent painting mode. | cpaint |  |
| HoD | teleportselectionto(teleport) [province id] | Teleports currently selected unit to location | teleportselectionto(teleport) [1] |  |
| HoD | reorg [province id] | Reorganize all units at location (includes enemies, so use wisely) | reorg [1] (reorganizes units in Stockholm) |  |
| HoD | tutorial [chapter id] [<reload>] | Sets or reload tutorial | tutorial [1] [<reload>] |  |
| HoD | copyprov | Copy selected provinces ids to clipboard | copyprov |  |
| HoD | spawnactor [actor name] [province id] [<animation>] [<gun>] [<hat>] | Spawns 3d object at location | spawnactor [actor name] [province id] [<animation>] [<gun>] [<hat>] |  |
| HoD | helplog | Print out all console commands to game.log file. | helplog |  |
| HoD | help [Command name] | Print out all console commands or a specific command description. | helplog |  |

### External links

- Cheat and Events...

### Unconfirmed or not working commands

 

**promotiondesc**: Somehow should descript pop promotion. Looks like game crashing.

**demotiondesc**: Somehow should descript pop demotion. Looks like game crashing.

**cthulhu**: Calls Cthulhu R'lyeh.

**help**: Displays the message 'No help for you!' Work in Heart of Darkness.

morehumans

rand_log    Rand log enabled

tech

list

lua

window Valid commands are: open <windowName> close reload  

view_ai 

no_pop_update   Pops are not updating   Pops are updating

tutorial

All follow use with debug prefix:

debug   lines

alwaysupgradecolony (Always can upgrade colony)

natfoc  Prio for:

artisanchange

focusai National focus

ai debug toggled water???

shadow  shadows info

profile

tooltips

assert

eco

textures    Texture info has been written to the debug log.

render Render options:  Trees:	  yes   no Borders: Text: Overlay: Objects: MapObjects:	Rivers:	  		Water:	   		WaterBorders:	    		Effects:

save

spawnactor Syntax is spawnactor <actorname> <provinceid> [animation] [gun] [hat]

Flag

name

HelmetNode

test

addresearch

runresearch

processinvent}}

[1]Format of the log generated[worldmarket.cpp:861]: Ammunition demand: 2213.24

[worldmarket.cpp:862]: Ammunition supply: 731.901

[worldmarket.cpp:863]: Ammunition price: 15.5681

....

TOTAL_LEFT_ON_WORLD_MARKET_NOT_BOUGHT

[worldmarket.cpp:1538]: --------------------------------------------

[worldmarket.cpp:1546]: Ammunition _ActualSold Domestic markets: 444.897

[worldmarket.cpp:1547]: Ammunition Suppply World markets: 366.213

[worldmarket.cpp:1549]: Ammunition _ActualSold World: 130.501

[worldmarket.cpp:1550]: Ammunition left on market: 235.712

....

ACTUAL SOLD

[worldmarket.cpp:3001]: --------------------------------------------

[worldmarket.cpp:3006]: Ammunition(i:0) sold(domestic): 444.897

[worldmarket.cpp:3007]: Ammunition(i:0) sold(world): 130.501

....

EXPORTED_TO_WORLD_MARKET_FOR_NEXT_TURN

[worldmarket.cpp:3011]: --------------------------------------------

[worldmarket.cpp:3016]: Ammunition on next market: 290.749}}
