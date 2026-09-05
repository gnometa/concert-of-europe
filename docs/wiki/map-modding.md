# Map modding

Source: https://vic2.paradoxwikis.com/Map_modding

This page contains information on the map files. Map modding is hard. Victoria 2 is part of the generation of Paradox games where it is a lot less forgiving to mod the map. All maps must also be saved in their correct encoding schemes. The bare minimum required to create a province and add it to the game without crashing on loading:

- Adding an entry in `definition.csv`
- Editing `provinces.bmp`
- Adding a history/provinces file.

Additionally:

- Add it to a region in `regions.txt` - will fix crashing when clicking on the province.
- Adding a history/pops entry.
- Adding a `positions.txt` entry.
- Adding a `climate.txt` entry.
- Adding a `continents.txt` entry.

### Province map

Provinces are drawn on `provinces.bmp` with their entries defined in `definition.csv`. The format of the province definitions is:

```
province;red;green;blue;x;x
1;41;201;201;Comment;x
```

The red, green, and blue values define the colour that is the province shape in `provinces.bmp`. After editing, `provinces.bmp` must be saved in 24 bit without colour space information being written. This is possible in editors such as GIMP or Paint.NET. Before adding any new provinces, it is highly recommended you figure out a workflow that allows you to save `provinces.bmp` in its correct format.

Gaps in the province ids in `definition.csv` cause province ids to be misaligned, which causes all history and localisation to be messed up.

Land provinces cannot be greater than 20000 pixels. If they are larger than that, then the game will launch fine but there will be a glitchy artefact on the map.

### Terrain map

### River map

Rivers run from a source, indicated by a green pixel, to the ocean. Rivers can combine with other rivers using red pixels. Rivers are drawn with a spectrum of blue colours which indicate the river's length at that position - darker blues resulting in wider rivers, cyan blues resulting in thinner rivers.

Editing the river map is best done with GIMP, which allows you finer controls when exporting the resulting .bmp file. Ensure you have the compatibility option "Do not write color space information" ticked.

### Map elements

#### Adjacencies

Adjacencies are provinces that are connected in game but are not physically located next to each other on the map. For example, Istanbul and Uskudar are connected over the Sea of Marmara - or put another way: an army can walk from Istanbul to Uskudar despite the Sea of Marmara being in the way.

Adjancencies can be found in `adjacencies.csv` and are represented in the format:

```
From;To;Type;Through;Data;Comment
860;861;sea;2773;0;Golden Horn
```

`From` and `To` represent the province IDs for the adjacency entry. E.g. 860 for Istanbul, 861 for Uskudar. `Through` represents the sea province that the adjacency is moving through. `Type` can either be "land" or "sea", despite all examples of adjacencies in Victoria 2 being sea. A sea type can be blocked by an enemy navy in the `Through` province. If the `Type` is "land", then the movement cannot be blocked by an enemy. `Data` is 0 in all known examples of adjacencies, and its meaning is unknown. `Comment` is a comment.

#### Climate

Continents are defined in `continent.txt`. The first part of the file defines the climate effects, e.g.:

```
harsh_climate = {
	farm_rgo_size = 0.0
	farm_rgo_eff = 0.0
	mine_rgo_size = 0.0
	mine_rgo_eff = 0.0
	max_attrition = 5
}
```

And the second half of the file defines which provinces belong to which climate:

```
harsh_climate = {
    [provid] [provid] [provid] [provid]
}
```

Climates have no effect in the base game except attrition.

#### Continent

Continents are defined in `continent.txt`. The basic structure is:

```
[continent] = {
    provinces = {
        [provid] [provid] [provid]
    }
    [any continent based province effects]
}
```

You can add extra continents. However, note that the continents on the diplomacy screen filters are hardcoded to use `europe`, `asia`, `africa`, `north_america`, `south_america`, `oceania`, therefore it is not recommended for modders to add extra continents. You can redefine their meanings by changing the continent localisation, however.

A province can be in multiple continents.

If `continents.txt` is empty, the game will crash on the build military unit screens.

#### Positions

The `positions.txt` determines where province map items such as the text, unit, city, and buildings are placed on the map. This can be useful to fix issues such as: a city that should be coastal is not appearing on the coast, or the province is very weirdly shaped and armies are not showing up as standing in the province.

An example excerpt from the positions.txt file:

```
# Sitka
1 = {
    text_position = {
        x = 698.068333
        y = 1976.978333
    }

    text_rotation = 5.322703
    text_scale = 3.5
    unit = {
        x = 699.000000
        y = 1978.000000
    }

    city = {
        x = 701.050000
        y = 1968.770000
    }

    factory = {
        x = 734.000000
        y = 1951.000000
    }

    building_construction = {
        x = 637.800000
        y = 2035.240000
    }

    military_construction = {
        x = 732.000000
        y = 1949.000000
    }

    building_position = {
        fort = {
            x = 612.606667
            y = 2048.795000
        }

        railroad = {
            x = 665.630000
            y = 2014.770000
        }

        naval_base = {
            x = 703.000000
            y = 1960.000000
        }

    }

    building_rotation = {
        naval_base = 5.672319
    }

}
```

Manually editing positions is tedious and prone to mistakes, so there are a few community tools to edit the positions through a GUI, such as the Clausewitz Positions Editor.<ref>[Clausewitz Positions Editor](https://forum.paradoxplaza.com/forum/threads/clausewitz-positions-editor.535767/), Paradox Plaza, 2011-05-08</ref> Its also been discovered how to enter the official positions editor (nudge mode) by altering the Victoria 2 binary.<ref>[I've just discovered the way to enter the Nudge Mode in Victoria 2!!!! TUTORIAL](https://old.reddit.com/r/victoria2/comments/1te46te/ive_just_discovered_the_way_to_enter_the_nudge/) Reddit, 2026-05-15</ref>

It is not required that all provinces are defined in `positions.txt`. Indeed, the file can be blank and the game will launch and play just fine. In cases where the positions entry for a province is missing, all items will default to appearing at the coordinates of the x midpoint and y midpoint.

#### States

States are defined in `region.txt`. The basic structure is:

```
[region name] = { [provid] [provid] [provid] }
```

Province can exist in multiple regions at the same time. In such cases, its first region is the state it will appear in. Mods have used this fact to have regions for all land provinces or all oil producing provinces to make conditional checks easier. Blank regions can also exist, which is used in [Dynamic localisation](dynamic-localisation.md).

If a province is not a part of any region, it will crash when you click the province in game.

#### Terrain types

### References

<references />
