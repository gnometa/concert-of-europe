# Flag modding

Source: https://vic2.paradoxwikis.com/Flag_modding

This page documents the formatting and creation of flags.

### What does a flag look like?

Flags are found within gfx\flags.

Flags are saved in the ".tga" file format at a size of 93 x 64.

In vanilla, there are five flag slots:
- Default
- Communist
- Fascist
- Monarchy
- Republic

These slots correspond to the "flagType" entries referenced in [governments.txt](governments-txt.md). Note that the game will not run, if there is not a defined flag for each country in the [countries.txt](creating-a-country.md)-file for each government type.

### Creating a new flag

Typically, new flags are only added to the files when a new flag type is created for a new or existing government, or when a new country is added.

When a new flag type is added, all countries must have a flag of that new type added. Otherwise the game will crash.

When a new country is added, a flag must be added for each flag slot. Otherwise the game will crash.

All countries must have as many flags as there are flag slots.
