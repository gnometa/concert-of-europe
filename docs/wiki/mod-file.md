# .mod file

Source: https://vic2.paradoxwikis.com/.mod_file

The **.mod file** is the file that tells the game what a mod is called and where to find it. The file should be located in the mod subfolder of the game directory, alongside the mod's file folder.

### Structure

The following lines are mandatory and should be arranged as follows:

```
name = "modName"
path = "mod/modDirectory"
user_dir = "modDirectory"
```

Optionally, you can declare that your mod is a dependency of another mod. In this case, the base mod is loaded before the secondary mod. Dependencies still require .mod files themselves but do not need to redefine the user_dir.

```
dependencies = { "baseMod" }
```

Optionally, you can add additional lines to direct the game to treat the mod files how you wish them to be treated. For example, the replace_path label indicates that none of the base game files in a given directory will be loaded for the mod. If that label is not given, the base game files will be loaded by default.

```
replace_path = "events"
```

