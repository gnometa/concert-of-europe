# Modding

Source: https://vic2.paradoxwikis.com/Modding

Modding, or creating mods, is the act of modifying the behavior of the base game (often referred as vanilla), either for personal use, or to release publicly to other players.
As with all Paradox games, Victoria II is moddable to a decent extent.

Motivations of modders may vary widely: better translation to native language, more events or decisions, better map, major overhaul, etc.

Modding is not magic or heresy, anybody can learn to build a mod, and this guide is intended to lower the entry barriers to the world of Vicky 2 modding.

Yet, however good the documentation, there is still a learning curve to it, and it cannot replace the need to read some working vanilla code, and do lots of trial & error experimentations!

For a list of notable mods the community has created, see List of mods.

### Guides

- [Event modding](event-modding.md)
- [Decision modding](how-to-make-a-decision.md)
- [Country modding](creating-a-country.md)
- Economy modding
- [Map modding](map-modding.md)
- [Save-game editing](save-game-editing.md)
- Reform modding
- Performance modding

### Game data

- Full list of effects
- [List of conditions](list-of-conditions.md)
- Full list of scopes
- [Modifier effects](modifier-effects.md)
- [Countries list](countries.md) - Basic info on all countries in the vanilla game, including country tags
- [Province IDs](provinces.md) - A list of all the provinces in the vanilla game, including province ids and resources
- [default.map](default-map.md) - Some information about the what the map file contains

### Miscellaneous

- [Checksum](checksum.md)
- [Localisation](localisation.md)

### Tools & utilities

- The Validator - Find errors quickly and with minimal pain!
- Java Save Game Replayer
- Scenario Editor and Map Viewer
- [Windowed mode instructions](windowed-mode.md)
- Clausewitz Positions Editor
- BMFont Creator
- [SirRunner's Modding Tools](https://github.com/SirRunner/SirRunner-Modding-Tools)

### Tips

- [You should disable the intro video, to save time](disabling-the-intro-video.md)
- To merge mods, you could use [WinMerge](http://winmerge.org//). An easy tool for merging folders and files.

### Various other modding tips

- Your most important tool for figuring out crash issues is the time when the game crashes - if it crashes during startup, you have a grammar issue somewhere in your code (e.g. missing }). If it crashes when you click on 'Start Game' or some time during gameplay, you have a context issue somewhere in the code (e.g. typo in a production_type).
- Factories can have at most 4 input goods.
- A roundabout way to restrict where factories can be built using a non-hardcoded trigger is to apply a highly negative throughput bonus in their production type.
